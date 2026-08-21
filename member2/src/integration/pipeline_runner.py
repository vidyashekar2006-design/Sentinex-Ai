"""
SupplyShield AI
============================================================

Production Pipeline Runner
Member 2 - AI/ML Integration Layer

Pipeline:

    MEMBER 1
        ↓
    unified_supply_data.json
        ↓
    Input Validation
        ↓
    DataFrame Construction
        ↓
    Data Quality Checks
        ↓
    MEMBER 2 ML PIPELINE
        ↓
    Feature Engineering
        ↓
    Anomaly Detection
        ↓
    NLP Risk Signals
        ↓
    WebShield
        ↓
    Risk Scoring
        ↓
    Explainability
        ↓
    Final Integrated Output

This file is the production orchestration layer.

The actual AI/ML processing is implemented in:

    member2/src/integration/ml_pipeline.py
"""

from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd


# ============================================================
# 1. PROJECT PATH CONFIGURATION
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

# pipeline_runner.py
#
# member2/
# └── src/
#     └── integration/
#         └── pipeline_runner.py
#
# parents[0] = integration
# parents[1] = src
# parents[2] = member2
# parents[3] = project root

MEMBER2_DIR = CURRENT_FILE.parents[2]

PROJECT_ROOT = CURRENT_FILE.parents[3]

DATA_DIR = MEMBER2_DIR / "data"

PROCESSED_DIR = DATA_DIR / "processed"

OUTPUT_DIR = MEMBER2_DIR / "outputs"


# ------------------------------------------------------------
# IMPORTANT
# ------------------------------------------------------------
# The successful Member 1 integration produces:
#
# member2/data/processed/
#     member1_integrated_supply_data.json
#
# We prefer that file because it is already validated by
# member1_loader.py.
#
# If it does not exist, we fall back to the original
# Member 1 unified dataset.
# ------------------------------------------------------------

INTEGRATED_MEMBER1_FILE = (
    PROCESSED_DIR
    / "member1_integrated_supply_data.json"
)

ORIGINAL_MEMBER1_FILE = (
    PROJECT_ROOT
    / "member1"
    / "supply-webshield"
    / "data"
    / "processed"
    / "unified_supply_data.json"
)

FINAL_OUTPUT_FILE = (
    OUTPUT_DIR
    / "final_supplyshield_output.json"
)

FINAL_CSV_FILE = (
    OUTPUT_DIR
    / "final_supplyshield_output.csv"
)

PIPELINE_SUMMARY_FILE = (
    OUTPUT_DIR
    / "pipeline_summary.json"
)


# ============================================================
# 2. LOGGING
# ============================================================

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(
    "SupplyShield.Member2.ProductionPipeline"
)


# ============================================================
# 3. DISPLAY HELPERS
# ============================================================

def print_section(
    title: str,
) -> None:
    """
    Print a consistent terminal section.
    """

    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def print_status(
    message: str,
    success: bool = True,
) -> None:
    """
    Print a professional pipeline status line.
    """

    symbol = "✓" if success else "✗"

    print(
        f"{symbol} {message}"
    )


# ============================================================
# 4. DIRECTORY INITIALIZATION
# ============================================================

