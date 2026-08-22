"""
SupplyShield AI
Member 2 - Data Loading & Preprocessing

Purpose
-------
Loads Member 1's trusted unified supply-chain dataset and converts it
into an analysis-ready Pandas DataFrame.

Important
---------
This module DOES NOT modify Member 1's files.
The original JSON remains the source of truth.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

UNIFIED_DATA_PATH = (
    PROJECT_ROOT
    / "member1"
    / "supply-webshield"
    / "data"
    / "processed"
    / "unified_supply_data.json"
)


EXPECTED_COLUMNS = [
    "source",
    "title",
    "company",
    "supplier",
    "product",
    "event",
    "location",
    "price",
    "currency",
    "availability",
    "rating",
    "review",
    "date",
    "url",
    "timestamp",
]


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

logger = logging.getLogger("supplyshield.data_loader")

if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------------------------------------------------------------------
# JSON Loading
# ---------------------------------------------------------------------

def load_json_records(file_path: Path | str = UNIFIED_DATA_PATH) -> list[dict[str, Any]]:
    """
    Load the unified JSON dataset.

    Parameters
    ----------
    file_path:
        Path to the unified JSON file.

    Returns
    -------
    list[dict]
        List of supply-chain records.

    Raises
    ------
    FileNotFoundError
        If the dataset does not exist.

    ValueError
        If the JSON structure is invalid.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Unified dataset not found at:\n{path}"
        )

    logger.info("Loading unified dataset: %s", path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Expected the unified dataset to contain a JSON list of records."
        )

    valid_records = [
        record
        for record in data
        if isinstance(record, dict)
    ]

    logger.info(
        "Loaded %d records (%d valid dictionary records).",
        len(data),
        len(valid_records),
    )

    return valid_records


# ---------------------------------------------------------------------
# DataFrame Creation
# ---------------------------------------------------------------------

def records_to_dataframe(
    records: list[dict[str, Any]],
) -> pd.DataFrame:
    """
    Convert JSON records into a Pandas DataFrame.
    """

    if not records:
        raise ValueError("No valid records were found in the dataset.")

    df = pd.DataFrame(records)

    logger.info(
        "Created DataFrame with shape: %s",
        df.shape,
    )

    return df


# ---------------------------------------------------------------------
# Column Standardization
# ---------------------------------------------------------------------

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names without changing business meaning.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


# ---------------------------------------------------------------------
# Text Cleaning
# ---------------------------------------------------------------------

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean textual fields conservatively.

    We intentionally do NOT aggressively remove punctuation,
    because the NLP pipeline will later need the original text.
    """

    df = df.copy()

    text_columns = [
        "source",
        "title",
        "company",
        "supplier",
        "product",
        "event",
        "location",
        "currency",
        "availability",
        "review",
        "url",
    ]

    for column in text_columns:

        if column not in df.columns:
            continue

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # Normalize empty-like values.
        df[column] = df[column].replace(
            {
                "nan": "",
                "None": "",
                "null": "",
                "NULL": "",
            }
        )

    return df


# ---------------------------------------------------------------------
# Numeric Conversion
# ---------------------------------------------------------------------

def convert_numeric_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric fields to appropriate numeric types.

    Invalid values become NaN instead of crashing the pipeline.
    """

    df = df.copy()

    numeric_columns = [
        "price",
        "rating",
    ]

    for column in numeric_columns:

        if column not in df.columns:
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    return df


# ---------------------------------------------------------------------
# Date / Timestamp Conversion
# ---------------------------------------------------------------------

