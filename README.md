# Gold Market AI Agent

An AI-powered gold market analysis assistant built with Python and Streamlit. The system combines real-time financial market data, recent financial news, large language models, and conversational context to provide interactive gold-market analysis.

The application is designed as both a practical financial-information assistant and a demonstration of how an LLM-powered agent can combine external tools, structured market data, news retrieval, model reasoning, and a web interface into a single system.

> Disclaimer: This application is intended for informational and educational purposes only. It does not provide financial advice, investment recommendations, or guaranteed predictions.

---

## Overview

Gold prices are influenced by a wide range of factors, including:

* US interest rates
* Federal Reserve policy
* Inflation
* US dollar strength
* Treasury yields
* Geopolitical developments
* Crude oil and commodity markets
* Investor sentiment
* Broader financial-market conditions

A conventional chatbot may have difficulty answering questions about these factors because its internal knowledge may not contain current market conditions or recent events.

Gold Market AI Agent addresses this by retrieving current market information and recent news before asking an LLM to analyze the user's question.

The general workflow is:

```text
User Question
      │
      ▼
Gold Market AI Agent
      │
      ├──────────────► Yahoo Finance
      │                 │
      │                 ├── Gold
      │                 ├── DXY
      │                 ├── Silver
      │                 └── Crude Oil
      │
      ├──────────────► Tavily
      │                 │
      │                 └── Recent financial/news sources
      │
      ▼
Prompt Construction
      │
      ├── Market Data
      ├── News
      ├── User Question
      ├── Conversation History
      └── Response Mode
      │
      ▼
OpenRouter
      │
      ├── Primary LLM
      └── Fallback Models
      │
      ▼
AI-Generated Response
      │
      ▼
Streamlit Interface
```

---

# Features

## 1. Real-Time Market Data

The application retrieves recent market data through Yahoo Finance using `yfinance`.

The dashboard currently tracks:

| Asset             | Symbol     | Purpose                              |
| ----------------- | ---------- | ------------------------------------ |
| Gold Futures      | `GC=F`     | Main gold-market indicator           |
| US Dollar Index   | `DX-Y.NYB` | Measures dollar strength             |
| Silver Futures    | `SI=F`     | Related precious-metal indicator     |
| Crude Oil Futures | `CL=F`     | Broader commodity/economic indicator |

For each asset, the application displays:

* Current price
* Daily percentage change
* Weekly percentage change

Example:

```text
Gold

$4,365.20

🟢 Day: +0.75%
🟢 Week: +2.31%
```

The market-data functionality is implemented in:

```text
market_data.py
```

---

# 2. Gold Price Chart

The Streamlit dashboard provides an interactive gold-price chart.

Available periods include:

* 7 days
* 1 month
* 3 months
* 6 months
* 1 year

The chart uses Yahoo Finance data for:

```text
GC=F
```

The chart allows users to visually inspect recent gold-price movements before asking the AI analyst questions about the market.

---

# 3. Financial News Retrieval with Tavily

The application uses Tavily to retrieve recent information related to gold and the broader financial environment.

News searches cover topics such as:

* Gold prices
* Gold market developments
* Federal Reserve interest rates
* Inflation
* US Dollar Index
* Geopolitical tensions
* Other factors relevant to gold prices

The news retrieval system returns information including:

```text
Title
Content
URL
```

The retrieved information is then formatted and supplied to the LLM as part of the analysis context.

This allows the model to distinguish between:

```text
Historical/general knowledge
```

and:

```text
Recently retrieved market information
```

The news retrieval functionality is implemented in:

```text
news_fetcher.py
```

---

# 4. AI-Powered Market Analysis

The application uses OpenRouter to access large language models.

Instead of sending only the user's question to the model, the agent constructs a context-rich prompt containing:

* User question
* Current market data
* Recent news
* Conversation history
* Detected response mode
* Language information
* Analysis instructions

The main prompt construction is implemented in:

```text
prompts.py
```

The model communication and fallback system is implemented in:

```text
llm_analyzer.py
```

---

# 5. Multiple LLM Models and Fallback System

The application supports multiple OpenRouter models.

