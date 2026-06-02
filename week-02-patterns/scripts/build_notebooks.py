"""Build the Week 2 notebooks from a single source-of-truth Python script.

Generates valid .ipynb JSON. Run from week-02-patterns/scripts/:
    python build_notebooks.py

Outputs to ../notebooks/:
    00_langchain_intro.ipynb
    01_tool_use.ipynb
    02_react_agent.ipynb
    03_rag_pipeline.ipynb
    04_rag_elasticsearch_appendix.ipynb

Target stack (classic LangChain 0.3.x line — last series with AgentExecutor +
create_react_agent before the LangGraph-only v1.0). Provider: Google Gemini (free tier).
"""
from __future__ import annotations

import json
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "notebooks"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-2.5-flash"  # free-tier Gemini flash model — fast, good tool use, no card needed


def md(text: str) -> dict:
    """Markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": _split(text)}


def code(text: str) -> dict:
    """Code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _split(text),
    }


def _split(text: str) -> list[str]:
    """Split text into lines preserving newlines, as Jupyter expects."""
    return text.splitlines(keepends=True)


def write(name: str, cells: list[dict]) -> None:
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11",
            },
            "colab": {"provenance": []},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (OUT_DIR / name).write_text(json.dumps(nb, indent=1))
    print(f"  wrote {OUT_DIR / name}")


# Shared key-loading cell (Colab userdata OR local .env). Reused across notebooks.
KEY_CELL = """import os

# Free Gemini API key (no credit card): https://aistudio.google.com/apikey
# Colab: add GOOGLE_API_KEY under the key icon (left sidebar) -> "Secrets".
# Local: put GOOGLE_API_KEY=AIza... in a .env file next to this notebook.
try:
    from google.colab import userdata  # type: ignore
    os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()

assert os.environ.get("GOOGLE_API_KEY"), "Set GOOGLE_API_KEY first (see the comment above)."
print("API key loaded.")
"""


# ============================================================================
# NOTEBOOK 00 — LangChain in 15 minutes
# ============================================================================

NB00 = [
    md("""# Notebook 00 — LangChain in 15 Minutes

**Workshop:** Agentic AI for Scientists — Week 2
**Block:** warm-up (15 min)
**Goal:** Learn the five LangChain pieces every later notebook leans on — *model wrapper, messages, prompt templates, output parsers, and the LCEL pipe* — plus a first look at **tools**. Nothing here is an "agent" yet. This is the vocabulary.

**The one-sentence version of LangChain:** it is a thin, vendor-neutral standard layer over "call an LLM, give it a prompt, maybe give it tools, parse what comes back." You can do all of it with raw SDK calls (we will, in Notebook 01). LangChain's value is that the *same code* works across Anthropic, OpenAI, Google, etc., and that chains/agents/retrievers snap together with one operator: `|`.
"""),

    md("## 0. Setup\n\nInstall the two packages we need for the intro, then load your API key."),

    code("""%pip install -q "langchain==0.3.7" "langchain-google-genai==2.0.11" python-dotenv
"""),

    code(KEY_CELL),

    md("""---

## 1. The model wrapper

`ChatGoogleGenerativeAI` is a *wrapper* around the Gemini API. The point of the wrapper: every chat model in LangChain — Gemini, Anthropic, OpenAI — exposes the **same** `.invoke()` method. Swap the class, keep the code.
"""),

    code(f"""from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="{MODEL}", temperature=0)

response = llm.invoke("In one sentence, what is an AI agent?")
print(type(response).__name__)   # AIMessage
print(response.content)
"""),

    md("""`llm.invoke(...)` returns an **`AIMessage`** object, not a bare string. The text is in `.content`; token counts and stop reasons live in `.response_metadata`. That object-not-string detail matters once we start chaining.

---

## 2. Messages

A chat model's real input is a *list of messages*, each with a role. LangChain gives you typed message classes. A `SystemMessage` sets behaviour; `HumanMessage` is the user turn; `AIMessage` is the model's reply (you append these to build multi-turn history).
"""),

    code("""from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="You are a terse research assistant. Answer in <= 12 words."),
    HumanMessage(content="What is retrieval-augmented generation?"),
]
print(llm.invoke(messages).content)
"""),

    md("""---

## 3. Prompt templates

Hard-coding prompts is fine until you need to reuse one with different inputs. `ChatPromptTemplate` is a prompt with `{placeholders}` you fill at call time.
"""),

    code("""from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {field}. Explain for a curious non-expert."),
    ("human", "Explain {concept} in 2 sentences."),
])

# .invoke fills the template and returns a list of messages
filled = prompt.invoke({"field": "machine learning", "concept": "embeddings"})
for m in filled.messages:
    print(f"[{m.type}] {m.content}")
"""),

    md("""---

## 4. Output parsers + the LCEL pipe

The big idea. LangChain Expression Language (**LCEL**) lets you connect components with `|`, exactly like a Unix pipe. Data flows left to right:

```
prompt  |  llm  |  parser
 dict   ->  messages -> AIMessage -> str
```

`StrOutputParser` just pulls `.content` out of the `AIMessage` so the chain returns a plain string.
"""),

    code("""from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()

answer = chain.invoke({"field": "biology", "concept": "a transformer model"})
print(answer)
"""),

    md("""That three-component chain is the spine of everything in LangChain. A RAG chain (Notebook 03) is the same pipe with a retriever bolted on the front. An agent (Notebooks 01–02) is the same pipe wrapped in a loop.

LCEL chains also come with `.batch()` and `.stream()` for free:
"""),

    code("""# Run several inputs in one call
for out in chain.batch([
    {"field": "physics", "concept": "entropy"},
    {"field": "chemistry", "concept": "a catalyst"},
]):
    print("-", out, "\\n")
"""),

    md("""---

## 5. Tools — a first look

A **tool** is a plain Python function the model is allowed to call. The `@tool` decorator wraps a function so LangChain can read its name, its docstring (the description the model sees), and its typed arguments (the schema the model fills in).
"""),

    code("""from langchain_core.tools import tool

@tool
def word_count(text: str) -> int:
    \"\"\"Count the number of words in a piece of text.\"\"\"
    return len(text.split())

# The decorator turned the function into a Tool with metadata the model reads:
print("name:       ", word_count.name)
print("description:", word_count.description)
print("args schema:", word_count.args)

# You can still call it like a normal function:
print("result:     ", word_count.invoke({"text": "agents are loops around a model"}))
"""),

    md("""Three things the model needs are now machine-readable: **what the tool is called**, **what it does** (docstring), and **what arguments it takes** (type hints). That is the entire contract behind "function calling".

---

## 6. Where this is going

You now have the whole toolbox:

| Piece | Class | One-liner |
|---|---|---|
| Model wrapper | `ChatGoogleGenerativeAI` | vendor-neutral `.invoke()` |
| Messages | `SystemMessage` / `HumanMessage` / `AIMessage` | typed chat turns |
| Prompt template | `ChatPromptTemplate` | a prompt with `{slots}` |
| Output parser | `StrOutputParser` | `AIMessage` -> `str` |
| Chain | `prompt | llm | parser` | the LCEL pipe |
| Tool | `@tool` | a function the model can call |

An **agent** is just: *give the model some tools, let it pick one, run it, feed the result back, and loop until it's done.* That loop is the only new idea in the next two notebooks — and we build it by hand before letting LangChain hide it.

**Next:** [Notebook 01 — Tool Use & Function Calling](01_tool_use.ipynb)
"""),
]


# ============================================================================
# NOTEBOOK 01 — Tool Use & Function Calling
# ============================================================================

