from market_data import get_market_data
from news_fetcher import get_gold_news, format_news_for_prompt
from prompts import build_prompt
from llm_analyzer import analyze


class GoldMarketAgent:

    def __init__(self):
        self.chat_history = []

    def run(self, question: str):
        try:
            # ====================================================
            # 1. GET CURRENT MARKET DATA
            # ====================================================

            market_data = get_market_data()

            # ====================================================
            # 2. GET RECENT GOLD-RELATED NEWS
            # ====================================================

            news = get_gold_news()
            news_text = format_news_for_prompt(news)

            # ====================================================
            # 3. DETERMINE RESPONSE DETAIL LEVEL
            # ====================================================

            detailed_keywords = [
                "analysis",
                "analyze",
                "forecast",
                "outlook",
                "trend",
                "risk",
                "detailed",

                # Persian
                "تحلیل",
                "تحلیل کن",
                "بررسی",
                "چشم انداز",
                "چشم‌انداز",
                "پیش بینی",
                "پیش‌بینی",
                "روند",
                "ریسک",
                "کامل",
            ]

            question_lower = question.lower()

            detailed = any(
                keyword in question_lower
                for keyword in detailed_keywords
            )

            # ====================================================
            # 4. BUILD THE LLM PROMPT
            # ====================================================

            prompt = build_prompt(
                question=question,
                market_data=market_data,
                news_text=news_text,
                detailed=detailed,
            )

            # ====================================================
            # 5. SEND TO LLM
            #
            # analyze() now handles:
            #
            #   - multiple models
            #   - retries
            #   - 429 errors
            #   - temporary cooldowns
            #   - automatic fallback
            #
            # So agent.py does not need to know which model
            # ultimately generated the response.
            # ====================================================

            response = analyze(
                prompt=prompt,
                chat_history=self.chat_history,
            )

            # ====================================================
            # 6. SAVE CONVERSATION HISTORY
            # ====================================================

            self.chat_history.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

            return response

        except Exception as e:
            return f"Agent error: {str(e)}"

    # ========================================================
    # GET CHAT HISTORY
    # ========================================================

    def get_history(self):
        return self.chat_history

    # ========================================================
    # CLEAR CHAT HISTORY
    # ========================================================

    def clear_history(self):
        self.chat_history = []
