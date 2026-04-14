# Clinical Text Simplifiers by Fine-Tuning Qwen and Llama with CLARA-MeD

**Authors:** Paula Guerrero Castelló & Iker Gutierrez Fandiño — *University of the Basque Country (EHU)*

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](./Clinical_text_simplifier.pdf)
[![HuggingFace - Qwen Demo](https://img.shields.io/badge/🤗%20Demo-Qwen--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier)
[![HuggingFace - Llama Demo](https://img.shields.io/badge/🤗%20Demo-Llama--FT--merged-blue)](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 📋 Overview

This project develops and evaluates **automatic clinical text simplification (ATS)** models for Spanish. Clinical texts — such as those found in clinical trial protocols — are often written in dense technical language that patients and non-specialists struggle to understand. Our goal is to make medical information more accessible using fine-tuned language models.

We fine-tune two compact LLMs on the **CLARA-MeD** corpus using parameter-efficient **LoRA** adapters:

| Model | Parameters | HuggingFace Hub |
|-------|-----------|-----------------|
| `Qwen/Qwen3.5-0.8B` | ~0.8B | [pguerrero-igutierrez/qwen_claramed](https://huggingface.co/pguerrero-igutierrez/qwen_claramed) |
| `meta-llama/Llama-3.2-1B-Instruct` | ~1B | [pguerrero-igutierrez/llama_claramed](https://huggingface.co/pguerrero-igutierrez/llama_claramed) |

For each model we produce:
- **Base (zero-shot):** out-of-the-box inference with no fine-tuning.
- **FT-adapter:** LoRA adapter weights trained on CLARA-MeD.
- **FT-merged:** adapter weights merged into the base model for standalone deployment.

---

## 🚀 Live Demos

Both merged models are deployed as public Gradio apps on Hugging Face Spaces:

| Model | Demo link | Size | Approx. inference time |
|-------|-----------|------|------------------------|
| Qwen-FT-merged | [🤗 Launch](https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier) | 1.73 GB | ~40 s / sentence |
| Llama-FT-merged | [🤗 Launch](https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier) | 2.49 GB | ~130 s / sentence |

### Example

**Input** *(clinical trial protocol)*:
> *Se recomienda profilaxis tromboembólica durante el postoperatorio.*

**Qwen-FT output**:
> *Se recomienda prevenir tromboembolismo durante el postoperatorio. El postoperatorio es el período después de una operación. El tromboembolismo es un coágulo de sangre que se forma en un vaso sanguíneo y se mueve a otro lugar del cuerpo.*

**Llama-FT output**:
> *Se recomienda evitar el tromboembolismo (obstrucción de un vaso sanguíneo por un coágulo de sangre) durante el postoperatorio.*

---

## 📁 Repository Structure

```
clinical-simplification/
│
├── APP1_project_IkerGutierrez_PaulaGuerrero.ipynb  ← Main notebook (full pipeline)
│
├── data/
│   └── README.md                    ← How to obtain CLARA-MeD
│
├── results/
│   ├── 01_baseline_llama_inference.csv
│   ├── 02_sent_finetuned_predictions.csv          ← Llama FT adapter
│   ├── 04_qwen_baseline_predictions.csv
│   ├── 05_qwen_finetuned_predictions.csv          ← Qwen FT adapter
│   ├── 06_merged_llama_finetuned_predictions.csv
│   ├── 07_merged_qwen_finetuned_predictions.csv
│   └── metrics_results.csv                        ← Aggregated evaluation table
│
├── figures/
│   ├── loss_curves_llama.png
│   ├── loss_curves_qwen.png
│   └── metrics_comparison.png
│
├── demo/
│   ├── app_qwen.py                  ← Gradio app for Qwen (HF Spaces)
│   ├── app_llama.py                 ← Gradio app for Llama (HF Spaces)
│   └── requirements_demo.txt
│
├── Clinical_text_simplifier.pdf    ← Project paper
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📊 Results

All models are evaluated on the 120-sentence CLARA-MeD test split using three complementary metrics:

| Metric | What it measures |
|--------|-----------------|
| **SARI** | Fluency of simplification: how well the system adds, keeps and deletes words w.r.t. the reference |
| **BERT-F1** | Semantic similarity of the prediction to the *source* (meaning preservation) using multilingual BERT |
| **FRE** | Flesch–Szigriszt Reading Ease: readability based on sentence length and syllable count (higher = easier) |

### Automatic Evaluation

| Model | SARI ↑ | BERT-F1 ↑ | FRE ↑ |
|-------|--------|-----------|-------|
| Llama-base (zero-shot) | 39.11 | 78.98 | 46.62 |
| **Llama-FT-adapter** | 55.56 | **89.64** | 48.82 |
| Llama-FT-merged | 54.66 | 89.63 | 48.72 |
| Qwen-base (zero-shot) | 39.48 | 74.70 | **58.58** |
| **Qwen-FT-adapter** ✅ | **57.73** | 89.30 | 49.75 |
| Qwen-FT-merged | 54.04 | 90.84 | 46.81 |
| Human reference | — | 87.33 | 50.92 |

**Best overall model: Qwen-FT-adapter** — highest SARI (57.73), strong meaning preservation (BERT-F1 89.30), and good readability (FRE 49.75).

Key findings:
- All fine-tuned models **consistently outperform their zero-shot baselines** across all metrics.
- Fine-tuned models **surpass the human expert reference** in meaning preservation (BERT-F1), while approaching it in readability and fluency.
- **Merging** the LoRA adapter into the base model causes a small but consistent drop in SARI (Llama: −0.90; Qwen: −3.69), likely because weight interpolation slightly weakens task-specific alignment.
- Qwen-base achieves the highest raw FRE (58.58), but at the cost of very poor semantic fidelity (BERT-F1 74.70), suggesting overly aggressive and meaning-losing simplification.

---

## 🗂️ Dataset: CLARA-MeD

We use the **CLARA-MeD** corpus ([Campillos-Llanos et al., 2022](https://github.com/lcampillos/CLARA-MeD)), a Spanish parallel corpus for clinical text simplification derived from clinical trial protocols.

| Split | Sentences | % |
|-------|-----------|---|
| Train | 956 | 80% |
| Validation | 120 | 10% |
| Test | 120 | 10% |
| **Total** | **1,196** | **100%** |

Each example pairs a complex source sentence from a clinical trial with an expert-written plain-language simplification. Source sentences average ~65 tokens and contain dense medical terminology, long noun phrases, and complex conditional structures.

> ⚠️ The dataset is not included in this repository. See [`data/README.md`](data/README.md) for download instructions.

---

## ⚙️ Methodology

### 1. Prompt Format

All examples use a shared instruction prompt in Spanish (ChatML format):

```
<|im_start|>system
Eres un asistente médico especializado en simplificar textos médicos complejos
al español sencillo. Simplifica el texto manteniendo la información esencial
pero usando un lenguaje claro y accesible para pacientes sin formación médica.
<|im_end|>
<|im_start|>user
Simplifica el siguiente texto médico:

{source sentence}
<|im_end|>
<|im_start|>assistant
```

### 2. LoRA Fine-Tuning

We apply [LoRA (Hu et al., 2022)](https://arxiv.org/abs/2106.09685) via the [Unsloth](https://github.com/unslothai/unsloth) library for memory-efficient training on a single GPU.

| Hyperparameter | Value |
|---------------|-------|
| LoRA rank `r` | 16 |
| LoRA alpha `α` | 32 |
| LoRA dropout | 0.05 |
| Target modules | `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
| Epochs | 3 |
| Learning rate | 2×10⁻⁴ |
| Batch size (effective) | 16 (4 per device × 4 gradient accumulation) |
| LR schedule | Cosine |
| Optimizer | AdamW-8bit |
| Max sequence length | 1024 |
| Quantization | 4-bit (NF4) |

### 3. Inference

Simplifications are generated with **greedy decoding** (`max_new_tokens=128`). Special tokens are stripped during post-processing.

### 4. Model Merging

Adapter weights are merged into the base model using Unsloth's `save_pretrained_merged`, producing fully self-contained checkpoints suitable for Gradio deployment without separate adapter loading.

---

## 🔧 Setup & Reproduction

### Requirements

```bash
pip install -r requirements.txt
```

> **Note:** Training requires a GPU (tested on Google Colab A100). For inference only, a T4 is sufficient.

### Running the Notebook

The entire pipeline — data loading, baseline inference, fine-tuning, evaluation, and demo — is contained in a single Jupyter notebook:

```
APP1_project_IkerGutierrez_PaulaGuerrero.ipynb
```

**Steps:**
1. Mount your Google Drive and place `claramed_synt_simp_aligned.tsv` at `MyDrive/APP1project/`.
2. Authenticate with Hugging Face Hub (`notebook_login()`).
3. Run all cells sequentially. Each major section is labelled:
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

## 🔬 Error Analysis

Qualitative inspection of the best model (Qwen-FT-adapter) on the test set reveals three recurring failure modes:

| Failure mode | Description |
|---|---|
| **Low SARI / Low FRE** | Model copies the source almost word-for-word instead of paraphrasing; long compound medical nouns inflate syllable counts, reducing FRE. |
| **Low BERT-F1** | Model introduces inaccurate paraphrases of clinical terminology (e.g. *músculos del vientre* for bladder musculature), creating factual errors. |
| **Lexical divergence** | Model preserves meaning but uses vocabulary that diverges from the reference style, which SARI penalises even when semantics are intact. |

---

## 🔭 Future Work

- **Document-level fine-tuning** using models with larger context windows (>20k tokens) to handle full clinical trial documents rather than isolated sentences.
- **RAG (Retrieval-Augmented Generation)** to ground simplifications in trusted medical terminology databases and improve factual accuracy.
- **Human evaluation** with patients and clinicians to complement automatic metrics.
- **Cross-lingual transfer** to extend the approach to other under-resourced languages.

---

## 📄 Citation

If you use this work, please cite:

```bibtex
@article{guerrero2025clinical,
  title     = {Clinical Text Simplifiers by Fine-Tuning Qwen and Llama with CLARA-MeD},
  author    = {Guerrero Castelló, Paula and Gutierrez Fandiño, Iker},
  year      = {2025},
  institution = {University of the Basque Country (EHU)}
}
```

Also cite the CLARA-MeD corpus:

```bibtex
@inproceedings{campillos2022building,
  title     = {Building a Comparable Corpus and a Benchmark for Spanish Medical Text Simplification},
  author    = {Campillos-Llanos, Leonardo and Terroba Reinares, Ana R. and Zakhir Puig, Sofia and Valverde-Mateos, Ana and Capllonch-Carrion, Adrian},
  journal   = {Procesamiento del Lenguaje Natural},
  number    = {69},
  pages     = {189--196},
  year      = {2022}
}
```

---

## 📚 References

- Campillos-Llanos et al. (2022, 2024). *CLARA-MeD corpus.*
- Hu et al. (2022). *LoRA: Low-Rank Adaptation of Large Language Models.* arXiv:2106.09685.
- Xu et al. (2016). *Optimizing Statistical Machine Translation for Text Simplification.* TACL.
- Zhang et al. (2020). *BERTScore: Evaluating Text Generation with BERT.* ICLR.
- Szigriszt-Pazos (1993). *Sistemas predictivos de legibilidad del mensaje escrito.*

---

## 📝 License

This project is released under the [MIT License](LICENSE).
