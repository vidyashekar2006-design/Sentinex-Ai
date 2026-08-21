"""
SupplyShield AI
==================================================

Member 2 Production ML Pipeline

Purpose
-------
This module provides the production orchestration layer
between the normalized Member 1 dataset and the completed
Member 2 AI/ML engines.

Pipeline:

    Member 1 Data
         ↓
    Data Preparation
         ↓
    Feature Engineering
         ↓
    Anomaly Signals
         ↓
    NLP Signals
         ↓
    Risk Scoring
         ↓
    WebShield
         ↓
    Unified Risk Output

IMPORTANT
---------
This module does not alter Member 1's scraper or
self-healing pipeline.

It also does not modify the original research notebooks.

The notebooks remain the experimentation / development
artifacts. This module provides the production interface
that will eventually call the finalized reusable ML
components.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger(
    "SupplyShield.Member2.MLPipeline"
)


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class MLPipelineConfig:
    """
    Configuration for the Member 2 ML pipeline.
    """

    # --------------------------------------------------------
    # Risk thresholds
    # --------------------------------------------------------

    low_risk_threshold: float = 33.0

    medium_risk_threshold: float = 66.0

    # --------------------------------------------------------
    # Anomaly configuration
    # --------------------------------------------------------

    price_anomaly_z_threshold: float = 2.5

    # --------------------------------------------------------
    # WebShield configuration
    # --------------------------------------------------------

    suspicious_price_ratio: float = 0.50

    # --------------------------------------------------------
    # Text configuration
    # --------------------------------------------------------

    minimum_text_length: int = 3


# ============================================================
# PIPELINE CLASS
# ============================================================

class SupplyShieldMLPipeline:
    """
    Production-ready Member 2 AI/ML processing pipeline.

    The class is intentionally modular so that trained models
    from the completed notebooks can be attached later without
    changing the overall application architecture.
    """

    def __init__(
        self,
        config: MLPipelineConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config is not None
            else MLPipelineConfig()
        )

        logger.info(
            "SupplyShield ML Pipeline initialized."
        )


    # ========================================================
    # 1. INPUT PREPARATION
    # ========================================================

    def prepare_input(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Prepare Member 1 data for downstream ML processing.

        This step:
            - copies the input
            - normalizes column names
            - guarantees expected fields
            - normalizes numerical values
            - creates unified text
        """

        if dataframe is None:

            raise ValueError(
                "Input dataframe cannot be None."
            )

        if dataframe.empty:

            raise ValueError(
                "Input dataframe is empty."
            )

        df = dataframe.copy()

        # ----------------------------------------------------
        # Normalize column names
        # ----------------------------------------------------

        df.columns = [
            str(column)
            .strip()
            .lower()
            .replace(" ", "_")
            for column in df.columns
        ]

        # ----------------------------------------------------
        # Required canonical columns
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Numeric conversion
        # ----------------------------------------------------

        df["price"] = pd.to_numeric(
            df["price"],
            errors="coerce",
        )

        df["rating"] = pd.to_numeric(
            df["rating"],
            errors="coerce",
        )

        # ----------------------------------------------------
        # Unified text representation
        # ----------------------------------------------------

        text_columns = [
            "title",
            "company",
            "supplier",
            "product",
            "event",
            "location",
            "review",
        ]

        for column in text_columns:

            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

        df["combined_text"] = (
            df[text_columns]
            .agg(" ".join, axis=1)
            .str.replace(
                r"\s+",
                " ",
                regex=True,
            )
            .str.strip()
        )

        logger.info(
            "Input preparation completed: %s",
            df.shape,
        )

        return df


    # ========================================================
    # 2. FEATURE ENGINEERING
    # ========================================================

    def engineer_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate production-level deterministic features.

        These features are deliberately model-independent.

        They can be used by:
            - anomaly detection
            - classification
            - risk scoring
            - WebShield
        """

        df = dataframe.copy()

        # ----------------------------------------------------
        # Text length
        # ----------------------------------------------------

        df["text_length"] = (
            df["combined_text"]
            .str.len()
            .fillna(0)
            .astype(int)
        )

        df["word_count"] = (
            df["combined_text"]
            .str.split()
            .str.len()
            .fillna(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # Review availability
        # ----------------------------------------------------

        df["has_review"] = (
            df["review"]
            .str.len()
            .gt(
                self.config.minimum_text_length
            )
            .astype(int)
        )

        # ----------------------------------------------------
        # Supplier availability
        # ----------------------------------------------------

        df["has_supplier"] = (
            df["supplier"]
            .str.len()
            .gt(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # Event availability
        # ----------------------------------------------------

        df["has_event"] = (
            df["event"]
            .str.len()
            .gt(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # URL availability
        # ----------------------------------------------------

        df["has_url"] = (
            df["url"]
            .fillna("")
            .astype(str)
            .str.len()
            .gt(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # Rating normalization
        # ----------------------------------------------------

        df["rating_normalized"] = (
            df["rating"]
            .clip(
                lower=0,
                upper=5,
            )
            .div(5)
        )

        # ----------------------------------------------------
        # Price log transformation
        # ----------------------------------------------------

        positive_price = (
            df["price"]
            .where(
                df["price"] > 0
            )
        )

        df["log_price"] = np.log1p(
            positive_price
        )

        # ----------------------------------------------------
        # Price percentile
        # ----------------------------------------------------

        if (
            df["price"]
            .notna()
            .sum()
            > 1
        ):

            df["price_percentile"] = (
                df["price"]
                .rank(
                    pct=True,
                    method="average",
                )
            )

        else:

            df["price_percentile"] = 0.5

        # ----------------------------------------------------
        # Availability signal
        # ----------------------------------------------------

        availability_text = (
            df["availability"]
            .fillna("")
            .astype(str)
            .str.lower()
        )

        df["availability_risk_signal"] = (
            availability_text
            .str.contains(
                r"out|unavailable|limited|stock|delay|backorder",
                regex=True,
                na=False,
            )
            .astype(int)
        )

        logger.info(
            "Feature engineering completed."
        )

        return df


    # ========================================================
    # 3. ANOMALY DETECTION
    # ========================================================

    def detect_anomalies(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate deterministic anomaly signals.

        This acts as the production baseline.

        The trained anomaly model from the completed ML
        notebook can later replace or augment these signals.
        """

        df = dataframe.copy()

        # ----------------------------------------------------
        # Price z-score
        # ----------------------------------------------------

        price_mean = df["price"].mean()

        price_std = df["price"].std()

        if (
            pd.isna(price_std)
            or price_std == 0
        ):

            df["price_z_score"] = 0.0

        else:

            df["price_z_score"] = (
                (
                    df["price"]
                    - price_mean
                )
                / price_std
            )

        # ----------------------------------------------------
        # Price anomaly flag
        # ----------------------------------------------------

        df["price_anomaly"] = (
            df["price_z_score"]
            .abs()
            .ge(
                self.config
                .price_anomaly_z_threshold
            )
            .astype(int)
        )

        # ----------------------------------------------------
        # Text anomaly signal
        # ----------------------------------------------------

        df["text_anomaly"] = (
            df["text_length"]
            .eq(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # Data completeness anomaly
        # ----------------------------------------------------

        completeness_fields = [
            "title",
            "company",
            "supplier",
            "product",
            "price",
            "currency",
            "url",
        ]

        available_columns = [
            column
            for column in completeness_fields
            if column in df.columns
        ]

        if available_columns:

            df["data_completeness"] = (
                df[available_columns]
                .notna()
                .mean(axis=1)
            )

        else:

            df["data_completeness"] = 0.0

        df["completeness_anomaly"] = (
            df["data_completeness"]
            .lt(0.40)
            .astype(int)
        )

        # ----------------------------------------------------
        # Combined anomaly score
        # ----------------------------------------------------

        df["anomaly_score"] = (
            (
                df["price_anomaly"] * 0.50
            )
            + (
                df["text_anomaly"] * 0.20
            )
            + (
                df["completeness_anomaly"]
                * 0.30
            )
        )

        logger.info(
            "Anomaly detection completed."
        )

        return df


    # ========================================================
    # 4. NLP RISK SIGNALS
    # ========================================================

    def generate_nlp_signals(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate interpretable text-based risk signals.

        This baseline is intentionally transparent.

        The trained NLP classifier from the completed notebook
        can later be plugged into the same output columns.
        """

        df = dataframe.copy()

        text = (
            df["combined_text"]
            .fillna("")
            .astype(str)
            .str.lower()
        )

        # ----------------------------------------------------
        # Supply disruption keywords
        # ----------------------------------------------------

        disruption_keywords = [
            "delay",
            "shortage",
            "shutdown",
            "strike",
            "disruption",
            "recall",
            "bankrupt",
            "closure",
            "scarcity",
            "backorder",
        ]

        # ----------------------------------------------------
        # Negative supplier/business keywords
        # ----------------------------------------------------

        negative_keywords = [
            "complaint",
            "fraud",
            "scam",
            "fake",
            "counterfeit",
            "poor",
            "bad",
            "damaged",
            "unreliable",
            "warning",
        ]

        # ----------------------------------------------------
        # Count keyword occurrences
        # ----------------------------------------------------

        def keyword_count(
            text_value: str,
            keywords: list[str],
        ) -> int:

            count = 0

            for keyword in keywords:

                count += len(
                    re.findall(
                        rf"\b{re.escape(keyword)}\b",
                        text_value,
                    )
                )

            return count

        df["disruption_keyword_count"] = (
            text.apply(
                lambda value:
                keyword_count(
                    value,
                    disruption_keywords,
                )
            )
        )

        df["negative_keyword_count"] = (
            text.apply(
                lambda value:
                keyword_count(
                    value,
                    negative_keywords,
                )
            )
        )

        # ----------------------------------------------------
        # NLP disruption signal
        # ----------------------------------------------------

        df["nlp_disruption_signal"] = (
            df["disruption_keyword_count"]
            .gt(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # NLP reputation signal
        # ----------------------------------------------------

        df["nlp_negative_signal"] = (
            df["negative_keyword_count"]
            .gt(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # NLP risk score
        # ----------------------------------------------------

        df["nlp_risk_score"] = (
            (
                df["nlp_disruption_signal"]
                * 60
            )
            + (
                df["nlp_negative_signal"]
                * 40
            )
        ).clip(
            lower=0,
            upper=100,
        )

        logger.info(
            "NLP risk signal generation completed."
        )

        return df


    # ========================================================
    # 5. WEB SHIELD SIGNALS
    # ========================================================

    def generate_webshield_signals(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate production baseline WebShield signals.

        Signals include:

            - suspiciously low price
            - missing supplier
            - missing URL
            - negative/counterfeit language
            - availability anomalies
        """

        df = dataframe.copy()

        # ----------------------------------------------------
        # Price-based signal
        # ----------------------------------------------------

        price_percentile = (
            df["price_percentile"]
            .fillna(0.5)
        )

        df["webshield_price_signal"] = (
            price_percentile
            .lt(
                self.config
                .suspicious_price_ratio
            )
            .astype(int)
        )

        # ----------------------------------------------------
        # Supplier identity signal
        # ----------------------------------------------------

        df["webshield_supplier_signal"] = (
            df["has_supplier"]
            .eq(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # URL signal
        # ----------------------------------------------------

        df["webshield_url_signal"] = (
            df["has_url"]
            .eq(0)
            .astype(int)
        )

        # ----------------------------------------------------
        # Reputation signal
        # ----------------------------------------------------

        df["webshield_reputation_signal"] = (
            df["nlp_negative_signal"]
        )

        # ----------------------------------------------------
        # Availability signal
        # ----------------------------------------------------

        df["webshield_availability_signal"] = (
            df["availability_risk_signal"]
        )

        # ----------------------------------------------------
        # WebShield risk
        # ----------------------------------------------------

        df["webshield_risk_score"] = (
            (
                df["webshield_price_signal"]
                * 25
            )
            + (
                df["webshield_supplier_signal"]
                * 20
            )
            + (
                df["webshield_url_signal"]
                * 15
            )
            + (
                df["webshield_reputation_signal"]
                * 25
            )
            + (
                df["webshield_availability_signal"]
                * 15
            )
        ).clip(
            lower=0,
            upper=100,
        )

        logger.info(
            "WebShield signal generation completed."
        )

        return df


    # ========================================================
    # 6. SUPPLY CHAIN RISK SCORING
    # ========================================================

    def calculate_risk_scores(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate unified supply-chain risk.

        Risk components:

            anomaly       30%
            NLP           25%
            WebShield     25%
            availability  10%
            rating        10%
        """

        df = dataframe.copy()

        # ----------------------------------------------------
        # Component scores
        # ----------------------------------------------------

        anomaly_component = (
            df["anomaly_score"]
            .clip(
                lower=0,
                upper=1,
            )
            * 100
        )

        nlp_component = (
            df["nlp_risk_score"]
            .clip(
                lower=0,
                upper=100,
            )
        )

        webshield_component = (
            df["webshield_risk_score"]
            .clip(
                lower=0,
                upper=100,
            )
        )

        availability_component = (
            df["availability_risk_signal"]
            * 100
        )

        # Lower rating → higher risk.
        rating_component = (
            (
                5
                - df["rating"].clip(
                    lower=0,
                    upper=5,
                )
            )
            / 5
            * 100
        )

        rating_component = (
            rating_component
            .fillna(50)
        )

        # ----------------------------------------------------
        # Weighted unified score
        # ----------------------------------------------------

        df["supply_chain_risk_score"] = (
            anomaly_component * 0.30
            + nlp_component * 0.25
            + webshield_component * 0.25
            + availability_component * 0.10
            + rating_component * 0.10
        ).clip(
            lower=0,
            upper=100,
        )

        # ----------------------------------------------------
        # Overall risk score
        # ----------------------------------------------------

        df["overall_risk_score"] = (
            df["supply_chain_risk_score"]
            .clip(
                lower=0,
                upper=100,
            )
            .round(2)
        )

        # ----------------------------------------------------
        # Risk category
        # ----------------------------------------------------

        df["risk_category"] = np.select(
            [
                df["overall_risk_score"]
                <= self.config
                .low_risk_threshold,

                df["overall_risk_score"]
                <= self.config
                .medium_risk_threshold,
            ],
            [
                "LOW",
                "MEDIUM",
            ],
            default="HIGH",
        )

        logger.info(
            "Risk scoring completed."
        )

        return df


    # ========================================================
    # 7. EXPLAINABILITY
    # ========================================================

    def generate_explanations(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate human-readable explanations for risk scores.

        This is important for the final dashboard because
        users should understand WHY an item was flagged.
        """

        df = dataframe.copy()

        explanations: list[str] = []

        for _, row in df.iterrows():

            reasons: list[str] = []

            if (
                row.get(
                    "price_anomaly",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Price anomaly detected"
                )

            if (
                row.get(
                    "nlp_disruption_signal",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Supply disruption signal detected"
                )

            if (
                row.get(
                    "nlp_negative_signal",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Negative reputation signal detected"
                )

            if (
                row.get(
                    "webshield_price_signal",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Suspicious pricing pattern"
                )

            if (
                row.get(
                    "webshield_supplier_signal",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Supplier identity information missing"
                )

            if (
                row.get(
                    "webshield_url_signal",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Source URL unavailable"
                )

            if (
                row.get(
                    "availability_risk_signal",
                    0,
                )
                == 1
            ):

                reasons.append(
                    "Availability risk signal detected"
                )

            if not reasons:

                reasons.append(
                    "No major risk signals detected"
                )

            explanations.append(
                "; ".join(reasons)
            )

        df["risk_explanation"] = (
            explanations
        )

        logger.info(
            "Risk explanations generated."
        )

        return df


    # ========================================================
    # 8. COMPLETE EXECUTION
    # ========================================================

    def run(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute the complete Member 2 ML pipeline.

        Parameters
        ----------
        dataframe:
            Validated Member 1 dataset.

        Returns
        -------
        pd.DataFrame
            Fully processed Member 2 dataset.
        """

        logger.info(
            "Starting SupplyShield Member 2 ML pipeline."
        )

        # ----------------------------------------------------
        # Stage A
        # ----------------------------------------------------

        df = self.prepare_input(
            dataframe
        )

        # ----------------------------------------------------
        # Stage B
        # ----------------------------------------------------

        df = self.engineer_features(
            df
        )

        # ----------------------------------------------------
        # Stage C
        # ----------------------------------------------------

        df = self.detect_anomalies(
            df
        )

        # ----------------------------------------------------
        # Stage D
        # ----------------------------------------------------

        df = self.generate_nlp_signals(
            df
        )

        # ----------------------------------------------------
        # Stage E
        # ----------------------------------------------------

        df = self.generate_webshield_signals(
            df
        )

        # ----------------------------------------------------
        # Stage F
        # ----------------------------------------------------

        df = self.calculate_risk_scores(
            df
        )

        # ----------------------------------------------------
        # Stage G
        # ----------------------------------------------------

        df = self.generate_explanations(
            df
        )

        logger.info(
            "SupplyShield Member 2 ML pipeline completed."
        )

        return df


# ============================================================
# 9. PIPELINE SUMMARY
# ============================================================

def generate_pipeline_summary(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate a machine-readable summary of the
    Member 2 AI/ML pipeline results.
    """

    if dataframe.empty:

        return {
            "records": 0,
            "status": "EMPTY",
        }

    summary = {
        "records_processed": int(
            len(dataframe)
        ),

        "average_risk_score": round(
            float(
                dataframe[
                    "overall_risk_score"
                ].mean()
            ),
            2,
        ),

        "maximum_risk_score": round(
            float(
                dataframe[
                    "overall_risk_score"
                ].max()
            ),
            2,
        ),

        "minimum_risk_score": round(
            float(
                dataframe[
                    "overall_risk_score"
                ].min()
            ),
            2,
        ),

        "low_risk_records": int(
            (
                dataframe[
                    "risk_category"
                ]
                == "LOW"
            ).sum()
        ),

        "medium_risk_records": int(
            (
                dataframe[
                    "risk_category"
                ]
                == "MEDIUM"
            ).sum()
        ),

        "high_risk_records": int(
            (
                dataframe[
                    "risk_category"
                ]
                == "HIGH"
            ).sum()
        ),

        "webshield_alerts": int(
            (
                dataframe[
                    "webshield_risk_score"
                ]
                > 0
            ).sum()
        ),

        "anomaly_records": int(
            (
                dataframe[
                    "anomaly_score"
                ]
                > 0
            ).sum()
        ),

        "status": "SUCCESS",
    }

    return summary


# ============================================================
# 10. STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 72)
    print(
        "SUPPLYSHIELD AI — "
        "ML PIPELINE MODULE TEST"
    )
    print("=" * 72)

    # --------------------------------------------------------
    # Small internal test dataset
    # --------------------------------------------------------

    test_data = pd.DataFrame(
        [
            {
                "source": "TestSource",
                "title": "Supply delay warning",
                "company": "Test Company",
                "supplier": "Test Supplier",
                "product": "Electronic Component",
                "event": "Shipping delay",
                "location": "India",
                "price": 500,
                "currency": "INR",
                "availability": "Limited stock",
                "rating": 3.2,
                "review": (
                    "Poor availability and delivery delay"
                ),
                "date": None,
                "url": "https://example.com",
                "timestamp": None,
            },
            {
                "source": "TestSource",
                "title": "Normal component",
                "company": "Stable Company",
                "supplier": "Stable Supplier",
                "product": "Standard Component",
                "event": "",
                "location": "India",
                "price": 1000,
                "currency": "INR",
                "availability": "Available",
                "rating": 4.8,
                "review": "Good product",
                "date": None,
                "url": "https://example.com/product",
                "timestamp": None,
            },
        ]
    )

    pipeline = SupplyShieldMLPipeline()

    result = pipeline.run(
        test_data
    )

    summary = (
        generate_pipeline_summary(
            result
        )
    )

    print()
    print(
        "PIPELINE TEST RESULT"
    )
    print("-" * 72)

    print(
        f"Records processed : "
        f"{summary['records_processed']}"
    )

    print(
        f"Average risk      : "
        f"{summary['average_risk_score']}"
    )

    print(
        f"High risk         : "
        f"{summary['high_risk_records']}"
    )

    print(
        f"Medium risk       : "
        f"{summary['medium_risk_records']}"
    )

    print(
        f"Low risk          : "
        f"{summary['low_risk_records']}"
    )

    print(
        f"WebShield alerts  : "
        f"{summary['webshield_alerts']}"
    )

    print()
    print(
        "STATUS: ML PIPELINE MODULE WORKING"
    )