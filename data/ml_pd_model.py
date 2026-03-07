#!/usr/bin/env python3
"""
VKKM Aegis — ML Probability of Default Model (Phase 3)
========================================================
Replaces lookup-table PD estimates with a calibrated logistic regression
model trained on synthetic industry-representative company data.

Model features:
  - X1 (Working Capital / Total Assets)
  - X2 (Retained Earnings / Total Assets)
  - X3 (EBIT / Total Assets) — the most predictive ratio
  - X4 (Equity Value / Total Liabilities)
  - X5 (Revenue / Total Assets)
  - Revenue growth YoY (decimal)
  - Leverage ratio (Debt/Equity)
  - Interest coverage ratio (EBIT/Interest)

Output:
  - pd_pct        : Predicted 1-year PD in percent (e.g. 8.4)
  - ci_lower      : 95% confidence interval lower bound (%)
  - ci_upper      : 95% confidence interval upper bound (%)
  - pd_label      : text bucket (Very Low / Low / Moderate / High / Very High)
  - model_quality : quality descriptor based on train/test accuracy

Usage:
    from data.ml_pd_model import MLProbabilityOfDefault
    model = MLProbabilityOfDefault()
    result = model.predict_pd({"X1": 0.2, "X2": 0.15, ...})

The model is re-trained at startup from the synthetic dataset if the
serialised model file (pd_model.pkl) is not found. Training takes < 1 second.

Author : VKKM (vaibhavkkm.com)
Version: 3.0
"""

import os
import math
import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Paths relative to this file.
_DIR         = os.path.dirname(__file__)
_MODEL_PATH  = os.path.join(_DIR, "pd_model.pkl")
_DATA_PATH   = os.path.join(_DIR, "synthetic_default_dataset.csv")

# Feature columns used for training.
FEATURE_COLS = [
    "X1", "X2", "X3", "X4", "X5",
    "revenue_growth", "leverage_ratio", "interest_coverage"
]

# Try importing sklearn — optional dependency.
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning(
        "scikit-learn not installed — ML PD model unavailable. "
        "Run: pip install scikit-learn joblib pandas"
    )


