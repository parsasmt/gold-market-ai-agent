SYSTEM_PROMPT = """
You are an expert financial analyst specializing in the gold market.

Your responsibilities are:

1. Analyze current market data.
2. Analyze recent economic and geopolitical news.
3. Answer the user's question clearly and professionally.
4. Support both Persian and English.
5. Explain your reasoning briefly.
6. Mention important risks and uncertainties.
7. Never guarantee future prices.
8. Do not give financial advice.

LANGUAGE RULE (VERY IMPORTANT):

The user's language determines the response language.

If the user's question contains Persian text:
- Respond entirely in Persian.
- Never switch to English.
- Never provide an English translation unless explicitly requested.

If the user's question contains English text:
- Respond entirely in English.

This rule has higher priority than all other instructions.

Provide structured responses with:

- Current market situation
- Impact of recent news
- Short-term outlook
- Risks
- Final answer

End every response with:

"This analysis is for informational purposes only and is not financial advice."
"""


def detect_language(text):
    """
    Simple Persian language detection.
    """

    for char in text:
        if '\u0600' <= char <= '\u06FF':
            return "Persian"

    return "English"



def build_prompt(question, market_data, news_text,detailed=False):
    """
    Build the prompt sent to the LLM.
    """

    language = detect_language(question)

    if detailed:
        response_style = """
    Provide a detailed analysis with the following sections:

    1. Current Market Situation
    2. Effect of Recent News
    3. Short-Term Outlook
    4. Main Risks
    5. Final Answer
    """
    else:
        response_style = """
    Provide only a concise direct answer.

    Rules:
    - No headings
    - No sections
    - No bullet points unless necessary
    - Maximum 2-3 short paragraphs
    - Focus on answering the user's question directly
    """


    prompt = f"""

    User Language: {language}

IMPORTANT INSTRUCTION:

You MUST answer entirely in {language}.

If User Language is Persian:
- Answer only in Persian.
- Do NOT answer in English.
- Do NOT mix Persian and English except for financial terms and symbols.

If User Language is English:
- Answer only in English.

Current Market Data

Gold
Price: {market_data["gold"]["price"]}
Daily Change (%): {market_data["gold"]["daily_change_percent"]}
Weekly Change (%): {market_data["gold"]["weekly_change_percent"]}

US Dollar Index (DXY)
Price: {market_data["dxy"]["price"]}
Daily Change (%): {market_data["dxy"]["daily_change_percent"]}
Weekly Change (%): {market_data["dxy"]["weekly_change_percent"]}

Silver
Price: {market_data["silver"]["price"]}
Daily Change (%): {market_data["silver"]["daily_change_percent"]}
Weekly Change (%): {market_data["silver"]["weekly_change_percent"]}

Crude Oil
Price: {market_data["oil"]["price"]}
Daily Change (%): {market_data["oil"]["daily_change_percent"]}
Weekly Change (%): {market_data["oil"]["weekly_change_percent"]}


Recent News

{news_text}


User Question

{question}


Instructions

{response_style}

Avoid speculation and do not provide financial advice.
"""

    return prompt