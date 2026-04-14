# Paper

This directory contains the short paper:

**"Clinical Text Simplifiers by Fine-Tuning Qwen and Llama with CLARA-MeD"**    

Authors: *Paula Guerrero Castelló & Iker Gutierrez Fandiño*    
University of the Basque Country (UPV/EHU)

## Abstract

This paper presents two models for clinical
automatic text simplification (ATS) in
Spanish. Clinical ATS can facilitate reading
compre- hension for patients without medical
knowledge or health students. We fine-tune
Qwen3.5-0.8B and Llama3.2-1B-Instruct on
the Clara-MeD corpus using Low-Rank Adaptation
(LoRA). For each fine-tuned adapter,
we also create a merged version by integrating
the adapter weights with the base model.
Baseline, adapter and merged models are evaluated
against the human reference using three
automatic metrics: SARI, BERTScore (F1),
and Flesch-szigriszt Reading Ease (FRE). Finetuning
(FT) is performed at the sentence level.
FT models consistently outperform their respective
baselines across all metrics and remarkably
obtain similar results compared to the human
expert reference: they surpass it in meaning
preservation (BERT-F1) but performance in
readability (FRE) is slightly worse. Among
all model variants, the Qwen-FT-adapter shows
slightly better performance, achieving a balance
between meaning preservation (BERT-F1
89.30), complexity reduction (FRE 49.75) and
fluency (SARI 57.73). Merged models have
been integrated into a user-friendly interface for
public deployment on HuggingFace.