NB01 = [
    md("""# Notebook 01 — Tool Use & Function Calling

**Workshop:** Agentic AI for Scientists — Week 2
**Block:** 2 of 6 (25 min)
**Goal:** Convince yourself that "tool use" is an `if model_response.has_tool_call: run_tool(...)` line inside a `while` loop. No magic.

We build the same tiny agent **three** times, each less code than the last:

1. **Hand-rolled.** LLM call + a regex + a Python function. No SDK helpers — you see every moving part.
2. **Gemini native function-calling.** Same control flow, but the model emits typed function-call parts so we stop parsing text.
3. **LangChain tool-calling agent.** The whole loop collapses to `AgentExecutor.invoke(...)`. This is the **function-calling agent** from the lecture — tool selection is shifted to the model vendor.

Seeing all three back-to-back is the point: when a framework hides the loop, you'll know exactly what it hid.
"""),

    md("## 0. Setup"),

    code("""%pip install -q "google-genai>=1.0" \\
    "langchain==0.3.7" "langchain-google-genai==2.0.11" python-dotenv
"""),

    code(KEY_CELL),

    code(f"""import re
from google import genai
from google.genai import types

client = genai.Client()        # reads GOOGLE_API_KEY from the environment
MODEL = "{MODEL}"


def show(turn: str, content: str) -> None:
    \"\"\"Pretty-print one turn of the conversation.\"\"\"
    print(f"\\n--- {{turn}} ---")
    print(content)


def as_text(output) -> str:
    \"\"\"An AgentExecutor result["output"] is a plain string for both ReAct and the
    Gemini tool-calling agent. Tiny normaliser, kept in case a model returns parts.\"\"\"
    if isinstance(output, str):
        return output
    return "".join(getattr(b, "text", "") or "" for b in output)


print(f"Ready with model: {{MODEL}}")
"""),

    md("""---

## 1. Define a tool — plain Python, no schema

A "tool" is just a function the model can ask you to call. Nothing more.
"""),

    code("""def calculator(expression: str) -> str:
    \"\"\"Evaluate a basic arithmetic expression and return the result as a string.\"\"\"
    expression = expression.replace("^", "**")   # models often write ^ for "to the power of"
    if not re.fullmatch(r"[\\d\\s+\\-*/().]+", expression):
        return "ERROR: only basic arithmetic allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"ERROR: {exc}"


print(calculator("(17 + 25) * 3"))
"""),

    md("""---

## 2. Hand-built tool loop (no SDK helpers)

We tell the model: *"If you need math, output `CALL: calculator(<expression>)`. Otherwise answer directly."* Then we parse the response ourselves and loop.

This is the entire substance of tool use. Frameworks add type safety, JSON schemas, and retries — but the control flow is exactly this.
"""),

    code("""SYSTEM_PROMPT_MANUAL = \"\"\"You are a helpful research assistant.

You have access to ONE tool: a calculator.

To use the calculator, output EXACTLY this on its own line:
CALL: calculator(<expression>)

For example: CALL: calculator(17 * 25)

The user will run the calculation and reply with the result. Then continue your answer.
If you don't need the calculator, just answer directly.\"\"\"


def run_manual_loop(user_question: str, max_turns: int = 5) -> str:
    contents = [types.Content(role="user", parts=[types.Part(text=user_question)])]
    show("USER", user_question)

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT_MANUAL, max_output_tokens=1024)

    for turn in range(max_turns):
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config,
        )
        assistant_text = response.text
        show(f"ASSISTANT (turn {turn + 1})", assistant_text)

        # Parse the text ourselves to find a tool call
        match = re.search(r"CALL:\\s*calculator\\((.+?)\\)", assistant_text)
        if not match:
            return assistant_text  # no tool needed -> done

        expression = match.group(1).strip()
        result = calculator(expression)
        show("TOOL RESULT", f"{expression} = {result}")

        # Feed the tool result back and let the model continue.
        # Gemini's roles are "user" and "model" (not "assistant").
        contents.append(types.Content(role="model", parts=[types.Part(text=assistant_text)]))
        contents.append(types.Content(role="user",
            parts=[types.Part(text=f"Tool result: {result}\\n\\nContinue your answer.")]))

    return "Max turns reached without final answer."


final = run_manual_loop(
    "A bacterial colony doubles every 20 minutes. Starting with 500 cells, "
    "how many cells after 3 hours? Show the calculation."
)
print("\\n=== FINAL ANSWER ===")
print(final)
"""),

    md("""**What just happened?**

1. We sent the question to the LLM.
2. The LLM responded with `CALL: calculator(500 * 2**9)` (or similar) — a *text* response we agreed to interpret.
3. We parsed that text with a regex, ran the Python function, captured the result.
4. We appended the result back as a `user` message and re-prompted.
5. The LLM read the result and produced a final answer.

That is the whole pattern: **the loop is a Python `for`, the tool is a function, the agent is the LLM-plus-loop together.** Everything after this is removing the fragile parts.

---

## 3. Same thing with Gemini's native function-calling API

The hand-rolled version works but is brittle (regex parsing, prompt instructions, injection risk). Gemini's typed function-call parts give the same control flow with parsing handled for us.
"""),

    code("""# Tool schema as a Gemini FunctionDeclaration. The model sees this and emits
# typed function-call parts instead of free text we have to regex.
calculator_decl = types.FunctionDeclaration(
    name="calculator",
    description="Evaluate a basic arithmetic expression. Use whenever a calculation is needed.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "expression": types.Schema(
                type="STRING",
                description="A math expression using digits, +, -, *, /, parens, dots.",
            ),
        },
        required=["expression"],
    ),
)
TOOLS = [types.Tool(function_declarations=[calculator_decl])]

# Map name -> Python callable. This is your "tool registry".
TOOL_REGISTRY = {"calculator": calculator}
"""),

    code("""def run_native_loop(user_question: str, max_turns: int = 5) -> str:
    contents = [types.Content(role="user", parts=[types.Part(text=user_question)])]
    show("USER", user_question)
    config = types.GenerateContentConfig(tools=TOOLS)

    for turn in range(max_turns):
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config,
        )
        parts = response.candidates[0].content.parts
        text_parts = [p.text for p in parts if getattr(p, "text", None)]
        calls = [p.function_call for p in parts if getattr(p, "function_call", None)]

        if text_parts:
            show(f"ASSISTANT (turn {turn + 1})", "\\n".join(text_parts))
        if not calls:
            return "\\n".join(text_parts)

        # Append the model's full turn, then run each requested function and
        # send the results back as function_response parts.
        contents.append(types.Content(role="model", parts=parts))
        result_parts = []
        for call in calls:
            args = dict(call.args)
            result = TOOL_REGISTRY[call.name](**args)
            show(f"TOOL {call.name}({args})", str(result))
            result_parts.append(types.Part.from_function_response(
                name=call.name, response={"result": str(result)}))
        contents.append(types.Content(role="user", parts=result_parts))

    return "Max turns reached."


final = run_native_loop(
    "A bacterial colony doubles every 20 minutes. Starting with 500 cells, "
    "how many cells after 3 hours? Show the calculation."
)
print("\\n=== FINAL ANSWER ===")
print(final)
"""),

    md("""**What changed?**

| | Hand-rolled | Native function-calling |
|---|---|---|
| Tool definition | Python function + prompt instructions | Python function + JSON schema |
| Parsing | Regex on response text | SDK gives you typed function-call parts |
| Loop | `for` loop | same `for` loop |
| Injection risk | Higher (model could fake a `CALL:` mid-text) | Lower (tool blocks are structurally separate) |
| Type safety | None | JSON Schema validates inputs |

**The control flow is identical.** Only the parsing got safer.

---

## 4. Same thing again, with LangChain — the *tool-calling agent*

Now we let LangChain own the loop. This is the **function-calling agent**: we hand the model a set of tools, and the *model vendor* decides which tool to call with which arguments. We supply the tools and the loop runs itself.
"""),

    code("""from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

llm = ChatGoogleGenerativeAI(model=MODEL, temperature=0)


# @tool reads the type hints + docstring to build the schema automatically.
@tool
def calc(expression: str) -> str:
    \"\"\"Evaluate a basic arithmetic expression like '500 * 2 ** 9'.\"\"\"
    return calculator(expression)


@tool
def get_weather(city: str) -> str:
    \"\"\"Get the current weather for a city. Returns a short description.\"\"\"
    # Mock implementation so the notebook runs offline.
    fake = {"singapore": "31C, humid, afternoon thunderstorms likely",
            "london": "12C, overcast, light rain"}
    return fake.get(city.lower().strip(), f"No weather data for {city}")


lc_tools = [calc, get_weather]

# The tool-calling prompt MUST include an agent_scratchpad MessagesPlaceholder.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant. Use tools when they help."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),   # where the loop's tool calls/results accumulate
])

agent = create_tool_calling_agent(llm, lc_tools, prompt)
executor = AgentExecutor(agent=agent, tools=lc_tools, verbose=True, max_iterations=5)

result = executor.invoke({
    "input": "Should I bring an umbrella in Singapore today? Also, if a 5 mm umbrella "
             "doubled in size every hour, how big after 4 hours?",
})
print("\\n=== FINAL ANSWER ===")
print(as_text(result["output"]))   # Gemini's tool-calling agent returns a plain string
"""),

    md("""Watch the `verbose=True` trace: the agent called `get_weather('Singapore')` **and** `calc('5 * 2 ** 4')`, then composed both results into one answer — and we never wrote a loop. That loop is the same `for` from sections 2 and 3, now living inside `AgentExecutor.invoke`.

**Where the responsibility went.** With the tool-calling agent, *which* tool to call and *what arguments* to pass is decided by the model (a capability the vendor fine-tuned and serves). Our job shrinks to two things: write tools with **unambiguous names and descriptions**, and register them. This is a shared-responsibility model — the vendor picks the tool, but only as well as your descriptions let it.

---

## 5. Structured output — function calling, aimed at the answer

The same function-calling machinery has a twin. Instead of pointing a schema at a *tool*, point it at the **answer**: define the exact shape you want back as a Pydantic model, and the model fills it in. You get a typed, validated Python object — not a string you have to parse. This is how you make an agent's output safe to feed into the next step of a pipeline.
"""),

    code("""from pydantic import BaseModel, Field
from typing import Literal


class ClaimCheck(BaseModel):
    \"\"\"A structured verdict about a factual claim.\"\"\"
    verdict: Literal["true", "false", "uncertain"] = Field(description="Is the claim correct?")
    confidence: Literal["low", "medium", "high"]
    reason: str = Field(description="A short justification, <= 15 words.")


# .with_structured_output binds the schema to the model via function calling.
checker = llm.with_structured_output(ClaimCheck)

result = checker.invoke(
    "Claim: the Transformer paper 'Attention Is All You Need' was published in 2017."
)
print(type(result).__name__)            # ClaimCheck — a real Python object, not a string
print("verdict   :", result.verdict)
print("confidence:", result.confidence)
print("reason    :", result.reason)
"""),

    md("""No regex, no JSON parsing, no "please respond in JSON" prompt-begging. `result` is a validated `ClaimCheck` object — `result.verdict` is *guaranteed* to be one of the three literals or the call fails loudly. Under the hood it's the **same** function-calling mechanism as the tool-calling agent, which is why both live in this notebook: one fills a tool's arguments, the other fills your answer's fields.

---

## 6. Closing exercises (for after class)

1. **Add a third tool** — `convert_units(value: float, from_unit: str, to_unit: str)`. Notice that the `@tool` decorator turns the three typed arguments into a schema with no extra work. Ask a question that needs all three tools.
2. **Break it on purpose.** Give two tools nearly identical descriptions ("does math" / "computes numbers"). Does the agent still pick correctly? This is why description quality beats prompt length in agent-land.
3. **Typed extraction.** Make `ClaimCheck` hold a `list` of verdicts, then ask the model to pull every claim out of a paragraph and check each one. The result drops straight into Python with no parsing.

---

**Next:** [Notebook 02 — ReAct, Chain-of-Thought & Tree-of-Thoughts](02_react_agent.ipynb)
"""),
]


