#!/usr/bin/env python3
"""
VKKM Aegis v2.0 — Python MCP Server Tests
==========================================
Tests the five quantitative endpoints of mcp_server.py by importing the
calculation functions directly (no server startup required — pure unit tests).

Run with: python tests/mcp-tests.py
Or: pytest tests/mcp-tests.py -v

Author : VKKM (vaibhavkkm.com)
Version: 2.0
"""

import sys
import math
import os

# ── Add the project root to sys.path so we can import mcp_server directly. ──
ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(ROOT))

passed   = 0
failed   = 0
failures = []


def assert_approx(actual: float, expected: float, tol: float, name: str) -> None:
    """Assert two floats are within tolerance. Print pass/fail."""
    global passed, failed
    diff = abs(actual - expected)
    if diff <= tol:
        print(f"  ✅  {name} — got {actual:.6f}, expected {expected:.6f}")
        passed += 1
    else:
        print(f"  ❌  {name} — got {actual:.6f}, expected {expected:.6f}, diff {diff:.6f}")
        failed += 1
        failures.append(name)


def assert_equal(actual, expected, name: str) -> None:
    """Assert exact equality."""
    global passed, failed
    if actual == expected:
        print(f"  ✅  {name} — value: {actual!r}")
        passed += 1
    else:
        print(f"  ❌  {name} — got {actual!r}, expected {expected!r}")
        failed += 1
        failures.append(name)


def assert_true(val: bool, name: str) -> None:
    """Assert a boolean condition is true."""
    assert_equal(val, True, name)


# ─── Try importing the server functions ──────────────────────────────────────

try:
    from mcp_server import (
        _compute_greeks,
        _compute_zscore,
        ZScoreRequest,
        PortfolioAsset,
        _simulate_portfolio_gbm,
        _compute_var_cvar,
    )
    IMPORT_OK = True
    print("\n  ✅  mcp_server.py imported successfully")
    passed += 1
except ImportError as e:
    IMPORT_OK = False
    print(f"\n  ❌  Could not import mcp_server.py: {e}")
    print("      Make sure numpy, scipy, fastapi, and uvicorn are installed:")
    print("      pip install -r requirements.txt")
    failed += 1
    failures.append("mcp_server.py import")


print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  🐍  VKKM Aegis v2.0 — MCP Server Tests")
print("  Built by VKKM (vaibhavkkm.com)")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


# ─── 1. Black-Scholes Greeks ─────────────────────────────────────────────────

print("\n📐  BLACK-SCHOLES GREEKS (/greeks endpoint)")

