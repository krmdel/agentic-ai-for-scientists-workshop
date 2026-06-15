# Week 4 — Resources

Curated companion material for **Week 4: Post-Training & Deployment** — why fine-tune, the post-training stages (continued pretraining → supervised fine-tuning → alignment), full fine-tuning vs **LoRA** vs **QLoRA**, the data formats that teach behaviour (chat templates, tool-use and reasoning tokens), and how a trained model is actually served. Suggestions welcome via an issue or pull request.

> **Stack note.** Every training notebook this week runs on **Unsloth** (`FastLanguageModel`) + **TRL** (`SFTTrainer`) on a free Colab GPU. Full SFT / LoRA / QLoRA are the *same* notebook with one flag flipped (`full_finetuning=True` → `get_peft_model(r=…)` → `load_in_4bit=True`).

---

## 📺 Watch first

- **[Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)** — Andrej Karpathy (3h31m). The full training stack: pretraining → SFT → RLHF, hallucinations, tool use. The single best mental model for *why* post-training exists.
- **[State of GPT](https://www.youtube.com/watch?v=bZQun8Y4L2A)** — Andrej Karpathy, Microsoft Build 2023 (~40 min). The post-training pipeline (SFT → reward model → RLHF) in one diagram-driven talk.
- **[LoRA — Explained visually + PyTorch from scratch](https://www.youtube.com/watch?v=PXWYUTMt-AU)** — Umar Jamil. The low-rank update built by hand; the clearest derivation of the `B·A` decomposition you see in Notebook 02. ([more videos](https://umarjamil.org/videos))

---

## 📄 Official documentation (the stack the notebooks run)

- **[Unsloth docs](https://docs.unsloth.ai/)** — `FastLanguageModel.from_pretrained`, `get_peft_model`, 4-bit loading; the 2× faster / ~half-VRAM trainer behind every notebook.
- **[TRL — `SFTTrainer`](https://huggingface.co/docs/trl)** — the supervised fine-tuning loop that runs on top of Unsloth.
- **[PEFT](https://huggingface.co/docs/peft)** — Hugging Face's parameter-efficient fine-tuning library: LoRA, QLoRA, adapters, `r` / `lora_alpha` / target modules.
- **[bitsandbytes](https://huggingface.co/docs/bitsandbytes/main/en/index)** — 4-bit NF4 + double quantization, the quantization under QLoRA.
- **[Transformers — chat templating](https://huggingface.co/docs/transformers/chat_templating)** — how messages become tokens; `<tool_call>` / `<tool_response>` and reasoning zones.
- **[Qwen3 chat template deep dive](https://huggingface.co/blog/qwen-3-chat-template-deep-dive)** — the exact template the notebooks fine-tune against (`<think>`, tool tokens).

---

## ✍️ Essential reading

- **[Practical Tips for Finetuning LLMs Using LoRA](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)** — Sebastian Raschka. Lessons from hundreds of LoRA runs: rank, `alpha`, which layers, optimizer choice. Read before you tune anything for real.
- **[RLHF: Reinforcement Learning from Human Feedback](https://huyenchip.com/2023/05/02/rlhf.html)** — Chip Huyen. The alignment stage explained end-to-end (the source of the "shoggoth" figure in the deck).
- **[PEFT: Parameter-Efficient Fine-Tuning on consumer hardware](https://huggingface.co/blog/peft)** — Hugging Face blog. Why a few million trainable params can match full fine-tuning.
- **[philschmid.de](https://www.philschmid.de/)** — Philipp Schmid's hands-on TRL / QLoRA / deployment how-tos, kept current with the libraries.

---

## 📚 Foundational papers (in the order the lesson builds them)

- **LoRA: Low-Rank Adaptation of Large Language Models** — Hu et al., 2021 · [arXiv 2106.09685](https://arxiv.org/abs/2106.09685)
  Freeze `W`, learn a low-rank update `B·A`. The whole of Notebook 02.
- **QLoRA: Efficient Finetuning of Quantized LLMs** — Dettmers et al., 2023 · [arXiv 2305.14314](https://arxiv.org/abs/2305.14314)
  4-bit NF4 base + LoRA adapters; fine-tune a large model on one consumer GPU. Notebook 03.
- **Training language models to follow instructions (InstructGPT)** — Ouyang et al., 2022 · [arXiv 2203.02155](https://arxiv.org/abs/2203.02155)
  The SFT → reward model → RLHF recipe (the 3-step figure in the deck).
- **Direct Preference Optimization (DPO)** — Rafailov et al., 2023 · [arXiv 2305.18290](https://arxiv.org/abs/2305.18290)
  Alignment without a separate reward model or RL loop; the modern alternative to RLHF.
- **Deep Reinforcement Learning from Human Preferences** — Christiano et al., 2017 · [arXiv 1706.03741](https://arxiv.org/abs/1706.03741)
  The root idea behind RLHF: optimise against a learned model of human preference.

---

## 🚀 Deployment & serving (Notebook 04)

- **[vLLM](https://docs.vllm.ai/)** — high-throughput, OpenAI-compatible serving with PagedAttention; the default self-hosted GPU server.
- **[Ollama](https://github.com/ollama/ollama)** — one-command local/on-device serving of GGUF models (laptop, edge, private).
- **[llama.cpp](https://github.com/ggml-org/llama.cpp)** — the GGUF runtime + quantization toolchain underneath Ollama.
- **[Text Generation Inference (TGI)](https://huggingface.co/docs/text-generation-inference)** — Hugging Face's production inference server.
- **[`jobs/`](jobs/)** — the real (headless) training + batch-inference run on **Hugging Face Jobs**, and [`AGENT_DRIVEN.md`](AGENT_DRIVEN.md) drives the whole lifecycle from Claude Code.

---

## How to use this list

Run the notebooks first — they *are* the lesson. Watch **Karpathy's two talks** for the *why*, then **Umar Jamil's LoRA video** for the math you implement in Notebook 02. Keep the **Unsloth + PEFT + TRL** docs open while you fine-tune. Skim **figure 1 + the abstract** of the LoRA and QLoRA papers; they map one-to-one onto the knobs (`r`, `lora_alpha`, `load_in_4bit`) in the notebooks. When you're ready to ship, read the **vLLM** docs and try **Ollama** locally.