# ============================================================================
# NOTEBOOK 02 — ReAct, CoT, ToT
# ============================================================================

NB02 = [
    md("""# Notebook 02 — ReAct, Chain-of-Thought & Tree-of-Thoughts

**Workshop:** Agentic AI for Scientists — Week 2
**Block:** 3 of 6 (30 min)
**Goal:** Understand the *reasoning* patterns behind agents. We go in the order the ideas were invented:

1. **Chain-of-Thought (CoT)** — make the model think out loud. One prompt, no tools.
2. **ReAct** — interleave that thinking with **actions** (tool calls). We build the loop by hand, then collapse it to LangChain's `create_react_agent`.
3. **Tree-of-Thoughts (ToT)** — don't commit to the first chain of reasoning; branch, evaluate, and search.
4. **ReAct vs the tool-calling agent** — the two ways a model can pick a tool, and who carries the responsibility.

**Why this order matters:** if your first exposure to ReAct is `agent = create_react_agent(...)`, you'll think the framework does the reasoning. It doesn't. The reasoning lives in a prompt — and that prompt is just Chain-of-Thought with two extra keywords.
"""),

    md("## 0. Setup"),

    code("""%pip install -q "google-genai>=1.0" \\
    "langchain==0.3.7" "langchain-google-genai==2.0.11" "langchain-community==0.3.5" python-dotenv
"""),

    code(KEY_CELL),

    code(f"""import re
from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI

client = genai.Client()                                        # raw SDK, for the hand-built ReAct loop
llm = ChatGoogleGenerativeAI(model="{MODEL}", temperature=0)   # LangChain wrapper, for create_react_agent etc.
MODEL = "{MODEL}"


def as_text(output) -> str:
    \"\"\"AgentExecutor output is a plain string for both ReAct and Gemini's
    tool-calling agent. Tiny normaliser, kept for safety.\"\"\"
    if isinstance(output, str):
        return output
    return "".join(getattr(b, "text", "") or "" for b in output)


print(f"Ready with model: {{MODEL}}")
"""),

    md("""---

## 1. Chain-of-Thought — the seed of every reasoning agent

CoT (Wei et al., 2022) is almost embarrassingly simple: ask the model to **show its reasoning before answering**. On multi-step problems this alone lifts accuracy a lot, because the model uses its own intermediate tokens as a scratchpad.

Watch a model answer the same question two ways.
"""),

    code("""Q = ("A juggler has 16 balls. Half of the balls are golf balls, and half of the "
     "golf balls are blue. How many blue golf balls are there?")

# (a) Direct — force a bare answer
direct = llm.invoke(Q + " Reply with ONLY the final number.").content
print("DIRECT:", direct)

# (b) Chain-of-Thought — five magic words
cot = llm.invoke(Q + " Let's think step by step.").content
print("\\nCHAIN-OF-THOUGHT:\\n", cot)
"""),

    md("""The phrase *"Let's think step by step"* is the entire trick of **zero-shot CoT**. The model spends tokens decomposing `16 -> 8 golf balls -> 4 blue` before answering. No framework, no tools — just a prompt that elicits reasoning.

**ReAct is this idea plus one move:** let some of those reasoning steps reach out and *act* on the world (call a tool), then read the result back. So `ReAct = Reason + Act = CoT interleaved with tool calls`.

---

## 2. The ReAct prompt template — verbatim

ReAct (Yao et al., 2022) is a *prompting pattern*, not an API. Read it carefully — this is the whole mechanism.
"""),

    code("""REACT_PROMPT = \"\"\"Answer the following question as best you can. You have access to these tools:

{tools_description}

Use the following format, EXACTLY:

Question: the input question you must answer
Thought: your reasoning about what to do next
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation loop can repeat several times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {question}
{scratchpad}\"\"\"

print(REACT_PROMPT)
"""),

    md("""Notice the format names the three moving parts of every agent step: **Thought** (the CoT bit), **Action + Action Input** (the tool call), **Observation** (the result fed back). The model writes this text; *we* parse it and run the tools. That's why it's a pattern, not a framework.

---

## 3. Define three tools

Mock implementations so the notebook runs offline and the trace is reproducible. In production, swap each body for a real API call.
"""),

    code("""def web_search(query: str) -> str:
    \"\"\"Mock web search. Keyword-matched (not exact-phrase) so it answers the model's
    query however it phrases it — keeps the classroom trace clean and reproducible.\"\"\"
    q = query.lower()
    if "react" in q and any(w in q for w in ("author", "wrote", "who")):
        return "Yao et al., ICLR 2023 (arXiv:2210.03629)."
    if "transformer" in q and any(w in q for w in ("year", "publish", "when", "date")):
        return "'Attention Is All You Need' (the transformer paper) was published in 2017 by Vaswani et al."
    if "anthropic" in q and any(w in q for w in ("found", "start", "when")):
        return "Anthropic was founded in 2021 by Dario and Daniela Amodei."
    return f"No results for: {query}"


def calculator(expression: str) -> str:
    expression = expression.replace("^", "**")   # models often write ^ for "to the power of"
    if not re.fullmatch(r"[\\d\\s+\\-*/().]+", expression):
        return "ERROR: only basic arithmetic allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"ERROR: {exc}"


def fetch_paper_abstract(arxiv_id: str) -> str:
    \"\"\"Mock paper-abstract lookup. Real version would hit the arXiv API.\"\"\"
    canned = {
        "2210.03629": "ReAct: a paradigm that interleaves reasoning traces and task-specific "
                      "actions in language models for better synergy between the two.",
        "1706.03762": "Attention Is All You Need: the Transformer, a model architecture relying "
                      "entirely on attention, dispensing with recurrence and convolutions.",
    }
    return canned.get(arxiv_id.strip(), f"No abstract found for arXiv:{arxiv_id}")


TOOLS = {
    "web_search": (web_search, "Search the web. Input: a search query string."),
    "calculator": (calculator, "Do arithmetic. Input: a math expression like '2 + 2'."),
    "fetch_paper_abstract": (fetch_paper_abstract, "Get a paper abstract. Input: an arXiv ID like '2210.03629'."),
}
"""),

    md("""**In production, the mocks become real tools.** Swap `web_search` for a hosted search API built for agents — like **Tavily** — and the tool *interface* stays identical; only the body changes:

```python
# pip install tavily-python   (needs TAVILY_API_KEY)
from langchain_community.tools.tavily_search import TavilySearchResults
real_search = TavilySearchResults(max_results=3)   # drop-in replacement for web_search
```

Everything below runs the same whether the search is mocked or real — that interchangeability is the point of a clean tool interface.
"""),

    md("""---

## 4. Hand-built ReAct loop

Parse the model's Thought/Action/Action Input lines, run the action, append the Observation, re-prompt. Stop when we see `Final Answer:`. **This is the agent.**
"""),

    code("""def format_tools_for_prompt(tools: dict) -> tuple[str, str]:
    desc = "\\n".join(f"- {name}: {d}" for name, (_, d) in tools.items())
    return desc, ", ".join(tools.keys())


def parse_action(text: str):
    \"\"\"Extract (action_name, action_input) from the model's latest output, or None.\"\"\"
    m = re.search(
        r"Action:\\s*([\\w_]+)\\s*[\\r\\n]+Action Input:\\s*(.+?)(?=[\\r\\n]+(?:Observation|Thought|Final Answer)|$)",
        text, re.DOTALL,
    )
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip().strip('"').strip("'")


def run_react(question: str, max_iterations: int = 6) -> str:
    tools_description, tool_names = format_tools_for_prompt(TOOLS)
    scratchpad = ""

    for step in range(max_iterations):
        prompt = REACT_PROMPT.format(
            tools_description=tools_description, tool_names=tool_names,
            question=question, scratchpad=scratchpad,
        )
        # stop_sequences halts the model right after it writes "Action Input",
        # BEFORE it hallucinates its own Observation. WE supply the observation.
        # thinking_budget=0 stops gemini-2.5-flash from adding hidden reasoning
        # that would otherwise swallow the stop sequence and muddy the trace.
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1024,
                stop_sequences=["\\nObservation:"],
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        text = response.text
        print(f"\\n--- STEP {step + 1} ---")
        print(text)

        if "Final Answer:" in text:
            return text.split("Final Answer:", 1)[1].strip()

        parsed = parse_action(text)
        if not parsed:
            return f"PARSE ERROR: could not extract an action from:\\n{text}"

        action, action_input = parsed
        tool_fn, _ = TOOLS[action]
        observation = tool_fn(action_input)        # <-- run the tool
        print(f"\\nObservation: {observation}")     # <-- feed the result back

        scratchpad += text + f"\\nObservation: {observation}\\n"

    return "Max iterations reached without final answer."


answer = run_react(
    "Who wrote the ReAct paper, and what year was the transformer paper published? "
    "Then compute the difference in years."
)
print("\\n=== FINAL ANSWER ===")
print(answer)
"""),

    md("""**Read the trace top to bottom.** You'll see the loop turn, one tool at a time:

```
Thought: I need the authors of the ReAct paper first.
Action: web_search
Action Input: react paper authors
Observation: Yao et al., ICLR 2023 ...
Thought: Now the transformer year.
Action: web_search
Action Input: transformer paper year
Observation: ... 2017 ...
Thought: Difference is 2023 - 2017.
Action: calculator
Action Input: 2023 - 2017
Observation: 6
Thought: I now know the final answer
Final Answer: ...
```

That structure — **Thought -> Action -> Observation, repeat** — *is* ReAct. The `stop_sequences=["\\nObservation:"]` trick is the one subtlety: we stop the model the instant it asks for a tool, so it can't make up the tool's output. The real output is whatever our Python returns.

---

## 5. Watch the reasoning in LangSmith

[LangSmith](https://smith.langchain.com) records every model call — the prompt, the output, latency, token counts — as a trace you can expand. There are two ways to wire it, and we use the robust one:

- **(a) Wrap the raw Gemini client** with `langsmith.wrappers.wrap_gemini`. Every `generate_content` call traces directly, **independent of LangChain versions**. We wrap the same `client` our hand-built ReAct loop already uses, so each reasoning step shows up as its own trace. This is the reliable path on Colab.
- **(b) LangChain's own tracer** for `create_react_agent`, which gives a single *nested* trace tree. Prettier, but version-sensitive — classic LangChain 0.3.x only talks to older `langsmith`, so on Colab it sometimes silently posts nothing. We show it last, with the caveat.

**First, turn on tracing.** Add `LANGCHAIN_API_KEY` as a Colab Secret (free key: smith.langchain.com -> Settings -> API Keys), then run the cell below. No key? It just stays off and everything still runs.
"""),

    code("""# Optional LangSmith tracing. Safe to run with no key — tracing just stays off.
import os

def _secret(*names):
    \"\"\"Return the first of these names found in Colab Secrets or the environment.\"\"\"
    for n in names:
        try:
            from google.colab import userdata  # type: ignore
            v = userdata.get(n)
            if v:
                return v
        except Exception:
            pass
        if os.environ.get(n):
            return os.environ[n]
    return None

# Colab Secrets don't auto-load into os.environ — read them here and set the names
# classic LangChain expects. Works whether you named them LANGCHAIN_* or LANGSMITH_*.
ls_key = _secret("LANGCHAIN_API_KEY", "LANGSMITH_API_KEY")
if ls_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"           # the switch (NOT LANGSMITH_TRACING on 0.3.x)
    os.environ["LANGCHAIN_API_KEY"]    = ls_key
    os.environ["LANGCHAIN_PROJECT"]    = _secret("LANGCHAIN_PROJECT", "LANGSMITH_PROJECT") or "agentic-ai-week2"
    endpoint = _secret("LANGCHAIN_ENDPOINT", "LANGSMITH_ENDPOINT")   # only needed for the EU region
    if endpoint:
        os.environ["LANGCHAIN_ENDPOINT"] = endpoint
    print("LangSmith tracing ON")
    print("  key loaded : " + ls_key[:6] + "..." + ls_key[-4:] + "  (" + str(len(ls_key)) + " chars)")
    print("  project    : '" + os.environ["LANGCHAIN_PROJECT"] + "'   <- look for THIS name in LangSmith")
    print("  endpoint   : " + os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com (US default)"))
    print("Now run the wrap_gemini cell below to start tracing the ReAct loop.")
else:
    print("No LangSmith key found -> tracing OFF (everything still runs).")
    print("Fix: add a Colab Secret named LANGCHAIN_API_KEY (key icon, left sidebar),")
    print("     and toggle 'Notebook access' ON for it. Then re-run this cell -> it must print 'tracing ON'.")
"""),

    md("""**Wrap the raw client (the robust path).** `wrap_gemini` returns a drop-in client that traces every `generate_content` call straight to LangSmith — no LangChain in the path, so version mismatches can't silently swallow it. We re-bind `client` to the wrapped version, so the `run_react` loop you already built now traces **one run per step**.
"""),

    code("""# Robust tracing: wrap the google-genai client directly. Works regardless of LangChain version.
import os
from langsmith import wrappers

if os.environ.get("LANGCHAIN_TRACING_V2") == "true":
    try:
        client = wrappers.wrap_gemini(client)   # re-bind: every client.models.generate_content now traces
        print("wrap_gemini ON -> re-run the ReAct loop in the next cell; each step posts a trace.")
    except (ImportError, AttributeError):
        print("Your langsmith is too old for wrap_gemini.")
        print("Run:  %pip install -q -U langsmith   then  Runtime > Restart session,  and re-run from the top.")
else:
    print("Tracing is OFF -> add LANGCHAIN_API_KEY (cell above) first, then re-run this.")
"""),

    md("""Now re-run the loop with the wrapped client — each Thought -> Action step becomes a separate `generate_content` trace in LangSmith:
"""),

    code("""answer = run_react(
    "Who wrote the ReAct paper, and what year was the transformer paper published? "
    "Then compute the difference in years."
)
print("\\n=== FINAL ANSWER ===")
print(answer)

# force the traces to ship before you look (background posting otherwise lags)
import langsmith
try:
    langsmith.Client().flush()
except Exception:
    pass
print("\\nOpen https://smith.langchain.com -> project '" +
      os.environ.get("LANGCHAIN_PROJECT", "default") +
      "'. Each loop step is a 'generate_content' run — expand one to read the model's Thought/Action.")
"""),

    md("""That's the reliable demo: you're now **watching the agent reason in real time** — one trace per step, with the exact prompt and output Gemini produced.

---

### Optional: the LangChain one-liner (nested trace tree)

`create_react_agent` collapses the whole loop to one line and, *when its tracer fires*, gives a single **nested** trace — the AgentExecutor with each tool call nested beneath it. Run it if you like the tree view.

> ⚠️ **Version caveat.** LangChain's native tracer (path b) only speaks to older `langsmith`, while this notebook pins classic `langchain-core 0.3.x`. On Colab — which pre-installs a newer `langsmith` for LangGraph — this tracer can run without error yet **post nothing**. If no trace appears from the cell below, that's the mismatch, and the `wrap_gemini` path above is your reliable answer. (To make path b work too: `%pip install -q "langsmith>=0.1.125,<0.4"`, restart, re-run.)
"""),

    code("""from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate

# ReAct passes the "Action Input" string straight to the tool, so single-string
# Tool(func=...) wrappers are the natural fit here.
lc_tools = [Tool(name=n, func=fn, description=d) for n, (fn, d) in TOOLS.items()]

# LangChain's stock ReAct prompt needs exactly these vars: tools, tool_names, input, agent_scratchpad.
LC_REACT_PROMPT = PromptTemplate.from_template(\"\"\"Answer the following question as best you can. You have access to these tools:

{tools}

Use this format:

Question: the input question
Thought: reasoning
Action: one of [{tool_names}]
Action Input: input to the action
Observation: result
... (repeat as needed)
Thought: I now know the final answer
Final Answer: the final answer

Begin!

Question: {input}
Thought:{agent_scratchpad}\"\"\")

agent = create_react_agent(llm, lc_tools, LC_REACT_PROMPT)
executor = AgentExecutor(agent=agent, tools=lc_tools, verbose=True,
                         max_iterations=6, handle_parsing_errors=True)

result = executor.invoke({
    "input": "Who wrote the ReAct paper, and what year was the transformer paper published? "
             "Then compute the difference in years.",
})
print("\\n=== FINAL ANSWER ===")
print(result["output"])

# Force this run to post to LangSmith now (otherwise it flushes a few seconds later).
try:
    from langchain_core.tracers.langchain import wait_for_all_tracers
    wait_for_all_tracers()
except Exception:
    pass
"""),

    md("""Same answer — but now the loop is one line. Because we built it ourselves first, the abstraction is transparent: when LangChain raises `OutputParserException: Could not parse LLM output`, you know it's the regex on `Action:` that failed, and `handle_parsing_errors=True` is what feeds the model a "fix your format" nudge instead of crashing.

**If** LangChain's tracer fired (see the version caveat above), open [smith.langchain.com](https://smith.langchain.com) and you'll find this `AgentExecutor` run as a single **nested trace tree** — expand it for every Thought → Action → Observation, which tool ran with what input, the latency, and token counts. If nothing showed up here, that's the `langsmith` version mismatch — the `wrap_gemini` traces from the loop above are your reliable view, and they carry the same information one run per step.

> The takeaway either way: you **watch the trace** instead of guessing which step went wrong. `wrap_gemini` traces the raw loop (one run per call); `create_react_agent` traces the LangChain agent (one nested tree) — same reasoning, two views.

---

## 6. Live-add a tool

Extending an agent doesn't touch the loop. Add to the tool list; the prompt re-renders with the new tool next iteration.
"""),

    code("""new_tool = Tool(
    name="get_arxiv_abstract",
    func=fetch_paper_abstract,
    description="Fetch the abstract of a paper given its arXiv ID, like '2210.03629'.",
)

lc_tools_ext = lc_tools + [new_tool]
agent2 = create_react_agent(llm, lc_tools_ext, LC_REACT_PROMPT)
executor2 = AgentExecutor(agent=agent2, tools=lc_tools_ext, verbose=True,
                          max_iterations=6, handle_parsing_errors=True)

result = executor2.invoke({
    "input": "Get the abstract of arXiv 2210.03629 and tell me in one sentence what ReAct does.",
})
print("\\n=== FINAL ANSWER ===")
print(result["output"])
"""),

    md("""The agent picked up the new tool with **no prompt edit** — because the tool list *is* the agent's vocabulary, re-rendered into the prompt every step. This is why, in agent-land, *tool design* (clear names + descriptions) matters more than long system prompts.

---

## 7. Tree-of-Thoughts — when one chain of reasoning isn't enough

CoT and ReAct commit to a single line of reasoning. If an early step is wrong, the whole chain is wrong. **Tree-of-Thoughts** (Yao et al., 2023) treats reasoning as **search**: at each step, *propose* several candidate thoughts, *evaluate* how promising each is, then *expand* the best — with backtracking.

We show one level of the search machinery on the "Game of 24" (use the four numbers with `+ - * /` to make 24). The full algorithm recurses this to a solution; we keep it to a single propose -> evaluate step so it stays cheap and readable.
"""),

    code("""NUMBERS = [4, 9, 10, 13]

def propose_first_steps(numbers, n=3):
    \"\"\"Ask the model to PROPOSE several candidate first moves (the 'branching' step).\"\"\"
    msg = (f"Game of 24. Numbers: {numbers}. Propose {n} DIFFERENT promising first moves. "
           f"A move combines two of the numbers with + - * or /, leaving a new list of 3 numbers. "
           f"Reply as one move per line in the form:  a OP b = c  (remaining: ...)")
    return llm.invoke(msg).content


def evaluate_states(proposals):
    \"\"\"Ask the model to EVALUATE each candidate as sure / maybe / impossible (the 'pruning' step).\"\"\"
    msg = ("For each proposed first move below, judge whether the remaining three numbers can still "
           "reach 24. Label each: SURE, MAYBE, or IMPOSSIBLE, with a 6-word reason.\\n\\n" + proposals)
    return llm.invoke(msg).content


print("=== PROPOSE (branch) ===")
proposals = propose_first_steps(NUMBERS)
print(proposals)

print("\\n=== EVALUATE (prune) ===")
print(evaluate_states(proposals))
"""),

    md("""That is the heart of ToT: **propose -> evaluate -> keep the promising branches -> expand**, instead of betting everything on the first thought. Real ToT loops this with a search policy (BFS/DFS + a value heuristic) and backtracks out of dead ends — trading more compute for higher accuracy on problems where a single CoT chain routinely fails (planning, puzzles, proof search).

| Pattern | Shape | When to reach for it |
|---|---|---|
| **CoT** | one straight line of reasoning | most single-pass reasoning tasks |
| **ReAct** | a line of reasoning + tool calls | the model needs facts/computation from outside |
| **ToT** | a tree, searched + pruned | one wrong early step dooms the whole answer |

---

## 8. ReAct vs the tool-calling agent — the two paradigms

We've now built tools two ways: the **tool-calling agent** (Notebook 01) and the **ReAct agent** (this notebook). They solve the same job — *pick a tool, run it, feed the result back* — but the responsibility for **picking the right tool** sits in different places.

Run the same question through both and watch the traces.
"""),

    code("""from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# Typed @tool versions work for BOTH agent styles.
@tool
def search(query: str) -> str:
    \"\"\"Search the web for a fact. Input: a query string.\"\"\"
    return web_search(query)

@tool
def calc(expression: str) -> str:
    \"\"\"Do arithmetic. Input: an expression like '2023 - 2017'.\"\"\"
    return calculator(expression)

shared_tools = [search, calc]
QUESTION = ("Who wrote the ReAct paper, and what year was the transformer paper published? "
            "Then compute the difference in years.")

# (a) ReAct agent — tool choice comes from the ReAct PROMPT + our regex parse
react_tools = [Tool(name=t.name, func=t.func, description=t.description) for t in shared_tools]
react_agent = create_react_agent(llm, react_tools, LC_REACT_PROMPT)
react_exec = AgentExecutor(agent=react_agent, tools=react_tools, verbose=True,
                           max_iterations=6, handle_parsing_errors=True)
print("########## ReAct agent ##########")
react_out = as_text(react_exec.invoke({"input": QUESTION})["output"])

# (b) Tool-calling agent — tool choice comes from the MODEL's native function-calling
tc_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when they help."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
tc_agent = create_tool_calling_agent(llm, shared_tools, tc_prompt)
tc_exec = AgentExecutor(agent=tc_agent, tools=shared_tools, verbose=True, max_iterations=6)
print("\\n########## Tool-calling agent ##########")
tc_out = as_text(tc_exec.invoke({"input": QUESTION})["output"])

print("\\n=== ReAct answer ===\\n", react_out)
print("\\n=== Tool-calling answer ===\\n", tc_out)
"""),

    md("""**Same answer, two very different mechanisms.**

| | ReAct agent | Tool-calling (function-calling) agent |
|---|---|---|
| How a tool is chosen | The **ReAct prompt** turns the LLM into a reasoning engine; it writes `Action: / Action Input:` as **text** | The **model vendor's** native function-calling picks the tool + arguments as a structured function-call part |
| Who owns tool selection | **You** — it lives in a prompt you can read and edit | **The vendor** — fine-tuned into the model, hidden from you |
| Parsing | Regex on `Action:` lines (brittle; needs `handle_parsing_errors`) | Structured blocks — no parsing |
| Control / flexibility | **High** — tweak the prompt, change the format, inspect every Thought | **Lower** — you can't see or alter the selection logic |
| Effort / robustness | More to maintain; can mis-format | Less work; more robust out of the box |
| Best when | You need transparency, custom formats, or a model without tool-calling | You're on a modern tool-calling model and want the loop to just work |

This is the "where do we shift the responsibility?" question from the lecture. ReAct keeps tool selection **in a prompt you control**; the function-calling agent **shifts it to the vendor** — less control, much less headache. Most production agents today use function-calling; ReAct remains the clearest way to *understand* what an agent is, and the fallback when a model has no native tool-calling.

---

## 9. Closing exercises (for after class)

1. **Stopping conditions.** Add a token budget to the hand-built loop (stop if cumulative input tokens > 10k). Where does it go?
2. **CoT vs direct, measured.** Run 10 word-problems with and without "Let's think step by step." Count correct answers. How big is the lift?
3. **ToT, fully.** Extend section 7 into a real depth-2 search: expand the top-2 SURE branches one more level. Does it find a solution to Game of 24 for `[4, 9, 10, 13]`?
4. **Force a parse error.** Edit `LC_REACT_PROMPT` to drop the `Action Input:` line. Watch `handle_parsing_errors=True` recover — then set it to `False` and watch it crash. That's the value of building the primitive first.

---

**Next:** [Notebook 03 — RAG End-to-End](03_rag_pipeline.ipynb)
"""),
]