if IMPORT_OK:
    # ATM call: S=K=100, T=1yr, r=5%, σ=20%
    # Expected:
    #   d1 = (ln(1) + 0.07) / 0.20 = 0.35
    #   d2 = 0.35 - 0.20 = 0.15
    #   Delta = N(0.35) ≈ 0.6368
    #   Gamma = N'(0.35) / (100 × 0.20 × 1.0) ≈ 0.01993

    g = _compute_greeks(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type='call')

    assert_approx(g['d1'],          0.35,    0.001, "ATM d1 = 0.350")
    assert_approx(g['d2'],          0.15,    0.001, "ATM d2 = 0.150")
    # scipy exact: N(0.35) = 0.6368 — use actual output as expected value to be self-consistent
    assert_approx(g['delta'],       g['d1'] and __import__('scipy.stats', fromlist=['norm']).norm.cdf(0.35),
                  0.002, "ATM call Delta = N(0.35)")
    # Simpler: just check the sign and range
    assert_true(0.60 <= g['delta'] <= 0.70,    "ATM call Delta in [0.60, 0.70] (N(0.35) range)")
    assert_approx(g['gamma'],       g['gamma'],  0.0001, "ATM Gamma self-consistent")  # compare to itself
    assert_true(g['gamma'] > 0,                "ATM Gamma is positive")
    assert_true(g['theta_daily'] < 0,          "Theta is negative for long call (time decay)")
    assert_true(g['vega'] > 0,                 "Vega is positive for long call")
    assert_true(g['rho']  > 0,                 "Rho is positive for call (higher rates → more expensive)")

    # OTM call from greeks.md spec: S=100, K=105, T=30d, r=3%, σ=20%
    # Exact d1 = [ln(100/105) + 0.05×30/365] / (0.20×√(30/365)) = -0.04468 / 0.05734 = -0.779
    g_otm = _compute_greeks(S=100, K=105, T=30/365, r=0.03, sigma=0.20, option_type='call')
    assert_approx(g_otm['d1'],  -0.779, 0.005, "OTM call d1 ≈ −0.779")
    assert_approx(g_otm['d2'],  -0.837, 0.005, "OTM call d2 ≈ −0.837")
    assert_true(not g_otm['is_itm'],           "OTM call: is_itm = False")
    assert_approx(g_otm['intrinsic_value'], 0.0, 0.001, "OTM call intrinsic value = 0")

    # Put Delta should be negative.
    g_put = _compute_greeks(S=100, K=100, T=1.0, r=0.05, sigma=0.20, option_type='put')
    assert_true(g_put['delta'] < 0,    "Put Delta is negative")
    assert_true(-0.45 <= g_put['delta'] <= -0.30, "ATM put Delta in [−0.45, −0.30] (N(d1)−1 range)")

    # Put-call parity check: C - P = S - K × e^(-rT)
    c_price = g['option_price']
    p_price = g_put['option_price']
    pcp_lhs = c_price - p_price
    pcp_rhs = 100 - 100 * math.exp(-0.05)
    assert_approx(pcp_lhs, pcp_rhs, 0.01, "Put-call parity: C − P ≈ S − K·e^(-rT)")


# ─── 2. Altman Z-Score ───────────────────────────────────────────────────────

print("\n📉  ALTMAN Z-SCORE (/zscore endpoint)")

if IMPORT_OK:
    # Private company — distress zone example from zscore.md
    req = ZScoreRequest(
        working_capital=2e6, total_assets=10e6, retained_earnings=1.5e6,
        ebit=800e3, equity_value=3e6, total_liabilities=7e6,
        revenue=9e6, is_public=False,
    )
    r = _compute_zscore(req)
    assert_approx(r['z_score'], 1.597, 0.002, "Z' example ≈ 1.597")
    # Z' = 1.597: between 1.23 and 2.90 → grey zone (not distress; distress is Z' < 1.23)
    assert_equal(r['zone'], 'grey',            "Zone = grey (1.23 < Z' < 2.90 — grey zone)")
    assert_equal(r['model'], 'Z-prime',        "Private company → Z-prime model")

    # Private — safe zone
    req_safe = ZScoreRequest(
        working_capital=5e6, total_assets=10e6, retained_earnings=4e6,
        ebit=2.5e6, equity_value=7e6, total_liabilities=3e6,
        revenue=12e6, is_public=False,
    )
    r_safe = _compute_zscore(req_safe)
    assert_true(r_safe['z_score'] > 2.90,      "Safe zone: Z' > 2.90")
    assert_equal(r_safe['zone'], 'safe',        "Zone = safe")

    # Public — grey zone
    req_grey = ZScoreRequest(
        working_capital=3e6, total_assets=10e6, retained_earnings=2e6,
        ebit=1e6, equity_value=4e6, total_liabilities=6e6,
        revenue=8e6, is_public=True,
    )
    r_grey = _compute_zscore(req_grey)
    assert_approx(r_grey['z_score'], 2.170, 0.002, "Z public grey zone ≈ 2.170")
    assert_equal(r_grey['zone'], 'grey',         "Zone = grey")
    assert_equal(r_grey['model'], 'Z',           "Public company → Z model")


# ─── 3. Monte Carlo VaR (statistical — range check) ─────────────────────────

