# Paper

This directory contains the short paper: **"Clinical text simplifiers by fine-tuning Qwen and Llama with CLARA-MeD"**    

Authors: *Paula Guerrero Castelló & Iker Gutierrez Fandiño*    
University of the Basque Country (UPV/EHU)

## Abstract

This paper presents two models for clinical ATS (automatic text simplification) in Spanish. Clinical ATS can facilitate reading comprehension for health students and patients without medical knowledge. We fine-tune Qwen3.5-0.8B and Llama3.2-1B-Instruct on the Clara-MeD corpus using Low-Rank Adaptation (LoRA). For each fine-tuned adapter, we also create a merged version by integrating the adapter weights with the base model. Baseline, adapter, and merged models are evaluated against a human reference using three automatic metrics: SARI, BERTScore (F1), and Flesch-Szigriszt Reading Ease (FRE). Fine-tuning (FT) is performed at the sentence level. FT models consistently outperform their respective baselines across all metrics and obtain results comparable to the human expert reference: they surpass it in meaning preservation (BERT-F1) but perform slightly worse in readability (FRE). Among all FT model variants, Qwen-FT-adapter shows slightly better performance, achieving a balance between meaning preservation (BERT-F1 89.30), complexity reduction (FRE 49.75), and human-like simplification (SARI 57.73). Merged models are integrated into a user-friendly interface for public deployment on Hugging Face Spaces. The code repository and model demos are openly accessible in Appendix A.