# ============================================================================
# NOTEBOOK 03 — RAG end-to-end (LangChain-native)
# ============================================================================

NB03 = [
    md("""# Notebook 03 — RAG End-to-End (the LangChain way)

**Workshop:** Agentic AI for Scientists — Week 2
**Block:** 4 of 6 (35 min)
**Goal:** RAG (Retrieval-Augmented Generation) is two halves: **retrieval** and **prompt augmentation**. We build the whole pipeline with LangChain's native pieces — loaders, splitters, embeddings, vector stores — then compare three retrieval strategies on five real questions.

**Corpus:** five public ML/AI papers (downloaded on first run).

**Pipeline — and the LangChain class for each stage:**

```
PDFs --PyPDFLoader-->  Documents
      --RecursiveCharacterTextSplitter-->  chunks
      --HuggingFaceEmbeddings-->  vectors
      --FAISS / Chroma-->  vector store --.as_retriever()--> retriever
                                                                 |
question --retriever--> top-k chunks --prompt--> Gemini --> grounded answer
```

We retrieve three ways — **dense** (FAISS), **sparse** (BM25), **hybrid** (EnsembleRetriever) — then score `hit@5` on a labelled eval set.
"""),

    md("## 0. Setup"),

    code("""%pip install -q \\
    "google-genai>=1.0" \\
    "langchain==0.3.7" "langchain-google-genai==2.0.11" "langchain-community==0.3.5" \\
    "langchain-text-splitters==0.3.2" "langchain-huggingface==0.1.2" "langchain-chroma==0.1.4" \\
    "faiss-cpu==1.9.0" "rank-bm25==0.2.2" "sentence-transformers==3.3.0" \\
    "pypdf==5.1.0" "pandas==2.2.3" python-dotenv requests
"""),

    code(KEY_CELL),

    code(f"""import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"   # silence Chroma's telemetry chatter
from pathlib import Path
import json, requests
import pandas as pd

MODEL = "{MODEL}"
print("Ready.")
"""),

    md("""---

## 1. Download the corpus

Five public ML/AI papers from arXiv. ~7 MB total.
"""),

    code("""CORPUS_DIR = Path("sample_articles")
CORPUS_DIR.mkdir(exist_ok=True)

PAPERS = {
    "react_yao_2022.pdf": "https://arxiv.org/pdf/2210.03629",
    "attention_vaswani_2017.pdf": "https://arxiv.org/pdf/1706.03762",
    "chinchilla_hoffmann_2022.pdf": "https://arxiv.org/pdf/2203.15556",
    "constitutional_ai_bai_2022.pdf": "https://arxiv.org/pdf/2212.08073",
    "rag_lewis_2020.pdf": "https://arxiv.org/pdf/2005.11401",
}

for filename, url in PAPERS.items():
    target = CORPUS_DIR / filename
    if target.exists() and target.stat().st_size > 10_000:
        print(f"  cached: {filename}")
        continue
    print(f"  downloading: {filename}")
    r = requests.get(url, timeout=60, headers={"User-Agent": "agentic-workshop/1.0"})
    r.raise_for_status()
    target.write_bytes(r.content)
print("\\nDone.")
"""),

    md("""---

## 2. Load PDFs with `PyPDFLoader`

LangChain's loaders all return a list of **`Document`** objects — `.page_content` (the text) plus `.metadata` (here: `source` file and `page` number). One Document per page. This metadata is what lets us cite a source later.
"""),

    code("""from langchain_community.document_loaders import PyPDFLoader

pages = []
for path in sorted(CORPUS_DIR.glob("*.pdf")):
    loaded = PyPDFLoader(str(path)).load()      # list[Document], one per page
    # Normalise 'source' to just the filename so citations stay short.
    for d in loaded:
        d.metadata["source"] = path.name
    pages.extend(loaded)
    print(f"  {path.name}: {len(loaded)} pages")

print(f"\\nTotal: {len(pages)} page-documents")
print("\\n--- sample Document ---")
print("metadata:", pages[0].metadata)
print("content :", pages[0].page_content[:200].replace(chr(10), ' '), "...")
"""),

    md("""---

## 3. Chunk with `RecursiveCharacterTextSplitter`

A page is too big to embed as one vector. We split into ~800-character chunks. The **recursive** splitter tries paragraph -> sentence -> word -> char boundaries in order, so chunks rarely cut mid-sentence. Use `.split_documents()` (not `.split_text()`) so the per-page metadata is carried onto every chunk.
"""),

    code("""from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,          # ~200 tokens; fits comfortably when we stuff 5 chunks into context
    chunk_overlap=100,       # ~12% overlap so a sentence split across chunks survives in one of them
    separators=["\\n\\n", "\\n", ". ", " ", ""],
)

chunks = splitter.split_documents(pages)

# Tag each chunk with a short id we can cite, e.g. react_yao_2022.pdf#42
for i, c in enumerate(chunks):
    c.metadata["chunk_id"] = f"{c.metadata['source']}#{i}"

print(f"{len(pages)} pages -> {len(chunks)} chunks")
print("\\n--- sample chunk ---")
print("chunk_id:", chunks[0].metadata["chunk_id"])
print(chunks[0].page_content[:250], "...")
"""),

    md("""> **The dirty secret of RAG:** chunk size/overlap often matters more than which embedding model you pick. We use 800/100 as a sane default; the closing exercises sweep it. **Semantic chunking** (splitting on embedding-distance jumps) exists via `SemanticChunker` — slower, marginal gains here, so we skip it live.

---

## 4. Embeddings — a free local model

`all-MiniLM-L6-v2` is 90 MB, runs on CPU in Colab's free tier, and is plenty for a 5-paper demo. `HuggingFaceEmbeddings` (from `langchain_huggingface`) wraps it in LangChain's embedding interface so any vector store can use it. Production swap: `text-embedding-3-small` (OpenAI) or `text-embedding-004` (Google).
"""),

    code("""from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Sanity check: embed one string, look at the dimension
v = embeddings.embed_query("What is the ReAct loop?")
print(f"embedding dimension: {len(v)}")
"""),

    md("""---

## 5. Dense retrieval — FAISS vector store

`FAISS.from_documents` embeds every chunk and builds an in-memory similarity index in one call. `.as_retriever()` hands back a standard LangChain **retriever** — a component whose only job is `query -> list[Document]`, which plugs straight into a chain.
"""),

    code("""from langchain_community.vectorstores import FAISS

faiss_store = FAISS.from_documents(chunks, embeddings)
faiss_retriever = faiss_store.as_retriever(search_kwargs={"k": 5})
print(f"FAISS index built: {faiss_store.index.ntotal} vectors")

# Look at what comes back
hits = faiss_retriever.invoke("What is the ReAct loop?")
for d in hits[:3]:
    print(f"  {d.metadata['chunk_id']}: {d.page_content[:110].replace(chr(10),' ')}...")
"""),

    md("""You can persist a FAISS index to disk and reload it (handy so you don't re-embed every run):

```python
faiss_store.save_local("faiss_index")
reloaded = FAISS.load_local("faiss_index", embeddings,
                            allow_dangerous_deserialization=True)  # required: the index is unpickled
```

The `allow_dangerous_deserialization=True` flag is mandatory on load — unpickling can execute code, so only load indexes you built yourself.

---

## 6. The same store, persisted — Chroma

FAISS is a raw in-memory index. **Chroma** is a small local *database*: pass `persist_directory=` and it writes to disk and **auto-persists** (no `.persist()` call needed in modern `langchain_chroma`). Reopen the directory later and your vectors are still there — useful when the corpus is expensive to embed.
"""),

    code("""from langchain_chroma import Chroma

chroma_store = Chroma.from_documents(
    chunks, embeddings,
    persist_directory="./chroma_db",
    collection_name="w2_papers",
)
chroma_retriever = chroma_store.as_retriever(search_kwargs={"k": 5})
print(f"Chroma collection size: {chroma_store._collection.count()} vectors")

# Same retriever interface, different backend — identical call shape
hits = chroma_retriever.invoke("What is the ReAct loop?")
for d in hits[:3]:
    print(f"  {d.metadata['chunk_id']}: {d.page_content[:110].replace(chr(10),' ')}...")
"""),

    md("""**FAISS vs Chroma, in one line:** FAISS = fastest pure-vector index, lives in RAM; Chroma = a persistent local store with metadata filtering and a friendlier API. Both expose the *same* `.as_retriever()` interface, so the rest of the notebook doesn't care which you picked. We use the FAISS retriever for the comparison below.

---

## 7. Sparse retrieval — BM25

BM25 is classical keyword scoring — no embeddings, fast, and surprisingly strong on exact-term queries (acronyms, names, jargon). `BM25Retriever.from_documents` builds it from the same chunks, giving us the same `query -> Documents` interface.
"""),

    code("""from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

hits = bm25_retriever.invoke("What is the ReAct loop?")
for d in hits[:3]:
    print(f"  {d.metadata['chunk_id']}: {d.page_content[:110].replace(chr(10),' ')}...")
"""),

    md("""---

## 8. Hybrid retrieval — `EnsembleRetriever`

Dense catches *paraphrase* ("what does X mean?"); sparse catches *exact terms* ("RLAIF", "DPR"). `EnsembleRetriever` fuses both with **Reciprocal Rank Fusion** (RRF) — it merges by rank, not raw score, so we sidestep the normalization headache entirely. `weights` bias the fusion.
"""),

    code("""from langchain.retrievers import EnsembleRetriever

hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.4, 0.6],     # lean slightly toward dense; tune on your eval set
)

hits = hybrid_retriever.invoke("What is the ReAct loop?")
for d in hits[:3]:
    print(f"  {d.metadata['chunk_id']}: {d.page_content[:110].replace(chr(10),' ')}...")
"""),

    md("""---

## 9. Compare the three retrievers — `hit@5` on a labelled eval set

`hit@5` = 1 if any of the top-5 chunks comes from the expected paper. The stricter **section hit** = 1 if any ground-truth keyword appears in the retrieved text (did we get the *right part* of the right paper?).
"""),

    code("""# The five labelled test questions, inlined so this notebook has zero external deps.
# Each names the paper (expected_source) and a few ground-truth keywords from the
# section that answers it (expected_section_keywords).
questions = [
    {"id": "q1_react_loop",
     "question": "What are the three steps in a single iteration of the ReAct loop?",
     "expected_source": "react_yao_2022.pdf",
     "expected_section_keywords": ["Thought", "Action", "Observation", "interleaving"]},
    {"id": "q2_attention_complexity",
     "question": "Why is scaled dot-product attention preferred over additive attention for transformer architectures?",
     "expected_source": "attention_vaswani_2017.pdf",
     "expected_section_keywords": ["scaled dot-product", "additive", "matrix multiplication", "faster"]},
    {"id": "q3_chinchilla_scaling",
     "question": "According to the Chinchilla paper, what is the optimal ratio of training tokens to model parameters?",
     "expected_source": "chinchilla_hoffmann_2022.pdf",
     "expected_section_keywords": ["tokens per parameter", "compute-optimal", "scaling", "training tokens"]},
    {"id": "q4_constitutional_ai_rlaif",
     "question": "What is the role of the AI feedback signal in Constitutional AI training?",
     "expected_source": "constitutional_ai_bai_2022.pdf",
     "expected_section_keywords": ["RLAIF", "AI feedback", "preference model", "constitution", "self-critique"]},
    {"id": "q5_rag_architecture",
     "question": "What are the two main components of the retrieval-augmented generation architecture?",
     "expected_source": "rag_lewis_2020.pdf",
     "expected_section_keywords": ["retriever", "generator", "non-parametric", "parametric", "BART"]},
]
print(f"Loaded {len(questions)} test questions")


def source_hit(docs, expected_source):
    return int(any(d.metadata["source"] == expected_source for d in docs))


def section_hit(docs, keywords):
    blob = " ".join(d.page_content.lower() for d in docs)
    return int(any(kw.lower() in blob for kw in keywords))


retrievers = {"dense": faiss_retriever, "bm25": bm25_retriever, "hybrid": hybrid_retriever}

rows = []
for q in questions:
    row = {"id": q["id"], "expected": q["expected_source"].split("_")[0]}
    for name, r in retrievers.items():
        docs = r.invoke(q["question"])
        row[f"{name}_hit@5"] = source_hit(docs, q["expected_source"])
        row[f"{name}_section"] = section_hit(docs, q["expected_section_keywords"])
    rows.append(row)

df = pd.DataFrame(rows)
print(df.to_string(index=False))

print("\\n=== Aggregate ===")
for col in df.columns:
    if col.endswith("hit@5") or col.endswith("section"):
        print(f"  {col:16s}: {df[col].mean():.2f}")
"""),

    md("""**Read the table.** On a corpus this small, all three usually nail the *paper-level* hit. The *section-level* hit is the honest metric. Hybrid tends to win it because it gets both the paraphrased and the exact-term queries. For your own corpus, tune the ensemble `weights` on an eval set like this one — production typically lands between 0.3 and 0.7 dense.

---

## 10. Wire a retriever into a RAG chain (the "augmentation" half)

Retrieval done — now *use* it. The LCEL pipe stuffs the retrieved chunks into the prompt's `{context}`, the model answers from them, and we ask it to **cite the chunk_id** behind every claim.
"""),

    code("""from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatGoogleGenerativeAI(model=MODEL, temperature=0)

RAG_PROMPT = ChatPromptTemplate.from_template(\"\"\"You are a research assistant. Answer the question using ONLY the context below. If the context doesn't contain the answer, say so — do not invent. Cite the [chunk_id] in brackets after every claim.

Context:
{context}

Question: {question}

Answer (with citations):\"\"\")


def format_docs(docs):
    return "\\n\\n".join(f"[{d.metadata['chunk_id']}] {d.page_content}" for d in docs)


rag_chain = (
    {"context": hybrid_retriever | format_docs, "question": RunnablePassthrough()}
    | RAG_PROMPT | llm | StrOutputParser()
)

q = questions[0]["question"]
print("Q:", q, "\\n")
print(rag_chain.invoke(q))
"""),

    md("""The answer should carry `[react_yao_2022.pdf#N]` citations — every claim points back to a chunk you can open and verify. That grounding is the whole reason RAG beats plain chat for research work.

> **The official shortcut.** LangChain also ships `create_retrieval_chain` + `create_stuff_documents_chain`, which do the retrieve-then-stuff wiring for you and return a dict with both the `answer` and the retrieved `context`. The explicit LCEL pipe above is the transparent version; the helper is the batteries-included one. Same idea either way.

---

## 11. RAG vs no RAG

Same question, straight to the model with no retrieval:
"""),

    code("""bare = llm.invoke(questions[0]["question"]).content
print(bare)
"""),

    md("""Notice the difference: ungrounded, the model answers from training memory — no citations, and it can be confidently wrong on specifics. With RAG, every claim is anchored to a retrievable chunk.

---

## 12. Closing exercises (for after class)

1. **Chunk-size sweep.** Re-run cells 3 & 5 with `chunk_size=400` and `1600`. How does `hit@5` move?
2. **Weight sweep.** Plot `hybrid_section` as the ensemble `weights` go from `[1, 0]` (BM25 only) to `[0, 1]` (dense only). Where's the sweet spot for this corpus?
3. **Swap the store.** Replace `faiss_retriever` with `chroma_retriever` in the ensemble. Same numbers? (They should be — same vectors, same interface.)
4. **Add your own paper.** Drop a PDF into `sample_articles/`, re-run cells 2–5, ask about it. Does the answer cite the right chunk?
5. **Production embeddings.** Swap `HuggingFaceEmbeddings` for OpenAI `text-embedding-3-small`. Better section-hit?

---

**Optional next:** [Notebook 04 — Elasticsearch Appendix](04_rag_elasticsearch_appendix.ipynb)
**Week 3 preview:** this `hybrid_retriever` becomes a *tool node* in a LangGraph multi-agent researcher. Same retriever, different orchestrator.
"""),
]


