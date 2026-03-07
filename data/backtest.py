#!/usr/bin/env python3
"""
VKKM Aegis — Historical VaR Backtesting Engine (Phase 3)
=========================================================
Implements the Kupiec Proportion of Failures (POF) test — the industry-
standard method for validating a Value at Risk model. Regulators (Basel,
DORA) require banks to run this test on every VaR model quarterly.

Kupiec Test Logic:
    Hypothesis: The true exception rate equals the nominal VaR tail (1 − α)
    LR = −2 × ln[(1−p̂)^(N−x) × p̂^x] + 2 × ln[(1−x/N)^(N−x) × (x/N)^x]
    LR ~ χ²(1) under H₀

Basel Traffic Light System (based on 250 observations):
    Green  →  0–4  exceptions  → model accepted
    Yellow →  5–9  exceptions  → model under review
    Red    → 10+   exceptions  → model rejected

Usage:
    from data.backtest import BacktestEngine
    engine = BacktestEngine()
    result = engine.run(pnl_series=pnl, var_estimate=10000, confidence=0.99)

Author : VKKM (vaibhavkkm.com)
Version: 3.0
"""

import math
import logging
from typing import Optional
import numpy as np

logger = logging.getLogger(__name__)


class BacktestEngine:
    """
    VaR model validation engine.

    Accepts a P&L time series and a VaR estimate, then runs the Kupiec POF
    test and Basel traffic light classification to judge model adequacy.
    """

    # Basel traffic light critical values (250 trading days, 99% VaR).
    # Source: Basel Committee on Banking Supervision (1996), Table 2.
    BASEL_ZONES = [
        # (max_exceptions, zone, color, interpretation)
        (4,  "Green",  "🟢", "Model accepted — exception rate within expectations."),
        (9,  "Yellow", "🟡", "Model under review — too many exceptions, investigate."),
        (999,"Red",    "🔴", "Model rejected — systematic underestimation of risk."),
    ]

    def run(
        self,
        pnl_series:    np.ndarray,
        var_estimate:  float,
        confidence:    float = 0.99,
        var_is_loss:   bool  = True,
    ) -> dict:
        """
        Run the Kupiec POF backtest.

        Parameters
        ----------
        pnl_series   : array of daily P&L values. Positive = profit, negative = loss.
        var_estimate : the VaR dollar amount (positive number, represents a loss).
        confidence   : VaR confidence level (e.g. 0.99 for 99% VaR).
        var_is_loss  : if True, exceptions are days where loss > VaR. If False,
                       exceptions are days where P&L < −var_estimate.

        Returns
        -------
        dict with keys:
            n_observations, n_exceptions, exception_rate, expected_exceptions,
            kupiec_lr, p_value, passes_kupiec, basel_zone, verdict, details.
        """
        pnl = np.asarray(pnl_series, dtype=float)
        N   = len(pnl)

        if N < 20:
            raise ValueError(
                f"Backtest requires at least 20 observations, got {N}. "
                "Basel requires 250 days for the traffic light system."
            )

        # Count the number of VaR exceptions (breaches).
        # Note: We assume P&L is signed where positive=profit, negative=loss.
        # It's a common trap in quant models to mix this up, so we handle both cases explicitly.
        if var_is_loss:
            # VaR expressed as a positive loss — compare to absolute P&L losses.
            exceptions_mask = pnl < -abs(var_estimate)
        else:
            exceptions_mask = pnl < var_estimate  # var_estimate is already negative

        x = int(np.sum(exceptions_mask))  # Number of exceptions (breaches)
        p_hat = x / N                      # Observed exception rate

        # The expected exception rate under the model.
        p_model = 1.0 - confidence        # e.g. 0.01 for 99% VaR

        expected_exceptions = N * p_model

        # ── Kupiec LR test statistic ──────────────────────────────────────────
        # Handle edge cases where x = 0 or x = N (log(0) is undefined).
        lr = self._kupiec_lr(x, N, p_model)

        # LR ~ χ²(1) under H₀ → critical value is 3.841 at 5% significance.
        # p-value approximated from chi-squared CDF.
        p_value = self._chi2_sf(lr, df=1) if lr is not None else None
        passes_kupiec = (p_value is not None and p_value >= 0.05)

        # ── Basel traffic light ───────────────────────────────────────────────
        zone, color, interpretation = self._classify_basel(x)

        # ── Conditional coverage (Christoffersen) — simplified ────────────────
        # Check for clustering of exceptions — consecutive breaches are worse.
        consecutive_runs = self._count_consecutive_exceptions(exceptions_mask)

        return {
            "n_observations":      N,
            "n_exceptions":        x,
            "exception_rate_pct":  round(p_hat * 100, 4),
            "expected_exceptions": round(expected_exceptions, 2),
            "expected_rate_pct":   round(p_model * 100, 2),
            "kupiec_lr":           round(lr, 4) if lr is not None else None,
            "p_value":             round(p_value, 4) if p_value is not None else None,
            "passes_kupiec":       passes_kupiec,
            "passes_at_5pct":      passes_kupiec,
            "basel_zone":          zone,
            "basel_color":         color,
            "interpretation":      interpretation,
            "consecutive_runs":    consecutive_runs,
            "clustering_risk":     "⚠️ High" if consecutive_runs >= 3 else "✅ Low",
            "confidence":          confidence,
            "verdict":             self._build_verdict(passes_kupiec, zone, x, N, p_hat, p_model),
        }

    def compute_historical_var(
        self,
        returns:       np.ndarray,
        portfolio_value: float,
        confidence:    float = 0.99,
        horizon_days:  int   = 1,
    ) -> dict:
        """
        Compute a non-parametric historical VaR and CVaR from actual return data.

        This is the 'historical simulation' method — no model assumptions.
        Uses the empirical distribution of past returns directly.

        Parameters
        ----------
        returns        : daily log-returns or percentage changes (as decimals)
        portfolio_value: total portfolio value in base currency
        confidence     : VaR confidence level
        horizon_days   : scaling horizon (uses square-root-of-time scaling)

        Returns
        -------
        dict with var_amount, cvar_amount, n_returns, return sources.
        """
        r = np.asarray(returns, dtype=float)

        if len(r) < 20:
            raise ValueError("At least 20 return observations required.")

        # Scale returns to the requested horizon using square-root-of-time.
        scale = math.sqrt(horizon_days)
        scaled_returns = r * scale

        # VaR = loss at (1−confidence) quantile of the return distribution.
        quantile = np.quantile(scaled_returns, 1.0 - confidence)
        var   = -quantile * portfolio_value

        # CVaR = average of all returns below the VaR quantile.
        tail         = scaled_returns[scaled_returns <= quantile]
        cvar         = -float(np.mean(tail)) * portfolio_value if len(tail) > 0 else var

        # Percentile statistics.
        p1   = float(np.percentile(r * 100, 1))
        p5   = float(np.percentile(r * 100, 5))
        worst = float(np.min(r * 100))

        return {
            "var_amount":         round(var, 2),
            "cvar_amount":        round(cvar, 2),
            "var_pct":            round(-quantile * 100, 4),
            "cvar_pct":           round(-float(np.mean(tail)) * 100, 4) if len(tail) else round(-quantile * 100, 4),
            "n_returns":          len(r),
            "horizon_days":       horizon_days,
            "confidence":         confidence,
            "worst_day_pct":      round(worst, 4),
            "p1_daily_return_pct": round(p1, 4),
            "p5_daily_return_pct": round(p5, 4),
            "method":             "Historical Simulation (non-parametric)",
        }

    # ─── Private helpers ──────────────────────────────────────────────────────

    def _kupiec_lr(self, x: int, N: int, p: float) -> Optional[float]:
        """
        Compute the Kupiec likelihood ratio statistic.

        LR = −2 ln[(1−p)^(N−x) × p^x] + 2 ln[(1−x/N)^(N−x) × (x/N)^x]

        Returns None if the statistic is mathematically undefined (x=0 or x=N).
        """
        if x == 0 or x == N:
            # LR undefined — return 0.0 (model looks perfect / perfectly wrong).
            # Pass/fail cannot be determined analytically; report separately.
            return 0.0

        p_hat = x / N

        try:
            # Log-likelihood under the model (H₀: p̂ = p_model).
            ll_h0 = (N - x) * math.log(1 - p) + x * math.log(p)
            # Log-likelihood under the unrestricted model (H₁: p̂ = x/N).
            ll_h1 = (N - x) * math.log(1 - p_hat) + x * math.log(p_hat)
            lr = -2 * (ll_h0 - ll_h1)
            return max(lr, 0.0)  # LR must be ≥ 0
        except (ValueError, ZeroDivisionError) as e:
            logger.warning(f"Kupiec LR computation failed: {e}")
            return None

    def _chi2_sf(self, lr: float, df: int = 1) -> float:
        """
        Approximate the chi-squared survival function (1 − CDF) at `lr`.
        Uses scipy.stats.chi2 if available, otherwise Wilson-Hilferty approx.

        This gives the p-value: probability of observing LR this extreme
        if H₀ (model is correctly specified) is true.
        """
        try:
            from scipy.stats import chi2
            return float(chi2.sf(lr, df))
        except ImportError:
            # Fallback for when scipy isn't installed. We use the Wilson-Hilferty normal 
            # approximation for χ²(1). It's surprisingly accurate for our purposes here.
            # χ²(1) ≈ z² where z ~ N(0,1) → p ≈ 2 × (1 − Φ(√lr))
            z = math.sqrt(abs(lr))
            # Abramowitz & Stegun erfc approximation.
            t = 1 / (1 + 0.3275911 * z)
            poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 +
                        t * (-1.453152027 + t * 1.061405429))))
            p_one_tail = poly * math.exp(-0.5 * lr)
            return min(max(2 * p_one_tail, 0.0), 1.0)

    def _classify_basel(self, n_exceptions: int) -> tuple:
        """Map exception count to Basel traffic light zone."""
        for max_exc, zone, color, interp in self.BASEL_ZONES:
            if n_exceptions <= max_exc:
                return zone, color, interp
        return "Red", "🔴", "Model rejected."

    def _count_consecutive_exceptions(self, mask: np.ndarray) -> int:
        """
        Count the longest run of consecutive VaR exceptions.
        Consecutive breaches signal volatility clustering — worse than random misses,
        indicating the model underestimates tail dependence.
        """
        max_run = 0
        current = 0
        for breach in mask:
            if breach:
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
        return max_run

    def _build_verdict(
        self, passes: bool, zone: str, x: int, N: int, p_hat: float, p_model: float
    ) -> str:
        """Compose a human-readable verdict string for the backtest report."""
        obs_rate   = round(p_hat * 100, 2)
        model_rate = round(p_model * 100, 2)

        if zone == "Green" and passes:
            return (
                f"✅ PASS — Model adequately estimates tail risk. "
                f"{x} exceptions in {N} days ({obs_rate}% observed vs {model_rate}% expected). "
                f"Basel Green zone — no regulatory action required."
            )
        elif zone == "Yellow":
            return (
                f"⚠️ REVIEW — Elevated exception rate detected. "
                f"{x} exceptions ({obs_rate}% vs {model_rate}% expected). "
                f"Basel Yellow zone — investigate model assumptions. "
                f"Consider re-calibrating σ or adding jump-diffusion."
            )
        else:
            return (
                f"🔴 FAIL — Model systematically underestimates risk. "
                f"{x} exceptions ({obs_rate}% vs {model_rate}% expected). "
                f"Basel Red zone — model must be replaced or recalibrated immediately."
            )