def ensure_directories() -> None:
    """
    Create required output directories.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "Required directories verified."
    )


# ============================================================
# 5. IMPORT ML PIPELINE
# ============================================================

def import_ml_pipeline():
    """
    Import the Member 2 ML pipeline safely.

    The function supports execution from the project root:

        python member2/src/integration/pipeline_runner.py

    """

    try:

        from ml_pipeline import (
            SupplyShieldMLPipeline,
            generate_pipeline_summary,
        )

        logger.info(
            "ML pipeline module imported successfully."
        )

        return (
            SupplyShieldMLPipeline,
            generate_pipeline_summary,
        )

    except ImportError as direct_import_error:

        logger.warning(
            "Direct ML pipeline import failed: %s",
            direct_import_error,
        )

        # ----------------------------------------------------
        # Fallback: explicitly add integration directory
        # ----------------------------------------------------

        integration_directory = (
            CURRENT_FILE.parent
        )

        integration_directory_string = str(
            integration_directory
        )

        if (
            integration_directory_string
            not in sys.path
        ):

            sys.path.insert(
                0,
                integration_directory_string,
            )

        try:

            from ml_pipeline import (
                SupplyShieldMLPipeline,
                generate_pipeline_summary,
            )

            logger.info(
                "ML pipeline imported using fallback path."
            )

            return (
                SupplyShieldMLPipeline,
                generate_pipeline_summary,
            )

        except ImportError as fallback_error:

            raise ImportError(
                "\n"
                "Could not import ml_pipeline.py.\n\n"
                "Expected file:\n"
                f"{CURRENT_FILE.parent / 'ml_pipeline.py'}\n\n"
                f"Original error: {direct_import_error}\n"
                f"Fallback error: {fallback_error}"
            ) from fallback_error


# ============================================================
# 6. LOAD MEMBER 1 DATA
# ============================================================

def load_member1_dataset() -> list[dict[str, Any]]:
    """
    Load the validated Member 1 dataset.

    Preferred source:

        member2/data/processed/
        member1_integrated_supply_data.json

    Fallback source:

        member1/supply-webshield/data/processed/
        unified_supply_data.json
    """

    print_section(
        "STAGE 1 — MEMBER 1 DATA LOADING"
    )

    # --------------------------------------------------------
    # Select input
    # --------------------------------------------------------

    if INTEGRATED_MEMBER1_FILE.exists():

        input_file = (
            INTEGRATED_MEMBER1_FILE
        )

        logger.info(
            "Using validated Member 1 integration output."
        )

    elif ORIGINAL_MEMBER1_FILE.exists():

        input_file = (
            ORIGINAL_MEMBER1_FILE
        )

        logger.info(
            "Validated integration output not found."
        )

        logger.info(
            "Using original Member 1 unified dataset."
        )

    else:

        raise FileNotFoundError(
            "\n"
            "No Member 1 dataset was found.\n\n"
            "Checked:\n"
            f"1. {INTEGRATED_MEMBER1_FILE}\n"
            f"2. {ORIGINAL_MEMBER1_FILE}"
        )

    logger.info(
        "Input file: %s",
        input_file,
    )

    # --------------------------------------------------------
    # Load JSON
    # --------------------------------------------------------

    try:

        with input_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Member 1 JSON file is invalid."
        ) from exc

    # --------------------------------------------------------
    # Normalize top-level structure
    # --------------------------------------------------------

    if isinstance(data, list):

        records = data

    elif isinstance(data, dict):

        records = [data]

    else:

        raise TypeError(
            "Member 1 dataset must contain "
            "a JSON list or dictionary."
        )

    # --------------------------------------------------------
    # Validate records
    # --------------------------------------------------------

    valid_records = [
        record
        for record in records
        if isinstance(record, dict)
    ]

    if not valid_records:

        raise ValueError(
            "No valid dictionary records were found."
        )

    logger.info(
        "Loaded %d records.",
        len(valid_records),
    )

    print_status(
        f"Member 1 records loaded: {len(valid_records)}"
    )

    return valid_records


# ============================================================
# 7. INPUT VALIDATION
# ============================================================

def validate_input_records(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Validate the core Member 1 → Member 2 data contract.
    """

    print_section(
        "STAGE 2 — INPUT VALIDATION"
    )

    required_fields = {
        "source",
        "title",
        "product",
    }

    valid_records = []

    rejected_count = 0

    for record in records:

        if not isinstance(
            record,
            dict,
        ):

            rejected_count += 1

            continue

        missing_fields = (
            required_fields
            - set(record.keys())
        )

        if missing_fields:

            rejected_count += 1

            continue

        valid_records.append(
            record
        )

    if not valid_records:

        raise ValueError(
            "No valid records remain after validation."
        )

    logger.info(
        "Input records: %d",
        len(records),
    )

    logger.info(
        "Valid records: %d",
        len(valid_records),
    )

    logger.info(
        "Rejected records: %d",
        rejected_count,
    )

    print_status(
        f"Valid records: {len(valid_records)}"
    )

    print_status(
        f"Rejected records: {rejected_count}"
    )

    return valid_records


# ============================================================
# 8. DATAFRAME CONSTRUCTION
# ============================================================