The purpose of the fallback system is to improve reliability when a free model or provider is temporarily unavailable.

The system can:

1. Try the primary model.
2. Detect temporary API/provider errors.
3. Retry the model when appropriate.
4. Place temporarily unavailable models on cooldown.
5. Move to another available model.
6. Continue until a model successfully generates a response.

The fallback architecture is particularly useful with free models because free-model providers may experience:

* Rate limits
* Temporary outages
* Provider capacity limitations
* HTTP 429 responses
* HTTP 5xx responses
* Temporary upstream errors

The model configuration is maintained in:

```text
config.py
```

while the fallback logic is handled by:

```text
llm_analyzer.py
```

---

# 6. Adaptive Simple and Detailed Response Modes

One of the main features of the application is its adaptive response mode.

The user does not need to manually select a response mode.

Instead, the application determines the desired depth from the wording of the question.

For example:

### Simple question

```text
What is the current gold price?
```

The application treats this as a simple request and aims to provide a concise response.

### Detailed question

```text
Analyze the current gold trend and explain the risks.
```

The application detects words such as:

```text
analysis
analyze
forecast
outlook
trend
risk
detailed
```

and switches to Detailed mode.

The system also supports Persian keywords such as:

```text
تحلیل
بررسی
چشم‌انداز
پیش‌بینی
روند
ریسک
کامل
```

This allows both English and Persian users to trigger deeper analysis naturally.

The same detection logic is used by the agent and displayed in the Streamlit interface.

---

# 7. Conversational Context

The agent maintains conversation history during the current application session.

The conversation history allows follow-up questions to make use of previous interactions.

For example:

```text
User:
What is happening with gold?

Assistant:
Gold has recently...

User:
What about the effect of the dollar?

Assistant:
The dollar is relevant because...
```

The second question can be interpreted in the context of the previous conversation.

Conversation management is handled by:

```text
agent.py
```

The agent maintains:

```python
self.chat_history
```

and sends the relevant conversation history to the LLM.

The application also provides a button to clear the current conversation.

---

# 8. Conversation Database

The project includes SQLite-based conversation storage.

The database is managed through:

```text
database.py
```

The application can save:

* User questions
* AI responses

The local database file is:

```text
chat_history.db
```

For security and repository hygiene, the database file should not be committed to GitHub.

It should therefore be included in `.gitignore`.

---

# 9. Bilingual Support

The application supports:

```text
English
Persian
```

The prompt system detects the language of the user's question and instructs the LLM to respond appropriately.

Persian questions can therefore be asked naturally, for example:

```text
قیمت طلا در هفته گذشته چه تغییری کرده است؟
```

or:

```text
روند قیمت طلا را تحلیل کن و عوامل مؤثر بر آن را توضیح بده.
```

---

# 10. Streamlit Dashboard

The project includes a dedicated Streamlit interface rather than exposing the agent only through a terminal.

The dashboard includes:

```text
Gold Market AI
│
├── Market Overview
│   ├── Gold
│   ├── US Dollar Index
│   ├── Silver
│   └── Crude Oil
│
├── Gold Price Chart
│
├── AI Market Analyst
│
├── Adaptive Response Mode
│
└── Conversation
```

The interface provides:

* Market overview cards
* Current prices
* Daily changes
* Weekly changes
* Gold price chart
* AI chat interface
* Response-mode indicator
* Conversation history
* Refresh functionality
* Conversation clearing

The main application entry point is:

```text
app.py
```

---

# Architecture

The project is divided into several components.

