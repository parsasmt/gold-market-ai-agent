from tavily import TavilyClient

from config import (
    TAVILY_API_KEY,
    MAX_NEWS_RESULTS
)

# Initialize Tavily client
client = TavilyClient(api_key=TAVILY_API_KEY)


def get_gold_news():
    """
    Fetch recent news related to the gold market.
    """

    try:

        response = client.search(
            query="""
            latest gold market news,
            Federal Reserve interest rates,
            inflation,
            US Dollar Index,
            geopolitical tensions
            """,
            max_results=MAX_NEWS_RESULTS
        )

        news_list = []

        for article in response["results"]:

            news_item = {
                "title": article.get("title", ""),
                "content": article.get("content", ""),
                "url": article.get("url", "")
            }

            news_list.append(news_item)

        return news_list

    except Exception as e:

        print("Error type:", type(e))
        print("Error details:", repr(e))

        return []
    
def format_news_for_prompt(news_list):
    """
    Convert list of news articles into formatted text.
    """

    if not news_list:
        return "No recent news available."

    formatted_news = ""

    for i, article in enumerate(news_list, start=1):

        formatted_news += (
            f"News {i}\n"
            f"Title: {article['title']}\n"
            f"Summary: {article['content']}\n"
            f"Source: {article['url']}\n\n"
        )

    return formatted_news


if __name__ == "__main__":

    news = get_gold_news()

    print("\n===== Latest Gold News =====\n")

    for i, article in enumerate(news, start=1):

        print(f"News {i}")

        print("Title:")
        print(article["title"])

        print("\nSummary:")
        print(article["content"])

        print("\nURL:")
        print(article["url"])

        print("\n" + "-" * 70 + "\n")