def records_to_dataframe(
    records: list[dict[str, Any]],
) -> pd.DataFrame:
    """
    Convert Member 1 records into a canonical DataFrame.
    """

    print_section(
        "STAGE 3 — DATAFRAME CONSTRUCTION"
    )

    df = pd.DataFrame(
        records
    )

    expected_columns = [
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

    for column in expected_columns:

        if column not in df.columns:

            df[column] = pd.NA

    logger.info(
        "DataFrame shape: %s",
        df.shape,
    )

    print_status(
        f"DataFrame created: {df.shape}"
    )

    return df


# ============================================================
# 9. SAFE CANONICALIZATION
# ============================================================

def canonicalize_value(
    value: Any,
) -> Any:
    """
    Convert nested values into hashable representations.

    Handles:

        list
        tuple
        dictionary
        set
        NumPy arrays
        Pandas missing values
    """

    if value is None:

        return None

    if value is pd.NA:

        return None

    if isinstance(
        value,
        dict,
    ):

        return tuple(
            sorted(
                (
                    str(key),
                    canonicalize_value(item),
                )
                for key, item
                in value.items()
            )
        )

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):

        return tuple(
            canonicalize_value(item)
            for item in value
        )

    if isinstance(
        value,
        set,
    ):

        return tuple(
            sorted(
                (
                    canonicalize_value(item)
                    for item in value
                ),
                key=str,
            )
        )

    if hasattr(
        value,
        "tolist",
    ):

        try:

            return canonicalize_value(
                value.tolist()
            )

        except Exception:

            pass

    try:

        missing = pd.isna(
            value
        )

        if (
            isinstance(
                missing,
                bool,
            )
            and missing
        ):

            return None

    except Exception:

        pass

    return value


# ============================================================
# 10. DATA QUALITY
# ============================================================

