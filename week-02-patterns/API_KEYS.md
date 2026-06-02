# API keys — get them free, and where to put them

The notebooks run on **Google Gemini's free tier** — no credit card, no cost for the workshop. You need **one** key (Gemini). Two more are **optional**, only for the "from demo to production" parts (real web search + tracing).

| Key | Colab Secret name | Get it (free) | Free tier | Used for |
|---|---|---|---|---|
| **Google Gemini** ✅ required | `GOOGLE_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Free, no credit card | The LLM in every notebook |
| **Tavily** *(optional)* | `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) | 1,000 searches/month, no card | Real web search (NB02 "production" note) |
| **LangSmith** *(optional)* | `LANGCHAIN_API_KEY` | [smith.langchain.com](https://smith.langchain.com) | Free Developer plan, no card | Tracing/observability (NB02 "production" note) |

---

## How Colab reads your keys (the 🔑 Secrets panel)

You never paste a key into a cell. Instead you store it once in Colab's **Secrets** vault, and the notebook reads it.

1. Open any notebook in Colab.
2. Click the **🔑 key icon** in the **left sidebar** → **Secrets**.
3. Click **+ Add new secret**.
4. **Name** = the secret name from the table above (e.g. `GOOGLE_API_KEY`). **Value** = your key.
5. Toggle **Notebook access** ON for that secret.

The first code cell of every notebook then loads it automatically:

```python
import os
from google.colab import userdata
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
```

That's it — add the secret once, and every cell can use it. (Running locally instead of Colab? Put the same names in a `.env` file next to the notebook; the cell falls back to `python-dotenv` automatically.)

---

## 1. Google Gemini — required, free ✅

1. Go to **[aistudio.google.com/apikey](https://aistudio.google.com/apikey)** and sign in with a Google account.
2. Click **Create API key** (you can use a new project). Copy the key — it starts with `AIza…`.
3. In Colab: 🔑 Secrets → **+ Add new secret** → Name **`GOOGLE_API_KEY`**, paste the value, enable Notebook access.

That single key powers all four notebooks. The free tier is generous for a workshop (rate-limited, so a heavy notebook may pause briefly between calls — that's normal).

> No credit card is required. Keys are personal — don't paste them into chats or commit them to git.

## 2. Tavily — optional (real web search)

The notebooks **mock** `web_search` so they run offline. To use a real, agent-grade search instead:

1. Sign up at **[app.tavily.com](https://app.tavily.com)** (free, no card — **1,000 searches/month**).
2. Copy your API key from the dashboard.
3. Colab: 🔑 Secrets → Name **`TAVILY_API_KEY`**, paste, enable access.
4. Then the drop-in is:

```python
# %pip install -q langchain-community tavily-python
import os
os.environ["TAVILY_API_KEY"] = userdata.get("TAVILY_API_KEY")
from langchain_community.tools.tavily_search import TavilySearchResults
real_search = TavilySearchResults(max_results=3)   # replaces the mocked web_search
```

## 3. LangSmith — optional (see every agent step)

LangSmith traces each Thought → Action → tool call, with latency and token counts — no code change, just two env vars.

1. Sign up at **[smith.langchain.com](https://smith.langchain.com)** (free Developer plan, no card).
2. **Settings → API Keys → Create API Key**. Copy it (starts with `lsv2_…`).
3. Colab: 🔑 Secrets → Name **`LANGCHAIN_API_KEY`**, paste, enable access.
4. Turn tracing on near the top of a notebook:

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"]   = userdata.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]   = "agentic-ai-week2"   # optional: names the trace project
```

Run any agent, then open your project at [smith.langchain.com](https://smith.langchain.com) to watch the trace.

---

## Prefer a different LLM? (optional)

Everything is LangChain, so swapping providers is one line — though you'd add that provider's key and `pip install` its package:

```python
# Gemini (default in these notebooks):
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Anthropic Claude (needs ANTHROPIC_API_KEY + `pip install langchain-anthropic`):
# from langchain_anthropic import ChatAnthropic
# llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)
```