```text
gold-market-ai-agent/
│
├── app.py
│
├── agent.py
│
├── config.py
│
├── database.py
│
├── llm_analyzer.py
│
├── market_data.py
│
├── news_fetcher.py
│
├── prompts.py
│
├── requirements.txt
│
├── .gitignore
│
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

## `app.py`

The Streamlit user interface.

Responsibilities:

* Dashboard layout
* Market cards
* Gold chart
* Chat interface
* Response-mode display
* Conversation display
* Refresh controls

---

## `agent.py`

The main agent orchestration layer.

Responsibilities:

1. Receive the user's question.
2. Retrieve market data.
3. Retrieve recent news.
4. Determine Simple/Detailed mode.
5. Construct the analysis prompt.
6. Send the prompt to the LLM.
7. Maintain conversation history.

---

## `market_data.py`

Retrieves financial market information using Yahoo Finance.

Current indicators:

```text
GC=F
DX-Y.NYB
SI=F
CL=F
```

Each asset returns:

```python
{
    "price": ...,
    "daily_change_percent": ...,
    "weekly_change_percent": ...,
    "error": ...
}
```

---

## `news_fetcher.py`

Responsible for retrieving recent financial news using Tavily.

The retrieved results are converted into a format that can be inserted into the LLM prompt.

---

## `prompts.py`

Contains the system prompt and prompt-generation logic.

It controls:

* Financial-analysis behavior
* Language handling
* Market-data context
* News context
* Simple/Detailed response style
* Risk and uncertainty handling

---

## `llm_analyzer.py`

Handles communication with OpenRouter.

Responsibilities include:

* OpenRouter API communication
* Model selection
* Reasoning configuration
* Multiple-model fallback
* Retry handling
* Temporary model cooldowns
* API error handling

---

## `config.py`

Contains application configuration such as:

```text
OpenRouter configuration
Tavily configuration
Model list
Market symbols
Retry settings
News-result limits
Supported languages
Application disclaimer
```

API keys are loaded from environment variables or Streamlit secrets rather than being hard-coded into the application.

---

## `database.py`

Provides SQLite-based local conversation storage.

---

# Technology Stack

## Programming Language

* Python

## User Interface

* Streamlit

## Large Language Models

* OpenRouter

## Financial Data

* Yahoo Finance
* `yfinance`

## News Retrieval

* Tavily

## Database

* SQLite

## Environment Configuration

* `python-dotenv`
* Streamlit Secrets

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/parsasmt/gold-market-ai-agent.git
cd gold-market-ai-agent
```

Replace the repository URL above if the repository name or URL is different.

---

## 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# API Keys

The application requires API access for:

* OpenRouter
* Tavily

For local development, create:

```text
.env
```

and add:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit this file to GitHub.

Your `.gitignore` should contain:

```text
.env
.streamlit/secrets.toml
chat_history.db
__pycache__/
*.pyc
```

---

# Running the Application Locally

Start Streamlit with:

```powershell
streamlit run app.py
```

The application will normally become available at:

```text
http://localhost:8501
```

---

# Streamlit Deployment

The application can be deployed through Streamlit Community Cloud.

The basic deployment structure is:

```text
GitHub Repository
        │
        ▼
Streamlit Community Cloud
        │
        ▼
app.py
```

After connecting the GitHub repository, set the Streamlit secrets:

```toml
OPENROUTER_API_KEY = "your_openrouter_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
```

The application reads these values through Streamlit's secrets mechanism.

API keys should never be committed to the GitHub repository.

---

# Example Questions

## Current Market

```text
What is the current gold price?
```

```text
How much has gold changed this week?
```

```text
Compare gold with silver.
```

## Analysis

```text
Analyze the current gold trend.
```

```text
What are the main risks for gold right now?
```

```text
Give me a detailed outlook for gold.
```

## News

```text
What are some important news about gold recently?
```

```text
What happened in the gold market this week?
```

```text
What recent Federal Reserve news could affect gold?
```

## Persian

```text
قیمت فعلی طلا چقدر است؟
```

```text
روند قیمت طلا را تحلیل کن.
```

```text
مهم‌ترین اخبار هفته گذشته درباره طلا چه بوده است؟
```

---

# Example Agent Workflow

For a question such as:

```text
Analyze the recent gold trend and explain the main risks.
```

the application performs approximately the following sequence:

```text
1. Receive question
        ↓
2. Detect "analyze" and "risk"
        ↓
3. Activate Detailed mode
        ↓
4. Retrieve gold market data
        ↓
5. Retrieve DXY data
        ↓
6. Retrieve silver data
        ↓
7. Retrieve oil data
        ↓
8. Search recent financial news with Tavily
        ↓
9. Format market data and news
        ↓
10. Build analysis prompt
        ↓
11. Send prompt to OpenRouter
        ↓
12. Generate response
        ↓
13. Display response in Streamlit
        ↓
14. Save conversation
```