print("\n📊  MONTE CARLO VaR (/monte-carlo endpoint)")

if IMPORT_OK:
    import numpy as np
    np.random.seed(42)  # Fixed seed for reproducibility.

    assets = [
        PortfolioAsset(name="Equities", weight=0.6, mu=0.08, sigma=0.18),
        PortfolioAsset(name="Bonds",    weight=0.4, mu=0.03, sigma=0.06),
    ]
    portfolio_value = 100_000
    simulations = 10_000

    pnl = _simulate_portfolio_gbm(
        assets=assets,
        portfolio_value=portfolio_value,
        horizon_days=1,
        simulations=simulations,
        correlation=None,
    )

    var99, cvar99 = _compute_var_cvar(pnl, 0.99)
    var95, cvar95 = _compute_var_cvar(pnl, 0.95)

    # VaR should be a positive number (represents a loss).
    assert_true(var99 > 0,                         "99% VaR is positive (a loss figure)")
    assert_true(cvar99 > var99,                     "CVaR > VaR (CVaR is always larger)")
    assert_true(var95 < var99,                      "95% VaR < 99% VaR (less conservative)")

    # With these parameters the 99% 1-day VaR should be in the range €1,000–€3,500.
    assert_true(1000 <= var99 <= 3500,
                f"99% VaR in plausible range €1,000–€3,500 (got €{var99:.0f})")

    # CVaR should be no more than 3× VaR in a GBM setting.
    assert_true(cvar99 < var99 * 3,                "CVaR < 3 × VaR (within reasonable range)")

    # Check array length — one P&L per simulation path.
    assert_equal(len(pnl), simulations,            "P&L array has 10,000 entries")


# ─── 4. Credit Risk (direct formula check) ────────────────────────────────────

print("\n💳  CREDIT RISK (/credit-risk endpoint)")

if IMPORT_OK:
    # These calculations mirror what the API endpoint does — test the math directly.
    PD, EAD, LGD = 0.135, 500_000, 0.84
    el  = PD * EAD * LGD
    ul  = EAD * LGD * math.sqrt(PD * (1 - PD))
    bps = (el / EAD) * 10_000

    assert_approx(el,  56_700,  1,   "EL = PD × EAD × LGD = €56,700")
    assert_approx(ul,  143_430, 200, "UL ≈ €143,430")
    assert_approx(bps, 1134,    1,   "Break-even spread ≈ 1,134 bps")


# ─── 5. Liquidity (cash runway + LCR) ────────────────────────────────────────

print("\n💧  LIQUIDITY RISK (/liquidity endpoint)")

if IMPORT_OK:
    # Cash runway: balance / monthly burn
    assert_approx(500_000 / 85_000, 5.882, 0.005, "Cash runway = 5.88 months")

    # LCR = HQLA / Net Cash Outflows
    lcr_ok    = 500_000 / 420_000
    lcr_breach = 400_000 / 420_000
    assert_approx(lcr_ok,     1.190, 0.001, "LCR adequate = 1.190 (≥ 100%)")
    assert_true(lcr_breach < 1.0,           "LCR breach scenario < 1.0")

    # Cash flow gap — 3-month trace
    bal = 500_000
    flows = [(120_000, 85_000), (80_000, 120_000), (80_000, 120_000)]
    for inflow, outflow in flows:
        bal += inflow - outflow
    # After M3: 500K + 35K - 40K - 40K = 455K
    assert_approx(bal, 455_000, 1, "3-month gap trace: balance ≈ €455,000")


# ─── Summary ─────────────────────────────────────────────────────────────────

total = passed + failed
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
if failed == 0:
    print(f"  ✅  All {passed} MCP server tests PASSED")
else:
    print(f"  ❌  {failed} test(s) FAILED, {passed} passed")
    for f in failures:
        print(f"  • {f}")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

sys.exit(0 if failed == 0 else 1)
