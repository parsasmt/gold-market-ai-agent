from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    BASE_URL,
    MODEL_NAME,
    ENABLE_REASONING
)

from prompts import SYSTEM_PROMPT


# client = OpenAI(
#     base_url=BASE_URL,
#     api_key=OPENROUTER_API_KEY
# )


def analyze(prompt, chat_history=None):
    """
    Generate an answer using GPT-OSS-120B.
    """
    client = OpenAI(
    base_url=BASE_URL,
    api_key=OPENROUTER_API_KEY
    )


    try:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Add previous conversation if available
        if chat_history:
            messages.extend(chat_history)

        # Add current request
        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            extra_body={
                "reasoning": {
                    "enabled": ENABLE_REASONING
                }
            }
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Error while communicating with OpenRouter:\n{e}"
    