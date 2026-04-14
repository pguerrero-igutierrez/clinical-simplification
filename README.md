# Clinical Text Simplifier by Fine-Tuning Qwen and Llama with CLARA-MeD

**Authors:** Paula Guerrero Castelló & Iker Gutierrez Fandiño — *University of the Basque Country (EHU)*

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/Clinical_text_simplifier.pdf)
[![HuggingFace - Qwen Demo](https://img.shields.io/badge/%20Demo-Qwen--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier)
[![HuggingFace - Llama Demo](https://img.shields.io/badge/%20Demo-Llama--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier)

This project fine-tunes two large language models for the task of automatic text simplification of clinical texts:
- **Qwen3.5-0.8B**
- **Llama-3.2-1B-Instruct**

on the [CLARA-MeD corpus](https://github.com/lcampillos/CLARA-MeD), a Spanish parallel corpus of clinical sentences and their simplified versions.

### Model variants evaluated

| ID | Description |
|----|-------------|
| `Llama (zero-shot)` | Base Llama-3.2-1B-Instruct, no fine-tuning |
| `Llama-FT` | Base + LoRA adapter (adapter-only inference) |
| `Llama-merged` | LoRA weights merged into the base model |
| `Qwen (zero-shot)` | Base Qwen3.5-0.8B, no fine-tuning |
| `Qwen-FT` | Base + LoRA adapter (adapter-only inference) |
| `Qwen-merged` | LoRA weights merged into the base model |

---
## Features

- **Sentence-level simplification** of clinical texts in Spanish.
- **Evaluation** with automatic metrics: SARI, BERTScore (F1), and Flesch–Szigriszt Reading Ease (FRE).

The Llama and Qwen applications are publicly available as web demos on Hugging Face Spaces:

- [Llama Text Simplifier](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier)  
- [Qwen Text Simplifier](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier)
