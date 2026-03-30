"""
Data loading and preprocessing utilities for the ClaraMed dataset.

Expected TSV columns:
    FILE_ID | SOURCE | SYNT_SIMPLIFIED | SYNT_LEX_SIMPLIFIED

The model is trained on SOURCE → SYNT_LEX_SIMPLIFIED pairs, which combine
both syntactic and lexical simplification.
"""

import pandas as pd
from sklearn.model_selection import train_test_split

from prompts import make_train_prompt, make_inference_prompt


def load_and_split_dataset(
    path: str,
    test_size: float = 0.10,
    val_size: float = 0.10,
    seed: int = 42,
):
    """
    Load the ClaraMed TSV and split into train / val / test.

    Returns
    -------
    X_train, X_val, X_test, y_train, y_val, y_test
        Each is a pandas Series of strings.
    """
    df = pd.read_csv(path, sep="\t")
    print(f"Loaded {len(df)} rows from {path}")

    X = df["SOURCE"]
    y = df["SYNT_LEX_SIMPLIFIED"]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=(test_size + val_size), random_state=seed
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=seed
    )

    print(f"Split: Train={len(X_train)} | Val={len(X_val)} | Test={len(X_test)}")
    return X_train, X_val, X_test, y_train, y_val, y_test


def build_hf_datasets(X_train, X_val, y_train, y_val):
    """
    Convert split Series into HuggingFace Dataset objects with
    formatted prompt strings.
    """
    from datasets import Dataset

    train_prompts = [make_train_prompt(src, simp)
                     for src, simp in zip(X_train, y_train)]
    val_prompts = [make_train_prompt(src, simp)
                   for src, simp in zip(X_val, y_val)]

    return (
        Dataset.from_dict({"text": train_prompts}),
        Dataset.from_dict({"text": val_prompts}),
    )