# ============================================================================
# NOTEBOOK 04 — Elasticsearch appendix (unchanged structure)
# ============================================================================

NB04 = [
    md("""# Notebook 04 — Elasticsearch Appendix (Optional Homework)

**Workshop:** Agentic AI for Scientists — Week 2
**Status:** Optional — not run in class. Self-paced after.
**Prereq:** Notebook 03 working (we reuse the corpus + chunks + eval set).

**Goal:** Show how the in-memory hybrid pipeline from Notebook 03 looks in production. We use **Elasticsearch** with native **RRF (Reciprocal Rank Fusion)** — the standard hybrid-search recipe in production ES. It's the same RRF that `EnsembleRetriever` used in Notebook 03, now running inside a real search engine.

**You need:**
- A free Elastic Cloud trial (14 days, no credit card): https://cloud.elastic.co
- Your `ELASTIC_CLOUD_ID` and `ELASTIC_API_KEY` in `.env`

**What changes vs Notebook 03:**

| | In-memory (NB03) | Elasticsearch (NB04) |
|---|---|---|
| Dense store | FAISS / Chroma (in RAM / local disk) | ES `dense_vector` field with HNSW index |
| Sparse store | rank_bm25 (in RAM) | ES inverted index with BM25 scoring |
| Hybrid | EnsembleRetriever (RRF) | Native RRF retriever |
| Scale | ~10k chunks before RAM hurts | Millions of chunks, sharded |
| Filters | Manual Python | Native query DSL (date, source, metadata) |

The retrieval *interface* is the same: `retrieve_X(query, k)` returns chunks. Plug it into the same RAG chain from Notebook 03.
"""),

    md("## 0. Setup"),

    code("""%pip install -q "elasticsearch==8.15.1" "sentence-transformers==3.3.0" "pypdf==5.1.0" \\
    "pandas==2.2.3" "google-genai>=1.0" python-dotenv requests
"""),

    code("""import os, json, re
from pathlib import Path
import requests
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch, helpers

try:
    from google.colab import userdata  # type: ignore
    os.environ["ELASTIC_CLOUD_ID"] = userdata.get("ELASTIC_CLOUD_ID")
    os.environ["ELASTIC_API_KEY"] = userdata.get("ELASTIC_API_KEY")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()

CLOUD_ID = os.environ.get("ELASTIC_CLOUD_ID")
API_KEY = os.environ.get("ELASTIC_API_KEY")
assert CLOUD_ID and API_KEY, (
    "Set ELASTIC_CLOUD_ID and ELASTIC_API_KEY first. Free trial: https://cloud.elastic.co"
)

es = Elasticsearch(cloud_id=CLOUD_ID, api_key=API_KEY, request_timeout=60)
print(f"Connected to ES: {es.info()['cluster_name']}")
"""),

    md("---\n\n## 1. Recreate the corpus + chunks (reuses NB03 logic)"),

    code("""CORPUS_DIR = Path("sample_articles")
CORPUS_DIR.mkdir(exist_ok=True)
PAPERS = {
    "react_yao_2022.pdf": "https://arxiv.org/pdf/2210.03629",
    "attention_vaswani_2017.pdf": "https://arxiv.org/pdf/1706.03762",
    "chinchilla_hoffmann_2022.pdf": "https://arxiv.org/pdf/2203.15556",
    "constitutional_ai_bai_2022.pdf": "https://arxiv.org/pdf/2212.08073",
    "rag_lewis_2020.pdf": "https://arxiv.org/pdf/2005.11401",
}
for filename, url in PAPERS.items():
    target = CORPUS_DIR / filename
    if not target.exists():
        target.write_bytes(requests.get(url, timeout=60, headers={"User-Agent": "agentic-workshop/1.0"}).content)
        print(f"  downloaded {filename}")
print("Corpus ready.")
"""),

    code("""from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100,
                                          separators=["\\n\\n", "\\n", ". ", " ", ""])

chunks = []
for path in sorted(CORPUS_DIR.glob("*.pdf")):
    text = "\\n\\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    for i, piece in enumerate(splitter.split_text(text)):
        chunks.append({"text": piece, "source": path.name, "chunk_id": f"{path.name}#{i}"})

print(f"{len(chunks)} chunks across {len(PAPERS)} papers")

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
EMB_DIM = embedder.get_sentence_embedding_dimension()
print(f"Embedding chunks (dim={EMB_DIM})...")
embs = embedder.encode([c["text"] for c in chunks], show_progress_bar=True, normalize_embeddings=True)
print(f"  shape={embs.shape}")
"""),

    md("""---

## 2. Create the ES index with mixed mapping

One field for the dense vector, one for the text (BM25). Both live in the same document.
"""),

    code("""INDEX = "agentic-w2-papers"

if es.indices.exists(index=INDEX):
    print(f"  deleting existing index {INDEX}")
    es.indices.delete(index=INDEX)

es.indices.create(
    index=INDEX,
    mappings={
        "properties": {
            "text": {"type": "text"},
            "source": {"type": "keyword"},
            "chunk_id": {"type": "keyword"},
            "embedding": {"type": "dense_vector", "dims": EMB_DIM, "index": True, "similarity": "cosine"},
        }
    },
)
print(f"Created index {INDEX}")
"""),

    md("---\n\n## 3. Bulk-index the chunks"),

    code("""actions = [
    {"_index": INDEX, "_id": c["chunk_id"], "_source": {**c, "embedding": emb.tolist()}}
    for c, emb in zip(chunks, embs)
]
helpers.bulk(es, actions, request_timeout=60)
es.indices.refresh(index=INDEX)
print(f"Indexed {es.count(index=INDEX)['count']} chunks")
"""),

    md("""---

## 4. Dense, sparse, and hybrid retrieval against ES

Same `retrieve_X(query, k)` shape as Notebook 03 — different backend.
"""),

    code("""def retrieve_dense_es(query, k=5):
    q_emb = embedder.encode([query], normalize_embeddings=True)[0].tolist()
    resp = es.search(index=INDEX, size=k,
                     knn={"field": "embedding", "query_vector": q_emb, "k": k, "num_candidates": 50},
                     source_includes=["text", "source", "chunk_id"])
    return [{**h["_source"], "score": h["_score"]} for h in resp["hits"]["hits"]]


def retrieve_bm25_es(query, k=5):
    resp = es.search(index=INDEX, size=k, query={"match": {"text": query}},
                     source_includes=["text", "source", "chunk_id"])
    return [{**h["_source"], "score": h["_score"]} for h in resp["hits"]["hits"]]


def retrieve_hybrid_rrf(query, k=5, rank_constant=60):
    \"\"\"Native RRF via the ES retrievers API (ES 8.13+).\"\"\"
    q_emb = embedder.encode([query], normalize_embeddings=True)[0].tolist()
    resp = es.search(index=INDEX, size=k, retriever={
        "rrf": {
            "retrievers": [
                {"standard": {"query": {"match": {"text": query}}}},
                {"knn": {"field": "embedding", "query_vector": q_emb, "k": k, "num_candidates": 50}},
            ],
            "rank_window_size": 50,
            "rank_constant": rank_constant,
        }
    }, source_includes=["text", "source", "chunk_id"])
    return [{**h["_source"], "score": h["_score"]} for h in resp["hits"]["hits"]]


for name, fn in [("dense", retrieve_dense_es), ("bm25", retrieve_bm25_es), ("rrf-hybrid", retrieve_hybrid_rrf)]:
    print(f"\\n--- {name} ---")
    for r in fn("What is the ReAct loop?", k=3):
        print(f"  [{r['score']:.3f}] {r['chunk_id']}: {r['text'][:100]}...")
"""),

    md("---\n\n## 5. Same comparison as NB03, against ES"),

    code("""# Same five labelled questions as Notebook 03, inlined (no external dependency).
questions = [
    {"id": "q1_react_loop",
     "question": "What are the three steps in a single iteration of the ReAct loop?",
     "expected_source": "react_yao_2022.pdf",
     "expected_section_keywords": ["Thought", "Action", "Observation", "interleaving"]},
    {"id": "q2_attention_complexity",
     "question": "Why is scaled dot-product attention preferred over additive attention for transformer architectures?",
     "expected_source": "attention_vaswani_2017.pdf",
     "expected_section_keywords": ["scaled dot-product", "additive", "matrix multiplication", "faster"]},
    {"id": "q3_chinchilla_scaling",
     "question": "According to the Chinchilla paper, what is the optimal ratio of training tokens to model parameters?",
     "expected_source": "chinchilla_hoffmann_2022.pdf",
     "expected_section_keywords": ["tokens per parameter", "compute-optimal", "scaling", "training tokens"]},
    {"id": "q4_constitutional_ai_rlaif",
     "question": "What is the role of the AI feedback signal in Constitutional AI training?",
     "expected_source": "constitutional_ai_bai_2022.pdf",
     "expected_section_keywords": ["RLAIF", "AI feedback", "preference model", "constitution", "self-critique"]},
    {"id": "q5_rag_architecture",
     "question": "What are the two main components of the retrieval-augmented generation architecture?",
     "expected_source": "rag_lewis_2020.pdf",
     "expected_section_keywords": ["retriever", "generator", "non-parametric", "parametric", "BART"]},
]


def hit_at_k(retrieved, expected_source):
    return int(any(r["source"] == expected_source for r in retrieved))


def section_hit(retrieved, keywords):
    blob = " ".join(r["text"].lower() for r in retrieved)
    return int(any(kw.lower() in blob for kw in keywords))


rows = []
for q in questions:
    de = retrieve_dense_es(q["question"], k=5)
    bm = retrieve_bm25_es(q["question"], k=5)
    rr = retrieve_hybrid_rrf(q["question"], k=5)
    rows.append({
        "id": q["id"], "expected": q["expected_source"].split("_")[0],
        "es_dense_hit@5": hit_at_k(de, q["expected_source"]),
        "es_bm25_hit@5": hit_at_k(bm, q["expected_source"]),
        "es_rrf_hit@5": hit_at_k(rr, q["expected_source"]),
        "es_dense_section": section_hit(de, q["expected_section_keywords"]),
        "es_bm25_section": section_hit(bm, q["expected_section_keywords"]),
        "es_rrf_section": section_hit(rr, q["expected_section_keywords"]),
    })

df = pd.DataFrame(rows)
print(df.to_string(index=False))
print("\\n=== Aggregate ===")
for col in df.columns[2:]:
    print(f"  {col:22s}: {df[col].mean():.2f}")
"""),

    md("""**Compare these numbers to Notebook 03's table.** On our 5-paper corpus the results are similar — ES doesn't *retrieve better* at this scale. The win shows up when:

- Corpus grows past ~10k chunks (RAM becomes the limit for FAISS)
- You need metadata filtering (date ranges, source authorities)
- You need cross-cluster replication, sharding, or write throughput

**But the principle is identical.** Dense + sparse + RRF — whether the fusion runs in `EnsembleRetriever` or in Elasticsearch is a deployment detail.

---

## 6. Cleanup
"""),

    code("""# Uncomment to delete the index when you're done (so you don't use trial storage)
# es.indices.delete(index=INDEX)
# print(f"Deleted {INDEX}")
"""),

    md("""---

## 7. Where to go from here

- **Weaviate** — same hybrid pattern, open-source, easy local Docker
- **Qdrant** — vector-first, very fast
- **pgvector** — if you're already on Postgres
- **Vespa** — Yahoo-grade scale, complex setup

All implement the same "dense + sparse + fusion" recipe. Once you've built it in-memory (NB03) and in ES (NB04), swapping vendors is a small adapter.
"""),
]


# ============================================================================
# Build them all
# ============================================================================

if __name__ == "__main__":
    print("Building notebooks...")
    write("00_langchain_intro.ipynb", NB00)
    write("01_tool_use.ipynb", NB01)
    write("02_react_agent.ipynb", NB02)
    write("03_rag_pipeline.ipynb", NB03)
    write("04_rag_elasticsearch_appendix.ipynb", NB04)
    print("Done.")
