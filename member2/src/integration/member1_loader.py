"""
SupplyShield AI
Member 1 → Member 2 Integration Loader

Purpose
-------
Loads the normalized dataset produced by Member 1's Bright Data
supply-webshield pipeline, validates the expected contract, performs
production-grade data quality checks, normalizes types, removes
exact duplicates, and exports a clean Member 2 input dataset.

Upstream:
    member1/supply-webshield/data/processed/unified_supply_data.json

Downstream:
    Member 2 feature engineering / NLP / ML / risk scoring / WebShield

Author:
    SupplyShield AI - Member 2 AI/ML Team
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

# member2/src/integration/member1_loader.py
# parents[0] = integration
# parents[1] = src
# parents[2] = member2
# parents[3] = project root

MEMBER2_DIR = CURRENT_FILE.parents[2]
PROJECT_ROOT = CURRENT_FILE.parents[3]

MEMBER1_DATA_PATH = (
    PROJECT_ROOT
    / "member1"
    / "supply-webshield"
    / "data"
    / "processed"
    / "unified_supply_data.json"
)

MEMBER2_PROCESSED_DIR = MEMBER2_DIR / "data" / "processed"
OUTPUT_PATH = MEMBER2_PROCESSED_DIR / "member1_integrated_supply_data.json"

LOG_DIR = MEMBER2_DIR / "outputs" / "integration"
LOG_PATH = LOG_DIR / "member1_integration.log"


# ============================================================
# EXPECTED MEMBER 1 DATA CONTRACT
# ============================================================

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


# ============================================================
# LOGGING
# ============================================================

def configure_logging() -> logging.Logger:
    """
    Configure both console and file logging.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("member1_integration")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers when notebook/process reloads module.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_PATH,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = configure_logging()


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def safe_json_value(value: Any) -> Any:
    """
    Convert NumPy/Pandas scalar values into JSON-safe Python values.
    """

    if value is None:
        return None

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        if np.isnan(value):
            return None
        return float(value)

    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()

    if isinstance(value, float) and np.isnan(value):
        return None

    return value


def normalize_text(value: Any) -> Any:
    """
    Normalize text fields without destroying legitimate information.
    """

    if value is None:
        return None

    if pd.isna(value):
        return None

    value = str(value).strip()

    if not value:
        return None

    return value


# ============================================================
# LOAD MEMBER 1 DATA
# ============================================================

def load_member1_json(path: Path) -> list[dict[str, Any]]:
    """
    Load Member 1's unified JSON dataset.

    Raises
    ------
    FileNotFoundError
        If the upstream dataset does not exist.

    ValueError
        If the JSON structure is not a list of dictionaries.
    """

    logger.info("Loading Member 1 dataset:")
    logger.info(str(path))

    if not path.exists():
        raise FileNotFoundError(
            f"Member 1 dataset not found:\n{path}\n\n"
            "Make sure Member 1 has generated "
            "unified_supply_data.json."
        )

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Member 1 dataset must contain a JSON list."
        )

    if not data:
        raise ValueError(
            "Member 1 dataset is empty."
        )

    invalid_records = [
        index
        for index, record in enumerate(data)
        if not isinstance(record, dict)
    ]

    if invalid_records:
        raise ValueError(
            f"Invalid records found at indexes: "
            f"{invalid_records[:10]}"
        )

    logger.info(
        "Successfully loaded %d Member 1 records.",
        len(data),
    )

    return data


# ============================================================
# SCHEMA VALIDATION
# ============================================================

def validate_schema(records: list[dict[str, Any]]) -> None:
    """
    Validate the Member 1 → Member 2 data contract.
    """

    actual_columns = set().union(*(record.keys() for record in records))

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    if missing_columns:
        raise ValueError(
            "Member 1 schema validation failed.\n"
            f"Missing columns: {missing_columns}"
        )

    logger.info(
        "Schema validation passed."
    )

    logger.info(
        "Expected contract fields available: %d/%d",
        len(EXPECTED_COLUMNS),
        len(EXPECTED_COLUMNS),
    )


# ============================================================
# DATAFRAME CONVERSION
# ============================================================

