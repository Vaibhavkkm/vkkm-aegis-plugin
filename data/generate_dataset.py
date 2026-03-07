#!/usr/bin/env python3
"""
VKKM Aegis — Synthetic Default Dataset Generator (Phase 3)
===========================================================
Generates a 300-row synthetic dataset of company financial ratios with
known default outcomes. Used to train the ML Probability of Default model
in ml_pd_model.py.

Default rates by Altman zone are calibrated to published academic research:
  - Safe zone  (Z' > 2.90): ~2%  default rate
  - Grey zone  (1.23–2.90): ~10% default rate
  - Distress   (Z' < 1.23): ~28% default rate

Run with: python3 data/generate_dataset.py
Output:   data/synthetic_default_dataset.csv

Author : VKKM (vaibhavkkm.com)
Version: 3.0
"""

import os
import numpy as np
import pandas as pd

# Fixed seed for reproducibility — the same CSV must be generated every run.
RNG = np.random.default_rng(seed=42)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "synthetic_default_dataset.csv")


def _altman_z_prime(x1, x2, x3, x4, x5) -> float:
    """Compute Altman Z' score from the 5 ratios."""
    return 0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.420 * x4 + 0.998 * x5


def _generate_company_in_zone(zone: str) -> dict:
    """
    Sample financially plausible ratios for one company in a given Altman zone.
    Uses bounded normal distributions calibrated to typical company financials.
    Rejects samples that land in the wrong zone (rejection sampling).
    """
    for _ in range(500):  # Max attempts before giving up.
        if zone == "safe":
            # Financially healthy: positive WC, good EBIT margin, low leverage.
            x1 = float(RNG.normal(0.35, 0.10))   # WC/TA
            x2 = float(RNG.normal(0.30, 0.10))   # RE/TA
            x3 = float(RNG.normal(0.18, 0.06))   # EBIT/TA
            x4 = float(RNG.normal(1.80, 0.50))   # Equity/Liab
            x5 = float(RNG.normal(1.20, 0.30))   # Rev/TA

        elif zone == "grey":
            # Moderate risk: thin margins, moderate leverage.
            x1 = float(RNG.normal(0.15, 0.10))
            x2 = float(RNG.normal(0.12, 0.08))
            x3 = float(RNG.normal(0.08, 0.05))
            x4 = float(RNG.normal(0.80, 0.30))
            x5 = float(RNG.normal(0.90, 0.25))

        else:  # distress
            # High risk: thin / negative WC, poor EBIT, high leverage.
            x1 = float(RNG.normal(-0.05, 0.15))
            x2 = float(RNG.normal(-0.10, 0.15))
            x3 = float(RNG.normal(0.01, 0.05))
            x4 = float(RNG.normal(0.30, 0.20))
            x5 = float(RNG.normal(0.70, 0.25))

        # Compute Z'-score and confirm the sample is in the right zone.
        z = _altman_z_prime(x1, x2, x3, x4, x5)
        correct_zone = (
            (zone == "safe"    and z > 2.90) or
            (zone == "grey"    and 1.23 <= z <= 2.90) or
            (zone == "distress" and z < 1.23)
        )
        if correct_zone:
            return {"X1": x1, "X2": x2, "X3": x3, "X4": x4, "X5": x5, "z_score": z, "zone": zone}

    # If rejection sampling fails (very rare), return a manually constructed row.
    fallback = {"safe": (0.4, 0.35, 0.22, 2.0, 1.3),
                "grey": (0.15, 0.14, 0.09, 0.75, 0.9),
                "distress": (-0.05, -0.12, 0.01, 0.28, 0.68)}
    x1, x2, x3, x4, x5 = fallback[zone]
    z = _altman_z_prime(x1, x2, x3, x4, x5)
    return {"X1": x1, "X2": x2, "X3": x3, "X4": x4, "X5": x5, "z_score": z, "zone": zone}


