# Clinical Text Simplifier by Fine-Tuning Qwen and Llama with CLARA-MeD

**Authors:** Paula Guerrero Castelló & Iker Gutierrez Fandiño    
*University of the Basque Country (UPV/EHU)*  
2025-26

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/Clinical_text_simplifier.pdf)
[![HuggingFace - Qwen Demo](https://img.shields.io/badge/%20Demo-Qwen--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier)
[![HuggingFace - Llama Demo](https://img.shields.io/badge/%20Demo-Llama--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier)


This project develops and evaluates two **automatic clinical text simplification (ATS)** models for Spanish. Clinical texts are often written in dense technical language that patients and non-specialists struggle to understand. Our goal is to make medical information more accessible using fine-tuned language models.

We fine-tune the models on the [CLARA-MeD simplified sentences] dataset (Bartolomé Rodríguez et al., 2024), a Spanish parallel corpus for clinical text simplification derived from clinical trial protocols. Available at: https://doi.org/10.20350/digitalCSIC/16110



| Model | HuggingFace Hub |
|-------|-----------|
| `Qwen/Qwen3.5-0.8B` | [pguerrero-igutierrez/qwen_claramed](https://huggingface.co/pguerrero-igutierrez/qwen_claramed) |
| `meta-llama/Llama-3.2-1B-Instruct` | [pguerrero-igutierrez/llama_claramed](https://huggingface.co/pguerrero-igutierrez/llama_claramed) |

Both merged models are deployed as public Gradio apps on Hugging Face Spaces.

### Example

**Input**:
> *Se recomienda profilaxis tromboembólica durante el postoperatorio.*

**[Qwen-FT](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier) output**:
> *Se recomienda prevenir tromboembolismo durante el postoperatorio. El postoperatorio es el período después de una operación. El tromboembolismo es un coágulo de sangre que se forma en un vaso sanguíneo y se mueve a otro lugar del cuerpo.*

**[Llama-FT](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier) output**:
> *Se recomienda evitar el tromboembolismo (obstrucción de un vaso sanguíneo por un coágulo de sangre) durante el postoperatorio.*

---

### Model variants evaluated

We evaluate two variants for each fine-tuned model, along with zero-shot baslines. All models are evaluated on the 120-sentence CLARA-MeD test split using three complementary metrics:

| Model | SARI ↑ | BERT-F1 ↑ | FRE ↑ |
|-------|--------|-----------|-------|
| Llama-base (zero-shot) | 39.11 | 78.98 | 46.62 |
| **Llama-FT-adapter** | 55.56 | **89.64** | 48.82 |
| Llama-FT-merged | 54.66 | 89.63 | 48.72 |
| Qwen-base (zero-shot) | 39.48 | 74.70 | **58.58** |
| **Qwen-FT-adapter**  | **57.73** | 89.30 | 49.75 |
| Qwen-FT-merged | 54.04 | 90.84 | 46.81 |
| Human reference | — | 87.33 | 50.92 |

Key findings:
- All fine-tuned models **consistently outperform their zero-shot baselines** across all metrics.
- Fine-tuned models **surpass the human expert reference** in meaning preservation (BERT-F1), while approaching it in readability and fluency.
- **Merging** the LoRA adapter into the base model causes a small but consistent drop in SARI (Llama: −0.90; Qwen: −3.69), likely because weight interpolation slightly weakens task-specific alignment.
- Qwen-base achieves the highest raw FRE (58.58), but at the cost of very poor semantic fidelity (BERT-F1 74.70), suggesting overly aggressive and meaning-losing simplification.

---

## Setup & Reproduction

### Requirements

```bash
pip install -r requirements.txt
```

### Running the Notebook

The entire pipeline (data loading, baseline inference, fine-tuning, evaluation and demo) is contained in a single Jupyter notebook:

```
APP1_project_IkerGutierrez_PaulaGuerrero.ipynb
```

**Steps:**
1. Mount your Google Drive and place `claramed_synt_simp_aligned.tsv` at `MyDrive/APP1project/`.
2. Run all cells sequentially. Each major section is labelled:
   - **Section 0:** Environment setup & imports
   - **Section 1:** Data loading & prompt formatting
   - **Section 2:** Llama zero-shot baseline
   - **Section 3:** Llama LoRA fine-tuning & inference
   - **Section 4:** Qwen zero-shot baseline
   - **Section 5:** Qwen LoRA fine-tuning & inference
   - **Section 6:** Evaluation (SARI, BLEU, BERTScore, FRE)
   - **Section 7:** Deployment-ready Gradio demos
   - **Section 8:** Appendix (screenshots, UI)

### Running the Demos Locally

```bash
# Qwen demo
pip install -r demo/requirements_demo.txt
python demo/app_qwen.py

# Llama demo
python demo/app_llama.py
```

---
