# Week 5 — Resources

Curated companion material for **Week 5: Evaluation & Benchmarking** — measuring against held-out ground truth, **LLM-as-a-judge** (and how much to trust it), running published benchmarks honestly, and building a reusable regression suite for your own system. Suggestions welcome via an issue or pull request.

> **Thread note.** Week 5 measures the models **Week 4** produced (base / full SFT / LoRA / QLoRA on MedQuAD). A lower training loss is *not* a better model — this week is how you prove it either way.

---

## 📺 Watch first

- **[Mastering LLMs — talks on Evals](https://www.youtube.com/playlist?list=PLgIaq8VgndJvt-HKMHPXehyJNNXQsAVHD)** — a playlist of conference talks (Hamel Husain and others) on building real eval systems: error analysis, LLM judges, eval-driven development. The practitioner's view that the notebooks operationalise.
- **[Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)** — Andrej Karpathy. The sections on benchmarks, hallucination, and "why a low loss isn't enough" are the motivation for this whole week.

---

## ✍️ Essential reading

- **[Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)** — Hamel Husain. The case that evals are to LLM products what tests are to software — and how to bootstrap them from error analysis. The spine of Notebook 03.
- **[LLM Evals: Everything You Need to Know (FAQ)](https://hamel.dev/blog/posts/evals-faq/)** — Hamel Husain. Practical answers: how many cases, judge vs code-based, calibration, avoiding leaderboard self-deception.
- **[The Evaluation Guidebook](https://github.com/huggingface/evaluation-guidebook)** — Hugging Face (from the Open LLM Leaderboard + `lighteval` team). Theory *and* practice: metric choice, contamination, designing your own eval. ([web version](https://huggingface.co/spaces/OpenEvals/evaluation-guidebook))

---

## 📚 Foundational papers (judges + benchmarks)

- **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** — Zheng et al., 2023 · [arXiv 2306.05685](https://arxiv.org/abs/2306.05685)
  The reference for model-graded eval: pointwise/pairwise judging, position bias, ~80% agreement with humans. Notebook 01.
- **LLMs-as-Judges: A Comprehensive Survey** — 2024 · [arXiv 2412.05579](https://arxiv.org/abs/2412.05579)
  The full landscape of judge methods, biases, and mitigations.
- **Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference** — Chiang et al., 2024 · [arXiv 2403.04132](https://arxiv.org/abs/2403.04132)
  Pairwise human preference at scale; why "is A better than B?" beats absolute scoring.
- **PubMedQA: A Dataset for Biomedical Research Question Answering** — Jin et al., 2019 · [arXiv 1909.06146](https://arxiv.org/abs/1909.06146)
  The medical benchmark you run honestly (against its majority-class baseline) in Notebook 02.
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Jimenez et al., 2023 · [arXiv 2310.06770](https://arxiv.org/abs/2310.06770)
  A *verifiable* agent benchmark (tests pass or they don't) — the gold standard the deck contrasts with judged scores.
- **GAIA: A Benchmark for General AI Assistants** — Mialon et al., 2023 · [arXiv 2311.12983](https://arxiv.org/abs/2311.12983)
  Real-world assistant tasks; a reminder that a high benchmark score ≠ good at *your* workflow.

---

## 🧰 Eval frameworks & benchmark sites

- **[lighteval](https://github.com/huggingface/lighteval)** — Hugging Face's lightweight evaluation harness (the one behind the Open LLM Leaderboard).
- **[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)** — EleutherAI; the de-facto standard for running academic benchmarks reproducibly.
- **[promptfoo](https://www.promptfoo.dev/)** — test matrices, model diffs, and CI for prompts and models.
- **[DeepEval](https://github.com/confident-ai/deepeval)** — pytest-native LLM assertions (turn evals into unit tests).
- **[Ragas](https://docs.ragas.io/)** — RAG-specific metrics (faithfulness, answer/context relevancy).
- **[LangSmith](https://docs.smith.langchain.com/)** / **[Langfuse](https://langfuse.com/)** — dataset versioning, tracing, and online eval in production.
- **Benchmarks:** [PubMedQA](https://pubmedqa.github.io/) · [SWE-bench](https://www.swebench.com/) · [GAIA](https://huggingface.co/gaia-benchmark) · [LMArena (Chatbot Arena)](https://lmarena.ai/)

---

## How to use this list

Run the notebooks first — they *are* the lesson. Read **Hamel Husain's "Your AI Product Needs Evals"** before anything else; it reframes evaluation from a report card into a development loop. Skim **figure 1 + the abstract** of the **MT-Bench** paper before Notebook 01 (judges) and the **SWE-bench** vs **GAIA** abstracts before Notebook 02 (read a benchmark number critically). When you build your own suite in Notebook 03, keep the **HF Evaluation Guidebook** open, then graduate to **promptfoo** or **DeepEval** for scale and CI.
