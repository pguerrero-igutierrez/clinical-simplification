# Clinical Text Simplifier by Fine-Tuning Qwen and Llama with CLARA-MeD

**Authors:** Paula Guerrero Castelló & Iker Gutierrez Fandiño — *University of the Basque Country (EHU)*

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/Clinical_text_simplifier.pdf)
[![HuggingFace - Qwen Demo](https://img.shields.io/badge/%20Demo-Qwen--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier)
[![HuggingFace - Llama Demo](https://img.shields.io/badge/%20Demo-Llama--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier)


This project develops and evaluates **automatic clinical text simplification (ATS)** models for Spanish. Clinical texts are often written in dense technical language that patients and non-specialists struggle to understand. Our goal is to make medical information more accessible using fine-tuned language models.

We fine-tune two models on the [CLARA-MeD corpus](https://github.com/lcampillos/CLARA-MeD), a Spanish parallel corpus of clinical sentences and their simplified versions.

| Model | HuggingFace Hub |
|-------|-----------|-----------------|
| `Qwen/Qwen3.5-0.8B` | [pguerrero-igutierrez/qwen_claramed](https://huggingface.co/pguerrero-igutierrez/qwen_claramed) |
| `meta-llama/Llama-3.2-1B-Instruct` | [pguerrero-igutierrez/llama_claramed](https://huggingface.co/pguerrero-igutierrez/llama_claramed) |

Both merged models are deployed as public Gradio apps on Hugging Face Spaces.

### Example

**Input** *(clinical trial protocol)*:
> *Se recomienda profilaxis tromboembólica durante el postoperatorio.*

**Qwen-FT output**:
> *Se recomienda prevenir tromboembolismo durante el postoperatorio. El postoperatorio es el período después de una operación. El tromboembolismo es un coágulo de sangre que se forma en un vaso sanguíneo y se mueve a otro lugar del cuerpo.*

**Llama-FT output**:
> *Se recomienda evitar el tromboembolismo (obstrucción de un vaso sanguíneo por un coágulo de sangre) durante el postoperatorio.*

---

### Model variants evaluated

We evaluate two variants for each fine-tuned model, along with zero-shot baslines.

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