class MLProbabilityOfDefault:
    """
    Logistic regression model for predicting Probability of Default (PD).

    The model is wrapped in a scikit-learn Pipeline:
        StandardScaler → LogisticRegression (L2 regularisation, C=1.0)

    On initialisation it either:
      1. Loads a pre-trained model from pd_model.pkl (fast path), or
      2. Trains from scratch on the synthetic dataset (< 1 second).

    Confidence intervals are computed analytically from the logistic
    regression's probability estimates using the delta method approximation:
        CI = [logit(p) ± 1.96 × σ_logit] transformed back through sigmoid.
    """

    def __init__(self):
        """Load or train the logistic regression model on initialisation."""
        self._pipeline = None
        self._train_accuracy = None
        self._test_accuracy  = None
        self._auc            = None
        self._n_train        = None
        self._is_ready       = False

        if not SKLEARN_AVAILABLE:
            return

        # Try loading pre-serialised model first.
        if os.path.isfile(_MODEL_PATH):
            try:
                saved = joblib.load(_MODEL_PATH)
                self._pipeline       = saved["pipeline"]
                self._train_accuracy = saved.get("train_accuracy")
                self._test_accuracy  = saved.get("test_accuracy")
                self._auc            = saved.get("auc")
                self._n_train        = saved.get("n_train")
                self._is_ready       = True
                logger.info(f"ML PD model loaded from {_MODEL_PATH}")
                return
            except Exception as e:
                logger.warning(f"Could not load pd_model.pkl: {e} — retraining.")

        # Train from scratch.
        self._train()

    def _train(self) -> None:
        """Train the logistic regression pipeline on the synthetic dataset."""
        if not SKLEARN_AVAILABLE:
            return

        # Generate or load the dataset.
        if not os.path.isfile(_DATA_PATH):
            logger.info("Synthetic dataset not found — generating now...")
            try:
                from data.generate_dataset import generate_dataset
                df = generate_dataset()
                df.to_csv(_DATA_PATH, index=False)
            except Exception as e:
                logger.error(f"Dataset generation failed: {e}")
                return
        else:
            df = pd.read_csv(_DATA_PATH)

        # Validate required columns.
        missing = [c for c in FEATURE_COLS + ["defaulted"] if c not in df.columns]
        if missing:
            logger.error(f"Dataset missing columns: {missing}")
            return

        X = df[FEATURE_COLS].values.astype(float)
        y = df["defaulted"].values.astype(int)

        # Impute any NaN values with column median (defensive coding).
        # We don't want the pipeline to crash if the user sends partial data.
        for col_idx in range(X.shape[1]):
            nan_mask = np.isnan(X[:, col_idx])
            if nan_mask.any():
                X[nan_mask, col_idx] = np.nanmedian(X[:, col_idx])

        # 80/20 train/test split — stratified to preserve class balance.
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )

        # Build pipeline: normalise → logistic regression.
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("clf",    LogisticRegression(
                C=1.0,              # L2 regularisation strength
                max_iter=500,
                solver="lbfgs",
                class_weight="balanced",  # Defaults are rare, so balancing is crucial here.
                random_state=42,
            )),
        ])

        pipeline.fit(X_train, y_train)

        # Compute performance metrics.
        train_acc = float(pipeline.score(X_train, y_train))
        test_acc  = float(pipeline.score(X_test, y_test))
        try:
            auc = float(roc_auc_score(y_test, pipeline.predict_proba(X_test)[:, 1]))
        except Exception:
            auc = None

        self._pipeline       = pipeline
        self._train_accuracy = round(train_acc * 100, 2)
        self._test_accuracy  = round(test_acc * 100, 2)
        self._auc            = round(auc * 100, 2) if auc else None
        self._n_train        = len(X_train)
        self._is_ready       = True

        logger.info(
            f"ML PD model trained — Train acc: {train_acc:.2%}, "
            f"Test acc: {test_acc:.2%}, AUC: {auc:.2%}" if auc else
            f"ML PD model trained — Train acc: {train_acc:.2%}, "
            f"Test acc: {test_acc:.2%}"
        )

        # Serialise for future fast-loads.
        try:
            joblib.dump({
                "pipeline":       pipeline,
                "train_accuracy": self._train_accuracy,
                "test_accuracy":  self._test_accuracy,
                "auc":            self._auc,
                "n_train":        self._n_train,
            }, _MODEL_PATH)
            logger.info(f"Model saved to {_MODEL_PATH}")
        except Exception as e:
            logger.warning(f"Could not save model: {e}")

    def predict_pd(self, features: dict) -> dict:
        """
        Predict the 1-year Probability of Default for a company.

        Parameters
        ----------
        features : dict with any subset of FEATURE_COLS as keys.
                   Missing features are substituted with conservative defaults.

        Returns
        -------
        dict with:
            pd_pct        — Predicted PD as a percentage (e.g. 8.4)
            ci_lower_pct  — Lower 95% CI bound (%)
            ci_upper_pct  — Upper 95% CI bound (%)
            pd_label      — Human-readable risk label
            z_score       — Implied Altman Z'-score from the input ratios
            model_quality — Short descriptor of model confidence
            available     — True if ML model ran; False if fallback was used
        """
        if not self._is_ready or not SKLEARN_AVAILABLE:
            return self._fallback_pd(features)

        # Build feature vector — fill missing columns with conservative defaults.
        defaults = {
            "X1": 0.15, "X2": 0.10, "X3": 0.07,
            "X4": 0.80, "X5": 0.90, "revenue_growth": 0.0,
            "leverage_ratio": 1.5, "interest_coverage": 2.0,
        }
        x_dict = {**defaults, **{k: v for k, v in features.items() if k in FEATURE_COLS}}
        x = np.array([[x_dict[c] for c in FEATURE_COLS]])

        # Get predicted probability.
        proba = self._pipeline.predict_proba(x)[0, 1]  # P(default=1)
        pd_pct = float(proba * 100)

        # ── 95% Confidence Interval via delta method on logit scale ──────────
        # logit(p) = log(p / (1−p))
        # Var[logit(p)] ≈ 1 / (n × p × (1−p)) where n = training set size
        eps   = 1e-9  # Prevent log(0)
        logit = math.log((proba + eps) / (1 - proba + eps))
        n     = self._n_train or 240
        sigma_logit = math.sqrt(1.0 / (n * (proba + eps) * (1 - proba + eps)))

        def _sigmoid(z):
            return 1 / (1 + math.exp(-z))

        ci_lower = _sigmoid(logit - 1.96 * sigma_logit) * 100
        ci_upper = _sigmoid(logit + 1.96 * sigma_logit) * 100

        # Altman Z' from the 5 input ratios (informational).
        z = (0.717 * x_dict["X1"] + 0.847 * x_dict["X2"] + 3.107 * x_dict["X3"] +
             0.420 * x_dict["X4"] + 0.998 * x_dict["X5"])

        # PD label buckets.
        label = self._pd_label(pd_pct)

        # Model quality descriptor.
        quality = "High" if (self._test_accuracy or 0) >= 75 else "Moderate"

        return {
            "pd_pct":          round(pd_pct,    2),
            "ci_lower_pct":    round(ci_lower,  2),
            "ci_upper_pct":    round(ci_upper,  2),
            "pd_label":        label,
            "z_score":         round(z, 4),
            "train_acc_pct":   self._train_accuracy,
            "test_acc_pct":    self._test_accuracy,
            "auc_pct":         self._auc,
            "model_quality":   quality,
            "n_train_samples": self._n_train,
            "available":       True,
            "method":          "Logistic Regression (L2) — sklearn Pipeline",
        }

    def _fallback_pd(self, features: dict) -> dict:
        """
        Fallback to Altman Z'-score zone lookup when sklearn is unavailable.
        Less precise but always available.
        """
        x1 = features.get("X1", 0.15)
        x2 = features.get("X2", 0.10)
        x3 = features.get("X3", 0.07)
        x4 = features.get("X4", 0.80)
        x5 = features.get("X5", 0.90)
        z  = 0.717*x1 + 0.847*x2 + 3.107*x3 + 0.420*x4 + 0.998*x5

        if z > 2.90:
            pd_pct = 2.0
        elif z > 1.23:
            pd_pct = 10.0
        else:
            pd_pct = 28.0

        return {
            "pd_pct":        pd_pct,
            "ci_lower_pct":  pd_pct * 0.5,
            "ci_upper_pct":  pd_pct * 2.0,
            "pd_label":      self._pd_label(pd_pct),
            "z_score":       round(z, 4),
            "available":     False,
            "method":        "Altman Z' zone lookup (scikit-learn not installed)",
        }

    @staticmethod
    def _pd_label(pd_pct: float) -> str:
        """Map a PD percentage to a human-readable label."""
        if pd_pct < 1.0:
            return "Very Low (< 1%)"
        elif pd_pct < 3.0:
            return "Low (1–3%)"
        elif pd_pct < 8.0:
            return "Moderate (3–8%)"
        elif pd_pct < 20.0:
            return "High (8–20%)"
        else:
            return "Very High (> 20%)"


# Module-level singleton — expensive to re-train on every call.
_ml_pd_model: Optional["MLProbabilityOfDefault"] = None


def get_ml_pd_model() -> "MLProbabilityOfDefault":
    """Return the module-level singleton, training if not yet initialised."""
    global _ml_pd_model
    if _ml_pd_model is None:
        _ml_pd_model = MLProbabilityOfDefault()
    return _ml_pd_model