def run_data_quality_checks(
    df: pd.DataFrame,
) -> None:
    """
    Perform production-safe quality checks.
    """

    print_section(
        "STAGE 4 — DATA QUALITY CHECK"
    )

    print(
        f"Rows    : {len(df)}"
    )

    print(
        f"Columns : {len(df.columns)}"
    )

    # --------------------------------------------------------
    # Detect complex columns
    # --------------------------------------------------------

    complex_columns = []

    for column in df.columns:

        try:

            has_complex = df[
                column
            ].apply(
                lambda value:
                isinstance(
                    value,
                    (
                        list,
                        dict,
                        tuple,
                        set,
                    ),
                )
            ).any()

        except Exception:

            has_complex = False

        if has_complex:

            complex_columns.append(
                column
            )

    # --------------------------------------------------------
    # Duplicate detection
    # --------------------------------------------------------

    safe_df = df.copy()

    for column in safe_df.columns:

        safe_df[column] = (
            safe_df[column]
            .map(
                canonicalize_value
            )
        )

    try:

        duplicate_count = int(
            safe_df
            .duplicated()
            .sum()
        )

    except Exception:

        duplicate_count = 0

    print(
        f"Duplicate rows: {duplicate_count}"
    )

    print(
        "Complex-value columns: "
        f"{len(complex_columns)}"
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    missing_percentage = (
        df.isna()
        .mean()
        .mul(100)
        .sort_values(
            ascending=False
        )
    )

    print()
    print(
        "Top missing-value columns:"
    )

    print(
        missing_percentage
        .head(10)
        .round(2)
        .to_string()
    )

    print()

    print_status(
        "Data quality checks completed."
    )


# ============================================================
# 11. RUN REAL MEMBER 2 ML PIPELINE
# ============================================================

def run_ml_pipeline(
    df: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    dict[str, Any],
]:
    """
    Execute the actual Member 2 ML pipeline
    against the real Member 1 dataset.
    """

    print_section(
        "STAGE 5 — MEMBER 2 AI/ML PIPELINE"
    )

    (
        SupplyShieldMLPipeline,
        generate_pipeline_summary,
    ) = import_ml_pipeline()

    logger.info(
        "Initializing SupplyShield ML Pipeline."
    )

    pipeline = (
        SupplyShieldMLPipeline()
    )

    print_status(
        "ML pipeline initialized."
    )

    # --------------------------------------------------------
    # Execute all ML stages
    # --------------------------------------------------------

    processed_df = pipeline.run(
        df
    )

    # --------------------------------------------------------
    # Generate summary
    # --------------------------------------------------------

    summary = (
        generate_pipeline_summary(
            processed_df
        )
    )

    print()
    print(
        "AI/ML PROCESSING RESULTS"
    )

    print("-" * 72)

    print(
        f"Records processed : "
        f"{summary.get('records_processed', 0)}"
    )

    print(
        f"Average risk      : "
        f"{summary.get('average_risk_score', 0)}"
    )

    print(
        f"Maximum risk      : "
        f"{summary.get('maximum_risk_score', 0)}"
    )

    print(
        f"Minimum risk      : "
        f"{summary.get('minimum_risk_score', 0)}"
    )

    print(
        f"High risk         : "
        f"{summary.get('high_risk_records', 0)}"
    )

    print(
        f"Medium risk       : "
        f"{summary.get('medium_risk_records', 0)}"
    )

    print(
        f"Low risk          : "
        f"{summary.get('low_risk_records', 0)}"
    )

    print(
        f"WebShield alerts  : "
        f"{summary.get('webshield_alerts', 0)}"
    )

    print(
        f"Anomaly records   : "
        f"{summary.get('anomaly_records', 0)}"
    )

    print("-" * 72)

    print_status(
        "Feature engineering completed."
    )

    print_status(
        "Anomaly detection completed."
    )

    print_status(
        "NLP risk analysis completed."
    )

    print_status(
        "WebShield analysis completed."
    )

    print_status(
        "Risk scoring completed."
    )

    print_status(
        "Risk explanations generated."
    )

    return (
        processed_df,
        summary,
    )


# ============================================================
# 12. FINAL OUTPUT VALIDATION
# ============================================================

def validate_final_output(
    df: pd.DataFrame,
) -> None:
    """
    Validate the AI/ML output schema before export.
    """

    print_section(
        "STAGE 6 — FINAL OUTPUT VALIDATION"
    )

    required_output_columns = [
        "overall_risk_score",
        "risk_category",
        "risk_explanation",
        "anomaly_score",
        "nlp_risk_score",
        "webshield_risk_score",
        "supply_chain_risk_score",
    ]

    missing_columns = [
        column
        for column
        in required_output_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Final ML output is missing required "
            f"columns: {missing_columns}"
        )

    if df.empty:

        raise ValueError(
            "Final ML output is empty."
        )

    # --------------------------------------------------------
    # Risk score validation
    # --------------------------------------------------------

    risk_scores = pd.to_numeric(
        df["overall_risk_score"],
        errors="coerce",
    )

    invalid_risk_scores = (
        risk_scores.isna()
        | ~risk_scores.between(
            0,
            100,
        )
    ).sum()

    if invalid_risk_scores:

        raise ValueError(
            f"{invalid_risk_scores} records contain "
            "invalid overall risk scores."
        )

    print_status(
        "Required ML output columns verified."
    )

    print_status(
        "Risk score range validated: 0–100."
    )

    print_status(
        "Final output is non-empty."
    )


# ============================================================
# 13. SAVE FINAL JSON
# ============================================================

def save_final_json(
    df: pd.DataFrame,
) -> Path:
    """
    Save final integrated AI/ML output as JSON.
    """

    records = (
        df.where(
            pd.notna(df),
            None,
        )
        .to_dict(
            orient="records"
        )
    )

    with FINAL_OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    logger.info(
        "Final JSON saved: %s",
        FINAL_OUTPUT_FILE,
    )

    return FINAL_OUTPUT_FILE


# ============================================================
# 14. SAVE FINAL CSV
# ============================================================

def save_final_csv(
    df: pd.DataFrame,
) -> Path:
    """
    Save final integrated AI/ML output as CSV.

    Complex Python objects are serialized as strings.
    """

    export_df = df.copy()

    for column in export_df.columns:

        export_df[column] = (
            export_df[column]
            .map(
                lambda value:
                json.dumps(
                    value,
                    ensure_ascii=False,
                )
                if isinstance(
                    value,
                    (
                        list,
                        dict,
                        tuple,
                        set,
                    ),
                )
                else value
            )
        )

    export_df.to_csv(
        FINAL_CSV_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    logger.info(
        "Final CSV saved: %s",
        FINAL_CSV_FILE,
    )

    return FINAL_CSV_FILE


# ============================================================
# 15. SAVE PIPELINE SUMMARY
# ============================================================

def save_pipeline_summary(
    summary: dict[str, Any],
) -> Path:
    """
    Save machine-readable pipeline metrics.
    """

    with PIPELINE_SUMMARY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    logger.info(
        "Pipeline summary saved: %s",
        PIPELINE_SUMMARY_FILE,
    )

    return PIPELINE_SUMMARY_FILE


# ============================================================
# 16. MAIN PRODUCTION PIPELINE
# ============================================================

def run_pipeline() -> pd.DataFrame:
    """
    Execute the complete Member 1 → Member 2 pipeline.
    """

    start_time = time.perf_counter()

    print()
    print("=" * 72)
    print(
        "SUPPLYSHIELD AI — "
        "MEMBER 1 → MEMBER 2 "
        "END-TO-END PIPELINE"
    )
    print("=" * 72)

    logger.info(
        "Project root: %s",
        PROJECT_ROOT,
    )

    try:

        # ----------------------------------------------------
        # Preparation
        # ----------------------------------------------------

        ensure_directories()

        # ----------------------------------------------------
        # Stage 1
        # ----------------------------------------------------

        records = (
            load_member1_dataset()
        )

        # ----------------------------------------------------
        # Stage 2
        # ----------------------------------------------------

        records = (
            validate_input_records(
                records
            )
        )

        # ----------------------------------------------------
        # Stage 3
        # ----------------------------------------------------

        df = (
            records_to_dataframe(
                records
            )
        )

        # ----------------------------------------------------
        # Stage 4
        # ----------------------------------------------------

        run_data_quality_checks(
            df
        )

        # ----------------------------------------------------
        # Stage 5
        # ----------------------------------------------------

        (
            final_df,
            summary,
        ) = run_ml_pipeline(
            df
        )

        # ----------------------------------------------------
        # Stage 6
        # ----------------------------------------------------

        validate_final_output(
            final_df
        )

        # ----------------------------------------------------
        # Save outputs
        # ----------------------------------------------------

        print_section(
            "STAGE 7 — FINAL OUTPUT EXPORT"
        )

        json_path = (
            save_final_json(
                final_df
            )
        )

        csv_path = (
            save_final_csv(
                final_df
            )
        )

        summary_path = (
            save_pipeline_summary(
                summary
            )
        )

        print_status(
            "Final JSON exported."
        )

        print_status(
            "Final CSV exported."
        )

        print_status(
            "Pipeline summary exported."
        )

        # ----------------------------------------------------
        # Execution metrics
        # ----------------------------------------------------

        elapsed = (
            time.perf_counter()
            - start_time
        )

        # ----------------------------------------------------
        # Final terminal report
        # ----------------------------------------------------

        print()
        print("=" * 72)
        print(
            "SUPPLYSHIELD AI — "
            "END-TO-END PIPELINE SUCCESS"
        )
        print("=" * 72)

        print()
        print(
            "DATA INGESTION"
        )

        print(
            f"  Records loaded       : "
            f"{len(records)}"
        )

        print()
        print(
            "AI / ML"
        )

        print(
            f"  Records processed    : "
            f"{len(final_df)}"
        )

        print(
            f"  Average risk score   : "
            f"{summary.get('average_risk_score', 0)}"
        )

        print(
            f"  High-risk records    : "
            f"{summary.get('high_risk_records', 0)}"
        )

        print(
            f"  Medium-risk records  : "
            f"{summary.get('medium_risk_records', 0)}"
        )

        print(
            f"  Low-risk records     : "
            f"{summary.get('low_risk_records', 0)}"
        )

        print(
            f"  Anomaly records      : "
            f"{summary.get('anomaly_records', 0)}"
        )

        print(
            f"  WebShield alerts     : "
            f"{summary.get('webshield_alerts', 0)}"
        )

        print()
        print(
            "OUTPUT FILES"
        )

        print(
            f"  JSON                 : "
            f"{json_path}"
        )

        print(
            f"  CSV                  : "
            f"{csv_path}"
        )

        print(
            f"  Summary              : "
            f"{summary_path}"
        )

        print()
        print(
            f"Execution time        : "
            f"{elapsed:.2f} seconds"
        )

        print()
        print(
            "STATUS: "
            "END-TO-END ML PIPELINE SUCCESS"
        )

        print("=" * 72)
        print()

        return final_df

    except Exception as exc:

        logger.exception(
            "Production pipeline failed."
        )

        print()
        print("=" * 72)
        print(
            "SUPPLYSHIELD AI — PIPELINE FAILED"
        )
        print("=" * 72)

        print(
            f"ERROR: {exc}"
        )

        print()

        raise


# ============================================================
# 17. COMMAND-LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_pipeline()