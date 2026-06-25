from market_data import get_market_data
from news_fetcher import get_gold_news, format_news_for_prompt
from prompts import build_prompt
from llm_analyzer import analyze


class GoldMarketAgent:
    """
    Main AI Agent that combines:
    - Market data
    - News data
    - LLM reasoning
    """

    def __init__(self):
        self.chat_history = []

    def run(self, question: str):
        """
        Main pipeline:
        1. Get market data
        2. Get news
        3. Build prompt
        4. Call LLM
        5. Store history
        """

        try:
            # 1. Market Data
            market_data = get_market_data()

            # 2. News Data
            news = get_gold_news()
            news_text = format_news_for_prompt(news)

            # 3. Build Prompt
            detailed_keywords = [
                    "analysis",
                    "analyze",
                    "forecast",
                    "outlook",
                    "trend",
                    "risk",
                    "detailed",

                    "تحلیل",
                    "تحلیل کن",
                    "بررسی",
                    "چشم انداز",
                    "پیش بینی",
                    "روند",
                    "ریسک",
                    "کامل"
            ]

            detailed = any(
                keyword in question.lower()
                for keyword in detailed_keywords
            )

            prompt = build_prompt(
                question=question,
                market_data=market_data,
                news_text=news_text,
                detailed=detailed
            )

            # 4. Call LLM
            response = analyze(
                prompt=prompt,
                chat_history=self.chat_history
            )

            # 5. Save conversation
            self.chat_history.append({
                "role": "user",
                "content": question
            })

            self.chat_history.append({
                "role": "assistant",
                "content": response
            })

            return response

        except Exception as e:
            return f"Agent error: {str(e)}"


def get_history(self):
    return self.chat_history

# # Optional test run
# if __name__ == "__main__":

#     agent = GoldMarketAgent()

#     while True:

#         q = input("\nAsk your question (or type 'exit'): ")

#         if q.lower() == "exit":
#             break

#         answer = agent.run(q)

#         print("\n====================")
#         print(answer)
#         print("====================\n")