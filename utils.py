import pandas as pd
from pathlib import Path
from typing import Optional


# -------------------------------------------------
# Safe CSV Loader
# -------------------------------------------------
def load_csv_safe(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV file safely.
    Returns an empty DataFrame if file is missing or unreadable.
    """
    path = Path(file_path)

    if not path.exists():
        print(f"[WARN] CSV file not found: {file_path}")
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"[ERROR] Failed to load CSV {file_path}: {e}")
        return pd.DataFrame()


# -------------------------------------------------
# Helper: Normalize Strings
# -------------------------------------------------
def normalize_text(value: Optional[str]) -> str:
    """
    Normalizes text for safe comparison.
    """
    if not value:
        return ""
    return value.strip().lower()

import numpy as np


def make_json_serializable(obj):
    """
    Recursively convert numpy / pandas types to native Python types
    so json.dumps() does not fail.
    """
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_json_serializable(v) for v in obj]

    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    return obj