def records_to_dataframe(
    records: list[dict[str, Any]],
) -> pd.DataFrame:
    """
    Convert validated records into a DataFrame while preserving
    the expected column order.
    """

    dataframe = pd.DataFrame(records)

    # Guarantee the contract column order.
    for column in EXPECTED_COLUMNS:
        if column not in dataframe.columns:
            dataframe[column] = None

    dataframe = dataframe[EXPECTED_COLUMNS]

    logger.info(
        "Created DataFrame with shape: %s",
        dataframe.shape,
    )

    return dataframe


# ============================================================
# TYPE NORMALIZATION
# ============================================================

def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize data types and text fields.

    This step is deliberately conservative. We do not fabricate
    missing supplier, event, location, availability, or date values.
    """

    df = dataframe.copy()

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
        df[column] = df[column].apply(normalize_text)

    # Numeric conversion.
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce",
    )

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce",
    )

    # Timestamp normalization.
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
        utc=True,
    )

    # Date may contain incomplete or inconsistent values.
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        utc=True,
    )

    # Remove impossible negative prices.
    negative_price_mask = df["price"] < 0

    negative_price_count = int(
        negative_price_mask.fillna(False).sum()
    )

    if negative_price_count:
        logger.warning(
            "Found %d negative prices. Converting them to missing values.",
            negative_price_count,
        )

        df.loc[negative_price_mask, "price"] = np.nan

    # Rating should normally be within 0-5.
    invalid_rating_mask = (
        df["rating"].notna()
        & ~df["rating"].between(0, 5)
    )

    invalid_rating_count = int(
        invalid_rating_mask.sum()
    )

    if invalid_rating_count:
        logger.warning(
            "Found %d out-of-range ratings. "
            "Converting them to missing values.",
            invalid_rating_count,
        )

        df.loc[invalid_rating_mask, "rating"] = np.nan

    return df


# ============================================================
# DATA QUALITY ANALYSIS
# ============================================================

def generate_quality_report(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate a machine-readable data quality report.
    """

    df = dataframe

    missing_counts = df.isna().sum()

    missing_percentages = (
        (missing_counts / len(df)) * 100
    ).round(2)

    report = {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "row_count": int(len(df)),

        "column_count": int(len(df.columns)),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "missing_values": {
            str(column): int(count)
            for column, count
            in missing_counts.items()
        },

        "missing_percentage": {
            str(column): float(value)
            for column, value
            in missing_percentages.items()
        },

        "sources": {
            str(key): int(value)
            for key, value
            in df["source"]
            .value_counts(dropna=False)
            .items()
        },

        "numeric_summary": {
            "price_available": int(
                df["price"].notna().sum()
            ),
            "rating_available": int(
                df["rating"].notna().sum()
            ),
        },
    }

    return report


# ============================================================
# DEDUPLICATION
# ============================================================

