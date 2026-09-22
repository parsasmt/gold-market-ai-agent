import time
import re

from openai import OpenAI
from openai import RateLimitError, APIError, APITimeoutError

from config import (
    OPENROUTER_API_KEY,
    BASE_URL,
    MODELS,
    ENABLE_REASONING,
    MAX_RETRIES_PER_MODEL,
    RETRY_DELAY_SECONDS,
    MAX_RETRY_DELAY_SECONDS,
    MODEL_COOLDOWN_SECONDS,
)

from prompts import SYSTEM_PROMPT


# ============================================================
# MODEL COOLDOWN TRACKING
# ============================================================

# Example:
# {
#     "z-ai/glm-5.2:free": 1758540000.0
# }
#
# If the current time is lower than the stored timestamp,
# that model is temporarily skipped.

model_cooldowns = {}


# ============================================================
# OPENROUTER CLIENT
# ============================================================

client = OpenAI(
    base_url=BASE_URL,
    api_key=OPENROUTER_API_KEY,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def is_model_on_cooldown(model: str) -> bool:
    """
    Check whether a model is temporarily unavailable because
    it previously returned a rate-limit error.
    """

    cooldown_until = model_cooldowns.get(model)

    if cooldown_until is None:
        return False

    if time.time() >= cooldown_until:
        # Cooldown expired.
        del model_cooldowns[model]
        return False

    return True


def put_model_on_cooldown(model: str):
    """
    Temporarily disable a model after a 429 response.
    """

    model_cooldowns[model] = (
        time.time() + MODEL_COOLDOWN_SECONDS
    )


def get_retry_after_seconds(error) -> float:
    """
    Try to extract Retry-After from an OpenRouter/OpenAI error.

    If unavailable, use the configured default retry delay.
    """

    # Some OpenAI exceptions expose response headers.
    try:
        response = getattr(error, "response", None)

        if response is not None:
            headers = getattr(response, "headers", None)

            if headers:
                retry_after = headers.get("retry-after")

                if retry_after:
                    try:
                        value = float(retry_after)

                        return min(
                            value,
                            MAX_RETRY_DELAY_SECONDS
                        )

                    except (ValueError, TypeError):
                        pass
    except Exception:
        pass

    # Sometimes Retry-After appears in the error text.
    try:
        error_text = str(error)

        match = re.search(
            r"retry[- ]after[: ]+(\d+(?:\.\d+)?)",
            error_text,
            re.IGNORECASE
        )

        if match:
            value = float(match.group(1))

            return min(
                value,
                MAX_RETRY_DELAY_SECONDS
            )

    except Exception:
        pass

    return RETRY_DELAY_SECONDS


def is_retryable_error(error) -> bool:
    """
    Determine whether the request should be retried.

    Retry:
        429 rate limit
        408 timeout
        5xx provider/server errors

    Do not retry:
        authentication errors
        invalid request errors
        invalid model errors
        other permanent errors
    """

    if isinstance(error, RateLimitError):
        return True

    if isinstance(error, APITimeoutError):
        return True

    if isinstance(error, APIError):

        status_code = getattr(
            error,
            "status_code",
            None
        )

        if status_code in {
            408,
            409,
            429,
            500,
            502,
            503,
            504
        }:
            return True

    # Some versions of the OpenAI Python SDK may expose
    # slightly different exception types, so also inspect
    # the error text as a fallback.

    error_text = str(error).lower()

    temporary_errors = [
        "429",
        "rate limit",
        "too many requests",
        "temporarily unavailable",
        "service unavailable",
        "bad gateway",
        "gateway timeout",
        "timeout",
        "upstream",
        "503",
        "502",
        "504",
        "server error",
    ]

    return any(
        phrase in error_text
        for phrase in temporary_errors
    )


def get_error_type(error) -> str:
    """
    Produce a short human-readable error classification.
    """

    if isinstance(error, RateLimitError):
        return "rate limited"

    if isinstance(error, APITimeoutError):
        return "timeout"

    if isinstance(error, APIError):

        status_code = getattr(
            error,
            "status_code",
            None
        )

        if status_code:
            return f"HTTP {status_code}"

    error_text = str(error).lower()

    if "429" in error_text or "rate limit" in error_text:
        return "rate limited"

    if "timeout" in error_text:
        return "timeout"

    if "503" in error_text:
        return "HTTP 503"

    if "502" in error_text:
        return "HTTP 502"

    if "504" in error_text:
        return "HTTP 504"

    return "request error"


# ============================================================
# SINGLE MODEL REQUEST
# ============================================================

def request_model(
    model: str,
    messages: list
):
    """
    Send one request to one model.

    Returns:
        assistant text

    Raises:
        Exception if the model request fails.
    """

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        extra_body={
            "reasoning": {
                "enabled": ENABLE_REASONING
            }
        }
    )

    if not response.choices:
        raise RuntimeError(
            f"{model} returned no choices."
        )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            f"{model} returned an empty response."
        )

    return content


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze(prompt, chat_history=None):
    """
    Generate an answer using multiple OpenRouter models
    with automatic retry and fallback.

    Behavior:

    Model 1
       |
       +-- success --> return answer
       |
       +-- temporary error
       |      |
       |      +-- retry
       |      +-- retry
       |      +-- next model
       |
       +-- permanent error --> next model

    Model 2
       |
       ...
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if chat_history:
        messages.extend(chat_history)

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    failed_models = []

    for model in MODELS:

        # ----------------------------------------------------
        # Skip models currently on cooldown
        # ----------------------------------------------------

        if is_model_on_cooldown(model):
            failed_models.append(
                f"{model}: currently on cooldown"
            )

            print(
                f"[SKIP] {model} "
                f"(temporarily rate limited)"
            )

            continue

        # ----------------------------------------------------
        # Try this model
        # ----------------------------------------------------

        for attempt in range(
            MAX_RETRIES_PER_MODEL + 1
        ):

            try:

                print(
                    f"[TRY] {model} "
                    f"(attempt {attempt + 1}/"
                    f"{MAX_RETRIES_PER_MODEL + 1})"
                )

                answer = request_model(
                    model=model,
                    messages=messages
                )

                print(
                    f"[SUCCESS] {model}"
                )

                return answer

            except Exception as error:

                error_type = get_error_type(error)

                print(
                    f"[ERROR] {model} -> "
                    f"{error_type}: {error}"
                )

                # ------------------------------------------------
                # Temporary error
                # ------------------------------------------------

                if is_retryable_error(error):

                    # If this was a rate-limit error,
                    # remember that the model is temporarily
                    # unavailable.
                    if (
                        isinstance(error, RateLimitError)
                        or "429" in str(error)
                        or "rate limit" in str(error).lower()
                    ):
                        put_model_on_cooldown(model)

                    # If retries remain, wait and retry.
                    if attempt < MAX_RETRIES_PER_MODEL:

                        retry_delay = (
                            get_retry_after_seconds(error)
                        )

                        print(
                            f"[RETRY] {model} "
                            f"in {retry_delay:.1f}s"
                        )

                        time.sleep(retry_delay)

                        continue

                    # No retries remaining.
                    failed_models.append(
                        f"{model}: {error_type}"
                    )

                    print(
                        f"[FALLBACK] "
                        f"Moving to next model."
                    )

                    break

                # ------------------------------------------------
                # Permanent error
                # ------------------------------------------------

                failed_models.append(
                    f"{model}: {error_type}"
                )

                print(
                    f"[FALLBACK] "
                    f"Permanent error. "
                    f"Moving to next model."
                )

                break

    # ========================================================
    # ALL MODELS FAILED
    # ========================================================

    error_summary = "\n".join(
        f"- {item}"
        for item in failed_models
    )

    return (
        "I could not generate a response because all "
        "configured AI models are currently unavailable.\n\n"
        "Model status:\n"
        f"{error_summary}\n\n"
        "Please try again in a few minutes."
    )