def convert_datetime_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date and timestamp columns into Pandas datetime objects.
    """

    df = df.copy()

    for column in ["date", "timestamp"]:

        if column not in df.columns:
            continue

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce",
            utc=True,
        )

    return df


# ---------------------------------------------------------------------
# Duplicate Detection
# ---------------------------------------------------------------------

def remove_exact_duplicates(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int]:
    """
    Remove exact duplicate rows.

    Returns
    -------
    cleaned_dataframe, number_of_duplicates_removed
    """

    before = len(df)

    df = df.drop_duplicates().reset_index(drop=True)

    removed = before - len(df)

    logger.info(
        "Exact duplicate rows removed: %d",
        removed,
    )

    return df, removed


# ---------------------------------------------------------------------
# Missing Value Analysis
# ---------------------------------------------------------------------

def generate_quality_report(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate a column-level data quality report.
    """

    total_rows = len(df)

    report = []

    for column in df.columns:

        missing_count = int(df[column].isna().sum())

        # Empty strings should also count as missing for text fields.
        if df[column].dtype == "object":
            empty_count = int(
                df[column]
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )
        else:
            empty_count = 0

        effective_missing = missing_count + empty_count

        missing_percentage = (
            effective_missing / total_rows * 100
            if total_rows > 0
            else 0
        )

        report.append(
            {
                "column": column,
                "dtype": str(df[column].dtype),
                "missing_count": effective_missing,
                "missing_percentage": round(
                    missing_percentage,
                    2,
                ),
                "unique_values": int(
                    df[column].nunique(dropna=True)
                ),
            }
        )

    return pd.DataFrame(report).sort_values(
        by="missing_percentage",
        ascending=False,
    ).reset_index(drop=True)


# ---------------------------------------------------------------------
# Complete Preprocessing Pipeline
# ---------------------------------------------------------------------

def prepare_dataset(
    file_path: Path | str = UNIFIED_DATA_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """
    Complete Member 2 data preparation pipeline.

    Returns
    -------
    df:
        Clean analysis-ready DataFrame.

    quality_report:
        Column-level data quality report.

    metadata:
        Dataset-level metadata and processing statistics.
    """

    # 1. Load
    records = load_json_records(file_path)

    # 2. DataFrame
    df = records_to_dataframe(records)

    original_rows = len(df)

    # 3. Standardize column names
    df = standardize_columns(df)

    # 4. Ensure expected columns exist
    for column in EXPECTED_COLUMNS:

        if column not in df.columns:
            df[column] = pd.NA

    # Keep any additional columns generated by Member 1.
    # We do NOT silently delete them.

    # 5. Text cleaning
    df = clean_text_columns(df)

    # 6. Numeric conversion
    df = convert_numeric_fields(df)

    # 7. Date conversion
    df = convert_datetime_fields(df)

    # 8. Remove exact duplicates
    df, duplicates_removed = remove_exact_duplicates(df)

    # 9. Reset index
    df = df.reset_index(drop=True)

    # 10. Quality report
    quality_report = generate_quality_report(df)

    # 11. Metadata
    metadata = {
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicates_removed": duplicates_removed,
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "source_distribution": (
            df["source"]
            .value_counts(dropna=False)
            .to_dict()
            if "source" in df.columns
            else {}
        ),
    }

    logger.info(
        "Final dataset shape: %s",
        df.shape,
    )

    return df, quality_report, metadata


# ---------------------------------------------------------------------
# Quick Command-Line Test
# ---------------------------------------------------------------------

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("SUPPLYSHIELD AI — MEMBER 2 DATA LOADER")
    print("=" * 70)

    dataframe, quality, metadata = prepare_dataset()

    print("\nDATASET SUMMARY")
    print("-" * 70)
    print(f"Original rows      : {metadata['original_rows']}")
    print(f"Final rows         : {metadata['final_rows']}")
    print(f"Duplicates removed : {metadata['duplicates_removed']}")
    print(f"Columns            : {metadata['column_count']}")

    print("\nSOURCE DISTRIBUTION")
    print("-" * 70)

    for source, count in metadata["source_distribution"].items():
        print(f"{source}: {count}")

    print("\nDATA TYPES")
    print("-" * 70)
    print(dataframe.dtypes.to_string())

    print("\nDATA QUALITY")
    print("-" * 70)
    print(quality.to_string(index=False))

    print("\nFIRST 5 RECORDS")
    print("-" * 70)
    print(dataframe.head().to_string())

    print("\n" + "=" * 70)
    print("DATA LOADER TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)