def deduplicate_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove exact duplicate records.

    URL-based deduplication is used where possible because
    the same product can appear with slightly different metadata.
    """

    df = dataframe.copy()

    before = len(df)

    # First remove exact duplicates.
    df = df.drop_duplicates(
        keep="first"
    ).reset_index(drop=True)

    exact_duplicates_removed = before - len(df)

    logger.info(
        "Exact duplicates removed: %d",
        exact_duplicates_removed,
    )

    # Remove duplicate URLs only when URLs are present.
    valid_url_mask = (
        df["url"].notna()
        & df["url"].astype(str).str.strip().ne("")
    )

    duplicate_url_count = int(
        df.loc[valid_url_mask, "url"]
        .duplicated()
        .sum()
    )

    if duplicate_url_count:
        df = df.drop_duplicates(
            subset=["url"],
            keep="first",
        ).reset_index(drop=True)

    logger.info(
        "Duplicate URLs removed: %d",
        duplicate_url_count,
    )

    logger.info(
        "Final record count after deduplication: %d",
        len(df),
    )

    return df


# ============================================================
# EXPORT
# ============================================================

def dataframe_to_records(
    dataframe: pd.DataFrame,
) -> list[dict[str, Any]]:
    """
    Convert DataFrame to JSON-safe records.
    """

    records = []

    for record in dataframe.to_dict(
        orient="records"
    ):
        cleaned_record = {
            key: safe_json_value(value)
            for key, value in record.items()
        }

        records.append(cleaned_record)

    return records


def save_integrated_dataset(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Save the validated Member 1 → Member 2 dataset.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = dataframe_to_records(
        dataframe
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False,
        )

    logger.info(
        "Integrated dataset saved to:"
    )

    logger.info(
        str(output_path)
    )


# ============================================================
# MAIN INTEGRATION PIPELINE
# ============================================================

def run_integration() -> pd.DataFrame:
    """
    Execute the complete Member 1 → Member 2 integration.

    Returns
    -------
    pd.DataFrame
        Clean, validated, normalized Member 2 input dataset.
    """

    logger.info("=" * 70)
    logger.info("SUPPLYSHIELD AI — MEMBER 1 → MEMBER 2 INTEGRATION")
    logger.info("=" * 70)

    # --------------------------------------------------------
    # 1. Load
    # --------------------------------------------------------

    records = load_member1_json(
        MEMBER1_DATA_PATH
    )

    # --------------------------------------------------------
    # 2. Validate contract
    # --------------------------------------------------------

    validate_schema(
        records
    )

    # --------------------------------------------------------
    # 3. Convert to DataFrame
    # --------------------------------------------------------

    dataframe = records_to_dataframe(
        records
    )

    # --------------------------------------------------------
    # 4. Normalize types
    # --------------------------------------------------------

    dataframe = normalize_dataframe(
        dataframe
    )

    # --------------------------------------------------------
    # 5. Remove duplicates
    # --------------------------------------------------------

    dataframe = deduplicate_dataframe(
        dataframe
    )

    # --------------------------------------------------------
    # 6. Quality report
    # --------------------------------------------------------

    quality_report = generate_quality_report(
        dataframe
    )

    logger.info(
        "Data quality summary:"
    )

    logger.info(
        "Rows: %d",
        quality_report["row_count"],
    )

    logger.info(
        "Columns: %d",
        quality_report["column_count"],
    )

    logger.info(
        "Duplicate rows: %d",
        quality_report["duplicate_rows"],
    )

    logger.info(
        "Sources: %s",
        quality_report["sources"],
    )

    # --------------------------------------------------------
    # 7. Save integration output
    # --------------------------------------------------------

    save_integrated_dataset(
        dataframe,
        OUTPUT_PATH,
    )

    # --------------------------------------------------------
    # 8. Final validation
    # --------------------------------------------------------

    if dataframe.empty:
        raise ValueError(
            "Integration produced an empty dataset."
        )

    missing_contract_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_contract_columns:
        raise RuntimeError(
            "Final integration validation failed: "
            f"{missing_contract_columns}"
        )

    logger.info("=" * 70)
    logger.info("INTEGRATION COMPLETED SUCCESSFULLY")
    logger.info(
        "Final dataset shape: %s",
        dataframe.shape,
    )
    logger.info("=" * 70)

    return dataframe


# ============================================================
# CLI ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        final_dataframe = run_integration()

        print("\n")
        print("=" * 70)
        print("MEMBER 1 → MEMBER 2 INTEGRATION SUCCESS")
        print("=" * 70)

        print(
            f"Records available : {len(final_dataframe)}"
        )

        print(
            f"Columns available : {len(final_dataframe.columns)}"
        )

        print(
            f"Output file       : {OUTPUT_PATH}"
        )

        print("\nColumns:")
        print(
            ", ".join(final_dataframe.columns)
        )

        print("\nFirst integrated record:")
        print(
            json.dumps(
                dataframe_to_records(
                    final_dataframe.head(1)
                )[0],
                indent=2,
                ensure_ascii=False,
            )
        )

        print("\nSTATUS: READY FOR MEMBER 2 AI/ML PIPELINE")

    except Exception as exc:

        logger.exception(
            "Member 1 → Member 2 integration failed."
        )

        print("\n")
        print("=" * 70)
        print("INTEGRATION FAILED")
        print("=" * 70)
        print(f"ERROR: {exc}")

        raise