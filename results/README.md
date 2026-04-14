# Results

This directory contains the prediction CSV files for each of the six system variants, along with the evaluation metrics table computed on the test set.

| File | Description |
|------|-------------|
| `01_baseline_llama_inference.csv` | Zero-shot Llama-3.2-1B-Instruct predictions on the test set |
| `02_llama_finetuned_predictions.csv` | Llama FT-adapter predictions on the test set |
| `03_qwen_finetuned_predictions.csv` | Zero-shot Qwen3.5-0.8B predictions on the test set |
| `04_qwen_baseline_predictions.csv` | Zero-shot Qwen3.5-0.8B predictions on the test set |
| `05_qwen_finetuned_predictions.csv` | Qwen FT-adapter predictions on the test set |
| `06_merged_llama_finetuned_predictions.csv` | Llama FT-merged predictions on the test set |
| `07_merged_qwen_finetuned_predictions.csv` | Qwen FT-merged predictions on the test set |
| `metrics_results.csv` | Aggregated SARI, BERT-F1, FRE scores for all models |

## CSV format (prediction files)

Each prediction CSV contains three columns:

```
source      — original complex sentence
reference   — expert simplified sentence
prediction  — model output
```