---

# Error Handling and Reliability

The application includes handling for several types of failures.

## Market Data Failure

If Yahoo Finance fails to return data, the application avoids crashing the entire dashboard and displays unavailable values where appropriate.

## News Retrieval Failure

If Tavily fails, the agent can continue operating with the available market information.

## LLM Failure

If an OpenRouter model returns a temporary error, the fallback system can retry and/or move to another configured model.

Temporary failures can include:

```text
HTTP 408
HTTP 409
HTTP 429
HTTP 500
HTTP 502
HTTP 503
HTTP 504
```

The model cooldown system helps prevent repeatedly sending requests to a temporarily unavailable provider.

---

# Project Design Goals

The project was designed around several principles:

### External Information Before Generation

The LLM should receive current information rather than relying exclusively on its pretrained knowledge.

### Tool-Augmented LLM

The model is used as the reasoning and language-generation component while external tools provide current information.

### Adaptive Interaction

The user does not need to configure the desired answer length manually. The wording of the question determines whether a simple or detailed response is appropriate.

### Provider Resilience

Multiple models can be configured so that temporary problems with one provider do not necessarily stop the entire application.

### Explainable Information Sources

Market information and news are retrieved from identifiable external sources rather than being treated as facts generated entirely by the LLM.

---

# Limitations

This application has several important limitations.

## Market Data

Yahoo Finance data availability and update frequency can vary.

The application should therefore not be considered a professional trading terminal.

## News

News retrieval depends on the search results returned by Tavily. Search coverage, indexing, publication dates, and source availability can affect the results.

## LLM Responses

LLMs can produce incorrect interpretations, misunderstand retrieved information, or generate unsupported conclusions.

Retrieved information should therefore be checked against the original sources when accuracy is important.

## Financial Predictions

The application does not guarantee future gold prices or market movements.

Its responses are intended for informational and educational use.

## Database Persistence

The local SQLite database is suitable for local development and demonstrations. For a production multi-user deployment, a persistent external database would be more appropriate.

---

# Security

Never commit API credentials to GitHub.

Sensitive files should remain local:

```text
.env
.streamlit/secrets.toml
```

A suitable `.gitignore` is:

```text
.env
.streamlit/secrets.toml
chat_history.db
__pycache__/
*.pyc
```

If an API key is accidentally committed to GitHub, revoke it and generate a new key immediately.

---

# Future Improvements

Potential future development includes:

* Historical gold-price analysis
* More financial indicators
* Treasury-yield integration
* Inflation and CPI data
* Federal Reserve data integration
* More advanced news ranking
* News deduplication
* Source/date display in the UI
* Persistent cloud database
* User authentication
* Portfolio tracking
* More advanced charting
* Technical indicators
* Automatic report generation
* Scheduled market summaries
* More sophisticated agent/tool selection
* Evaluation of LLM response quality
* Automated testing and benchmarking

---

# Project Structure

```text
Gold Market AI Agent
│
├── User Interface
│   └── Streamlit
│
├── Agent Layer
│   └── agent.py
│
├── Data Layer
│   ├── market_data.py
│   └── news_fetcher.py
│
├── LLM Layer
│   ├── prompts.py
│   └── llm_analyzer.py
│
├── Storage Layer
│   └── database.py
│
└── Configuration
    └── config.py
```

---

# License

This project is intended for educational and research purposes.

If a specific open-source license is added to the repository, this section should be updated accordingly.

---

# Acknowledgments

This project makes use of:

* Streamlit for the web application interface
* Yahoo Finance through `yfinance` for financial market data
* Tavily for web/news retrieval
* OpenRouter for access to large language models
* SQLite for local conversation storage

---

# Author

Parsa Esmatloo

GitHub:

https://github.com/parsasmt

---

## Disclaimer

This project provides automatically generated financial information and analysis for educational and informational purposes only.

It is not financial, investment, trading, legal, or professional advice. Market data and news may contain delays, inaccuracies, omissions, or errors. Users should independently verify important information and consult qualified professionals before making financial decisions.