def generate_dataset(
    n_safe:     int = 120,
    n_grey:     int = 100,
    n_distress: int = 80,
    default_rate_safe:     float = 0.02,
    default_rate_grey:     float = 0.10,
    default_rate_distress: float = 0.28,
) -> pd.DataFrame:
    """
    Generate a synthetic dataset of company financial ratios with default labels.

    Total: 300 companies (120 safe + 100 grey + 80 distress).
    Default rates calibrated to Altman zone:
        Safe     → ~2%  (120 companies → ~2 defaults)
        Grey     → ~10% (100 companies → ~10 defaults)
        Distress → ~28% ( 80 companies → ~22 defaults)

    Returns
    -------
    pd.DataFrame with columns: X1–X5, z_score, zone, revenue_growth,
                               leverage_ratio, interest_coverage, defaulted
    """
    records = []

    for zone, count, dr in [
        ("safe",     n_safe,     default_rate_safe),
        ("grey",     n_grey,     default_rate_grey),
        ("distress", n_distress, default_rate_distress),
    ]:
        for i in range(count):
            row = _generate_company_in_zone(zone)

            # ── Additional features beyond the 5 Altman ratios ──────────────

            # Revenue growth YoY (positive for growing firms, negative for declining)
            if zone == "safe":
                revenue_growth = float(RNG.normal(0.08, 0.06))
            elif zone == "grey":
                revenue_growth = float(RNG.normal(0.01, 0.07))
            else:
                revenue_growth = float(RNG.normal(-0.06, 0.10))

            # Leverage ratio (debt/equity) — higher = more risky
            if zone == "safe":
                leverage = float(RNG.uniform(0.3, 1.0))
            elif zone == "grey":
                leverage = float(RNG.uniform(0.8, 2.5))
            else:
                leverage = float(RNG.uniform(2.0, 5.0))

            # Interest coverage ratio (EBIT/Interest Expense)
            # Below 1.5x is a red flag; below 1.0x means can't service debt.
            if zone == "safe":
                int_cov = float(RNG.uniform(4.0, 12.0))
            elif zone == "grey":
                int_cov = float(RNG.uniform(1.5, 4.0))
            else:
                int_cov = float(RNG.uniform(0.2, 1.8))

            # ── Assign default label ─────────────────────────────────────────
            # Add a small Z-score-based nudge to the default probability so
            # the ML model has meaningful signal to learn from.
            z = row["z_score"]
            # Higher Z-score → lower chance of default (logistic-style nudge)
            nudge = max(min((2.0 - z) * 0.03, 0.08), -0.05)
            p_default = min(max(dr + nudge, 0.01), 0.90)
            defaulted = int(RNG.random() < p_default)

            records.append({
                "X1":               round(row["X1"],  4),
                "X2":               round(row["X2"],  4),
                "X3":               round(row["X3"],  4),
                "X4":               round(row["X4"],  4),
                "X5":               round(row["X5"],  4),
                "z_score":          round(row["z_score"], 4),
                "zone":             zone,
                "revenue_growth":   round(revenue_growth, 4),
                "leverage_ratio":   round(leverage, 4),
                "interest_coverage":round(min(int_cov, 20.0), 4),  # Cap at 20x
                "defaulted":        defaulted,
            })

    df = pd.DataFrame(records).sample(frac=1, random_state=42).reset_index(drop=True)
    return df


if __name__ == "__main__":
    # Regenerate the training dataset on demand.
    df = generate_dataset()

    defaults = df["defaulted"].sum()
    total    = len(df)
    rate     = defaults / total * 100

    print(f"\nGenerated {total} synthetic company records")
    print(f"Default rate: {defaults}/{total} ({rate:.1f}%)")
    print("\nBy zone:")
    for zone in ["safe", "grey", "distress"]:
        subset = df[df["zone"] == zone]
        d = subset["defaulted"].sum()
        print(f"  {zone:8s}: {d}/{len(subset)} defaulted "
              f"({d/len(subset)*100:.1f}%)")

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved to: {OUTPUT_PATH}")
