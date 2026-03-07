#!/usr/bin/env python3
"""
VKKM Aegis — Python MCP Server (Phase 3 / v3.0)
=================================================
A FastAPI backend that powers the quantitative calculation, live data,
ML modeling, and export endpoints for the VKKM Aegis Claude plugin.

Phase 2 endpoints (v2.0):
  POST /monte-carlo  — 10,000-path GBM simulation → VaR + CVaR
  POST /greeks       — Exact Black-Scholes Greeks (δ, γ, ν, θ, ρ)
  POST /zscore       — Altman Z-Score (public Z model + private Z' model)
  POST /credit-risk  — PD × EAD × LGD → Expected & Unexpected Loss
  POST /liquidity    — LCR, NSFR, cash runway, 12-month gap table

Phase 3 endpoints (v3.0):
  GET  /market-data  — Live price, realised vol, 1yr return via Yahoo Finance
  GET  /risk-free-rate — Current 3-month US T-bill yield
  POST /backtest     — Kupiec POF test + Basel traffic light (CSV P&L upload)
  POST /ml-pd        — ML-predicted Probability of Default (logistic regression)
  POST /export/excel — Generate .xlsx report with RAG colour-coding
  POST /export/json  — Generate structured JSON report
  GET  /health       — Liveness probe

Usage:
  pip install -r requirements.txt
  uvicorn mcp_server:app --port 8082 --reload

Author : VKKM (vaibhavkkm.com)
Version: 3.0
"""

import math
import logging
import io
import json
import numpy as np
from scipy.stats import norm
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# ── Phase 3 data modules (soft imports — server runs even if dependencies missing) ──
try:
    from data.live_data import get_live_data
    LIVE_DATA_OK = True
except ImportError:
    LIVE_DATA_OK = False
    logging.warning("data.live_data not available — /market-data will return 503")

try:
    from data.backtest import BacktestEngine
    BACKTEST_OK = True
except ImportError:
    BACKTEST_OK = False
    logging.warning("data.backtest not available — /backtest will return 503")

try:
    from data.ml_pd_model import get_ml_pd_model
    ML_PD_OK = True
except ImportError:
    ML_PD_OK = False
    logging.warning("data.ml_pd_model not available — /ml-pd will return 503")

try:
    from data.excel_export import (
        generate_kri_excel, generate_gap_table_excel,
        generate_credit_risk_excel, generate_risk_register_excel,
        generate_backtest_excel, generate_json_export,
    )
    EXCEL_OK = True
except ImportError:
    EXCEL_OK = False
    logging.warning("data.excel_export not available — /export will return 503")


# ─── Application setup ────────────────────────────────────────────────────────

app = FastAPI(
    title="VKKM Aegis MCP Server",
    description="Quantitative finance calculation, live data, ML modeling, and export engine for the VKKM Aegis Claude Plugin.",
    version="3.0",
)

# Allow Claude's environment to call this server from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic request/response models ─────────────────────────────────────────

class PortfolioAsset(BaseModel):
    """One position in a multi-asset portfolio."""
    name: str = Field(..., description="Asset name / ticker")
    weight: float = Field(..., ge=0.0, le=1.0, description="Portfolio weight (0–1)")
    mu: float = Field(..., description="Expected annual return (decimal, e.g. 0.08 for 8%)")
    sigma: float = Field(..., gt=0.0, description="Annual volatility (decimal, e.g. 0.18 for 18%)")


class MonteCarloRequest(BaseModel):
    """Request body for the /monte-carlo endpoint."""
    assets: List[PortfolioAsset] = Field(..., description="List of portfolio positions")
    portfolio_value: float = Field(..., gt=0.0, description="Total portfolio value in base currency")
    horizon_days: int = Field(1, ge=1, le=252, description="Horizon in trading days (1 = 1-day VaR)")
    confidence: float = Field(0.99, ge=0.90, le=0.999, description="Confidence level (e.g. 0.99 for 99% VaR)")
    simulations: int = Field(10_000, ge=1_000, le=100_000, description="Number of GBM simulation paths")
    correlation: Optional[float] = Field(None, description="Pairwise correlation (simplified — for 2-asset portfolios)")


class MonteCarloResponse(BaseModel):
    """Results from the Monte Carlo VaR engine."""
    var_amount: float = Field(..., description="VaR in base currency at stated confidence and horizon")
    cvar_amount: float = Field(..., description="CVaR (Expected Shortfall) in base currency")
    var_pct: float = Field(..., description="VaR as % of portfolio value")
    cvar_pct: float = Field(..., description="CVaR as % of portfolio value")
    simulations_run: int
    confidence: float
    horizon_days: int
    risk_contribution: List[dict] = Field(..., description="Each asset's % contribution to total VaR")
    worst_simulation_loss: float = Field(..., description="Single worst simulated loss across all paths")


class GreeksRequest(BaseModel):
    """Request body for the /greeks endpoint (Black-Scholes European option)."""
    S: float = Field(..., gt=0.0, description="Current asset price")
    K: float = Field(..., gt=0.0, description="Strike price")
    T_days: float = Field(..., gt=0.0, description="Time to expiry in calendar days")
    r: float = Field(..., description="Risk-free rate (annualised, decimal — e.g. 0.03 for 3%)")
    sigma: float = Field(..., gt=0.0, description="Implied volatility (annualised, decimal — e.g. 0.20 for 20%)")
    option_type: str = Field(..., pattern="^(call|put)$", description="'call' or 'put'")


class GreeksResponse(BaseModel):
    """All five Black-Scholes Greeks plus intermediate values."""
    d1: float
    d2: float
    N_d1: float
    N_d2: float
    Nprime_d1: float
    delta: float
    gamma: float
    vega: float           # Per 1% vol move (divided by 100)
    theta_daily: float    # Per calendar day (divided by 365)
    rho: float            # Per 1% rate move (divided by 100)
    option_price: float
    T_years: float
    is_itm: bool
    intrinsic_value: float
    time_value: float


class ZScoreRequest(BaseModel):
    """Financial inputs for Altman Z-Score calculation."""
    working_capital: float = Field(..., description="Current Assets − Current Liabilities")
    total_assets: float = Field(..., gt=0.0, description="Total balance sheet assets")
    retained_earnings: float = Field(..., description="Accumulated retained earnings (can be negative)")
    ebit: float = Field(..., description="Earnings Before Interest and Tax (can be negative)")
    equity_value: float = Field(..., description="Market value of equity (public) or book value (private)")
    total_liabilities: float = Field(..., gt=0.0, description="Total liabilities and debt")
    revenue: float = Field(..., ge=0.0, description="Annual revenue / turnover")
    is_public: bool = Field(..., description="True for listed (Z model), False for private (Z' model)")


class ZScoreResponse(BaseModel):
    """Altman Z-Score result with full ratio breakdown."""
    model: str = Field(..., description="'Z' (public) or 'Z-prime' (private)")
    X1: float = Field(..., description="Working Capital / Total Assets")
    X2: float = Field(..., description="Retained Earnings / Total Assets")
    X3: float = Field(..., description="EBIT / Total Assets")
    X4: float = Field(..., description="Equity Value / Total Liabilities")
    X5: float = Field(..., description="Revenue / Total Assets")
    z_score: float
    zone: str = Field(..., description="'safe', 'grey', or 'distress'")
    zone_emoji: str
    estimated_pd_range: str = Field(..., description="Approximate 1-year PD range based on zone")
    weakest_ratio: str = Field(..., description="The ratio contributing least to the score")


class CreditRiskRequest(BaseModel):
    """Inputs for the PD × EAD × LGD credit risk calculation."""
    pd: float = Field(..., ge=0.0, le=1.0, description="Probability of Default (decimal, e.g. 0.135 for 13.5%)")
    ead: float = Field(..., gt=0.0, description="Exposure at Default (drawn balance at default)")
    lgd: float = Field(..., ge=0.0, le=1.0, description="Loss Given Default (decimal, e.g. 0.84 for 84%)")


class CreditRiskResponse(BaseModel):
    """Basel credit risk output: EL, UL, spread."""
    expected_loss: float = Field(..., description="EL = PD × EAD × LGD")
    unexpected_loss: float = Field(..., description="UL = EAD × LGD × √(PD×(1−PD))")
    expected_loss_pct: float = Field(..., description="EL as % of EAD")
    unexpected_loss_pct: float = Field(..., description="UL as % of EAD")
    breakeven_spread_bps: float = Field(..., description="Minimum credit spread to break even on EL (basis points)")
    risk_rating: str = Field(..., description="Low / Moderate / High / Critical")


class LiquidityCashFlowItem(BaseModel):
    """One month's cash flow data."""
    month: int = Field(..., ge=1, le=24)
    inflows: float = Field(..., ge=0.0)
    outflows: float = Field(..., ge=0.0)


class LiquidityRequest(BaseModel):
    """Inputs for liquidity risk and cash flow gap analysis."""
    opening_balance: float = Field(..., ge=0.0, description="Current cash balance")
    monthly_cash_flows: List[LiquidityCashFlowItem] = Field(..., description="Month-by-month inflow/outflow data")
    hqla: Optional[float] = Field(None, description="High Quality Liquid Assets (for LCR — banks only)")
    net_cash_outflows_30d: Optional[float] = Field(None, description="Stressed 30-day net outflows (for LCR)")
    available_stable_funding: Optional[float] = Field(None, description="ASF for NSFR calculation")
    required_stable_funding: Optional[float] = Field(None, description="RSF for NSFR calculation")


class LiquidityResponse(BaseModel):
    """Liquidity analysis results."""
    cash_runway_months: Optional[float]
    monthly_average_burn: float
    lcr: Optional[float] = Field(None, description="LCR ratio (None if inputs not provided)")
    lcr_status: Optional[str] = Field(None, description="'adequate' (>=100%) or 'breach' (<100%)")
    nsfr: Optional[float] = Field(None, description="NSFR ratio (None if inputs not provided)")
    nsfr_status: Optional[str]
    gap_table: List[dict] = Field(..., description="Month-by-month cumulative balance table")
    shortfall_month: Optional[int] = Field(None, description="First month where balance goes negative (None if no shortfall)")
    trough_balance: float = Field(..., description="Lowest cumulative balance in the projection period")
    trough_month: int


# ─── Core calculation functions ────────────────────────────────────────────────

def _simulate_portfolio_gbm(
    assets: List[PortfolioAsset],
    portfolio_value: float,
    horizon_days: int,
    simulations: int,
    correlation: Optional[float],
) -> np.ndarray:
    """
    Simulate portfolio returns over the given horizon using Geometric Brownian
    Motion. Returns an array of shape (simulations,) containing the simulated
    portfolio P&L (negative = loss) for each path.

    GBM per asset:
        S(T) = S(0) × exp[(μ - σ²/2)T + σ√T × Z]
        where Z ~ N(0,1)

    For a portfolio: compute weighted sum of asset returns per path.
    """
    dt = horizon_days / 252.0  # Convert trading days to years

    n_assets = len(assets)
    n = simulations

    if n_assets == 2 and correlation is not None:
        # Use a simple 2-asset correlated draw via Cholesky decomposition.
        rho = np.clip(correlation, -0.999, 0.999)
        L = np.array([[1.0, 0.0], [rho, math.sqrt(1.0 - rho**2)]])
        Z_indep = np.random.standard_normal((2, n))
        Z = L @ Z_indep  # Correlated normals — shape (2, n)
    else:
        # Independent draws — simplification when correlation not provided.
        Z = np.random.standard_normal((n_assets, n))

    portfolio_returns = np.zeros(n)

    for i, asset in enumerate(assets):
        # Log-normal GBM drift and diffusion terms.
        drift = (asset.mu - 0.5 * asset.sigma**2) * dt
        diffusion = asset.sigma * math.sqrt(dt) * Z[i]

        # Asset return (fractional) for each simulation path.
        asset_return = np.exp(drift + diffusion) - 1.0

        # Weighted contribution to portfolio return.
        portfolio_returns += asset.weight * asset_return

    # Convert from returns to P&L in currency terms.
    portfolio_pnl = portfolio_returns * portfolio_value
    return portfolio_pnl


def _compute_var_cvar(pnl: np.ndarray, confidence: float) -> tuple[float, float]:
    """
    Given an array of P&L simulations, compute VaR and CVaR.

    VaR(α) = −Quantile(1−α) of the distribution
            = the loss that is exceeded with probability (1−α)

    CVaR(α) = average loss in the worst (1−α)% of scenarios
             = E[−PnL | PnL < −VaR]
    """
    q = np.quantile(pnl, 1.0 - confidence)  # Negative for losses
    var = -q  # VaR is expressed as a positive loss figure

    # CVaR = average of all outcomes worse than VaR threshold
    tail_losses = -pnl[pnl <= q]
    cvar = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var

    return float(var), float(cvar)


def _compute_greeks(S, K, T, r, sigma, option_type: str) -> dict:
    """
    Compute all five Black-Scholes Greeks for a European option.

    Uses scipy.stats.norm for N() (CDF) and N'() (PDF) values,
    ensuring full numerical precision.
    """
    # d1 and d2 — the core intermediate values in Black-Scholes.
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    Nprime_d1 = norm.pdf(d1)  # Standard normal PDF at d1

    # Black-Scholes option price.
    discount = math.exp(-r * T)
    if option_type == "call":
        price = S * N_d1 - K * discount * N_d2
    else:
        price = K * discount * norm.cdf(-d2) - S * norm.cdf(-d1)

    # ── Delta: sensitivity to underlying price ──
    if option_type == "call":
        delta = N_d1
    else:
        delta = N_d1 - 1.0

    # ── Gamma: rate of change of Delta (same for calls and puts) ──
    gamma = Nprime_d1 / (S * sigma * math.sqrt(T))

    # ── Vega: sensitivity to 1% volatility change ──
    # Raw formula gives sensitivity per unit σ; divide by 100 for per-1% convention.
    vega_raw = S * Nprime_d1 * math.sqrt(T)
    vega = vega_raw / 100.0

    # ── Theta: daily time decay ──
    # Raw formula gives per-year decay; divide by 365 for per-day convention.
    theta_common = -(S * Nprime_d1 * sigma) / (2.0 * math.sqrt(T))
    if option_type == "call":
        theta_raw = theta_common - r * K * discount * N_d2
    else:
        theta_raw = theta_common + r * K * discount * norm.cdf(-d2)
    theta_daily = theta_raw / 365.0

    # ── Rho: sensitivity per 1% interest rate change ──
    # Raw formula gives per-unit rate change; divide by 100 for per-1% convention.
    if option_type == "call":
        rho = K * T * discount * N_d2 / 100.0
    else:
        rho = -K * T * discount * norm.cdf(-d2) / 100.0

    # Intrinsic value and time value.
    if option_type == "call":
        intrinsic = max(S - K, 0.0)
    else:
        intrinsic = max(K - S, 0.0)
    time_value = max(price - intrinsic, 0.0)

    return dict(
        d1=d1, d2=d2, N_d1=N_d1, N_d2=N_d2, Nprime_d1=Nprime_d1,
        delta=delta, gamma=gamma, vega=vega, theta_daily=theta_daily, rho=rho,
        option_price=price, intrinsic_value=intrinsic, time_value=time_value,
        is_itm=(S > K if option_type == "call" else S < K),
    )


def _compute_zscore(req: ZScoreRequest) -> dict:
    """
    Compute the Altman Z-Score from the five financial ratios.

    Public company: Z  = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5
    Private company: Z' = 0.717X1 + 0.847X2 + 3.107X3 + 0.420X4 + 0.998X5
    """
    X1 = req.working_capital / req.total_assets
    X2 = req.retained_earnings / req.total_assets
    X3 = req.ebit / req.total_assets           # Most predictive ratio
    X4 = req.equity_value / req.total_liabilities
    X5 = req.revenue / req.total_assets

    if req.is_public:
        # Original Altman (1968) model for publicly traded manufacturing companies.
        z = 1.2 * X1 + 1.4 * X2 + 3.3 * X3 + 0.6 * X4 + 1.0 * X5
        model = "Z"
        safe_threshold = 2.99
        distress_threshold = 1.81
    else:
        # Altman Z' model (1983) revised for private companies.
        z = 0.717 * X1 + 0.847 * X2 + 3.107 * X3 + 0.420 * X4 + 0.998 * X5
        model = "Z-prime"
        safe_threshold = 2.90
        distress_threshold = 1.23

    # Zone classification.
    if z > safe_threshold:
        zone, emoji, pd_range = "safe", "🟢", "< 2%"
    elif z < distress_threshold:
        zone, emoji, pd_range = "distress", "🔴", "12–40%+"
    else:
        zone, emoji, pd_range = "grey", "🟡", "5–15%"

    # Identify the ratio contributing least (after weighting) to the score.
    if req.is_public:
        weighted = {"X1": 1.2*X1, "X2": 1.4*X2, "X3": 3.3*X3, "X4": 0.6*X4, "X5": 1.0*X5}
    else:
        weighted = {"X1": 0.717*X1, "X2": 0.847*X2, "X3": 3.107*X3, "X4": 0.420*X4, "X5": 0.998*X5}
    weakest = min(weighted, key=weighted.get)

    return dict(
        model=model, X1=X1, X2=X2, X3=X3, X4=X4, X5=X5,
        z_score=z, zone=zone, zone_emoji=emoji,
        estimated_pd_range=pd_range, weakest_ratio=weakest,
    )


# ─── API endpoints ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["Infrastructure"])
def health_check():
    """
    Simple liveness probe. Returns 200 OK when the server is running.
    Claude's MCP connector uses this to confirm the server is reachable.
    """
    return {"status": "ok", "version": "3.0", "engine": "VKKM Aegis MCP Server",
            "capabilities": {
                "quantitative":  True,
                "live_data":     LIVE_DATA_OK,
                "backtesting":   BACKTEST_OK,
                "ml_pd":         ML_PD_OK,
                "excel_export":  EXCEL_OK,
            }}


@app.post("/monte-carlo", response_model=MonteCarloResponse, tags=["Market Risk"])
def monte_carlo_var(req: MonteCarloRequest):
    """
    Run a Monte Carlo VaR / CVaR simulation using Geometric Brownian Motion.

    Simulates N paths for each asset in the portfolio, computes weighted
    portfolio P&L per path, then derives VaR and CVaR at the requested
    confidence level and horizon.

    Returns VaR, CVaR, risk contribution per asset, and the worst
    single simulated loss (tail scenario).
    """
    # Normalise weights — warn if they don't sum to 1, but proceed.
    total_weight = sum(a.weight for a in req.assets)
    if abs(total_weight - 1.0) > 0.01:
        raise HTTPException(
            status_code=422,
            detail=f"Asset weights must sum to 1.0 (got {total_weight:.4f})."
        )

    # Run the GBM simulation engine.
    portfolio_pnl = _simulate_portfolio_gbm(
        assets=req.assets,
        portfolio_value=req.portfolio_value,
        horizon_days=req.horizon_days,
        simulations=req.simulations,
        correlation=req.correlation,
    )

    var, cvar = _compute_var_cvar(portfolio_pnl, req.confidence)

    # ── Risk contribution per asset (marginal VaR approximation) ──
    # For each asset, re-run simulation with that asset at zero weight and
    # measure the change in VaR. Normalise to 100%.
    risk_contributions = []
    for i, asset in enumerate(req.assets):
        # Remove asset i from the portfolio.
        reduced_assets = [
            PortfolioAsset(
                name=a.name,
                weight=(0.0 if j == i else a.weight),
                mu=a.mu,
                sigma=a.sigma,
            )
            for j, a in enumerate(req.assets)
        ]
        reduced_pnl = _simulate_portfolio_gbm(
            assets=reduced_assets,
            portfolio_value=req.portfolio_value,
            horizon_days=req.horizon_days,
            simulations=req.simulations,
            correlation=req.correlation,
        )
        reduced_var, _ = _compute_var_cvar(reduced_pnl, req.confidence)
        marginal_var = var - reduced_var
        risk_contributions.append({
            "asset": asset.name,
            "weight_pct": round(asset.weight * 100, 1),
            "annual_vol_pct": round(asset.sigma * 100, 1),
            "marginal_var": round(marginal_var, 2),
        })

    # Normalise contributions so they sum to 100%.
    total_marginal = sum(abs(rc["marginal_var"]) for rc in risk_contributions)
    for rc in risk_contributions:
        rc["risk_contribution_pct"] = (
            round(abs(rc["marginal_var"]) / total_marginal * 100, 1)
            if total_marginal > 0 else 0.0
        )

    return MonteCarloResponse(
        var_amount=round(var, 2),
        cvar_amount=round(cvar, 2),
        var_pct=round(var / req.portfolio_value * 100, 4),
        cvar_pct=round(cvar / req.portfolio_value * 100, 4),
        simulations_run=req.simulations,
        confidence=req.confidence,
        horizon_days=req.horizon_days,
        risk_contribution=risk_contributions,
        worst_simulation_loss=round(float(-np.min(portfolio_pnl)), 2),
    )


@app.post("/greeks", response_model=GreeksResponse, tags=["Market Risk"])
def compute_greeks(req: GreeksRequest):
    """
    Compute all five Black-Scholes Greeks for a European option.

    Returns Delta, Gamma, Vega (per 1% vol), Theta (per day), Rho (per 1% rate),
    the option price, d1, d2, and intrinsic / time value breakdown.
    """
    T = req.T_days / 365.0  # Convert calendar days to years.

    if T <= 0:
        raise HTTPException(status_code=422, detail="T_days must be > 0.")
    if req.sigma <= 0:
        raise HTTPException(status_code=422, detail="sigma (implied vol) must be > 0.")

    result = _compute_greeks(req.S, req.K, T, req.r, req.sigma, req.option_type)
    result["T_years"] = round(T, 6)

    # Round all outputs for clean presentation.
    return GreeksResponse(
        d1=round(result["d1"], 6),
        d2=round(result["d2"], 6),
        N_d1=round(result["N_d1"], 6),
        N_d2=round(result["N_d2"], 6),
        Nprime_d1=round(result["Nprime_d1"], 6),
        delta=round(result["delta"], 6),
        gamma=round(result["gamma"], 6),
        vega=round(result["vega"], 6),
        theta_daily=round(result["theta_daily"], 6),
        rho=round(result["rho"], 6),
        option_price=round(result["option_price"], 4),
        T_years=round(T, 6),
        is_itm=result["is_itm"],
        intrinsic_value=round(result["intrinsic_value"], 4),
        time_value=round(result["time_value"], 4),
    )


@app.post("/zscore", response_model=ZScoreResponse, tags=["Credit Risk"])
def compute_zscore(req: ZScoreRequest):
    """
    Calculate the Altman Z-Score from financial statement inputs.

    Automatically selects the correct model:
      - is_public=True  → Z model  (Altman 1968, for listed companies)
      - is_public=False → Z' model (Altman 1983, for private companies)

    Returns the score, zone classification, estimated PD range, and
    the weakest (lowest contributing) ratio.
    """
    result = _compute_zscore(req)
    return ZScoreResponse(**{k: (round(v, 4) if isinstance(v, float) else v)
                              for k, v in result.items()})


@app.post("/credit-risk", response_model=CreditRiskResponse, tags=["Credit Risk"])
def compute_credit_risk(req: CreditRiskRequest):
    """
    Calculate Basel credit risk metrics: Expected Loss, Unexpected Loss,
    and minimum break-even credit spread.

    EL  = PD × EAD × LGD   → priced into credit spread
    UL  = EAD × LGD × √(PD×(1−PD))  → capital held against this
    """
    el = req.pd * req.ead * req.lgd
    ul = req.ead * req.lgd * math.sqrt(req.pd * (1.0 - req.pd))

    el_pct = el / req.ead * 100.0
    ul_pct = ul / req.ead * 100.0

    # Minimum credit spread to break even on expected loss only.
    breakeven_bps = (el / req.ead) * 10_000.0

    # Simple risk rating based on EL percentage.
    if el_pct < 1.0:
        rating = "Low"
    elif el_pct < 3.0:
        rating = "Moderate"
    elif el_pct < 7.0:
        rating = "High"
    else:
        rating = "Critical"

    return CreditRiskResponse(
        expected_loss=round(el, 2),
        unexpected_loss=round(ul, 2),
        expected_loss_pct=round(el_pct, 4),
        unexpected_loss_pct=round(ul_pct, 4),
        breakeven_spread_bps=round(breakeven_bps, 1),
        risk_rating=rating,
    )


@app.post("/liquidity", response_model=LiquidityResponse, tags=["Liquidity Risk"])
def compute_liquidity(req: LiquidityRequest):
    """
    Perform liquidity risk and cash flow gap analysis.

    Builds a month-by-month cash balance table, calculates cash runway,
    and optionally computes LCR / NSFR (if banking inputs are provided).

    Identifies the first month where the cumulative balance goes negative
    (shortfall) and the trough (minimum balance) over the projection period.
    """
    # ── Cash flow gap table ──────────────────────────────────────────────────
    gap_table = []
    cumulative = req.opening_balance
    trough = req.opening_balance
    trough_month = 0
    shortfall_month = None
    total_net = 0.0
    n_months = len(req.monthly_cash_flows)

    for item in sorted(req.monthly_cash_flows, key=lambda x: x.month):
        net = item.inflows - item.outflows
        cumulative += net
        total_net += net

        if cumulative < trough:
            trough = cumulative
            trough_month = item.month

        if cumulative < 0 and shortfall_month is None:
            shortfall_month = item.month

        gap_table.append({
            "month": item.month,
            "inflows": round(item.inflows, 2),
            "outflows": round(item.outflows, 2),
            "net": round(net, 2),
            "cumulative_balance": round(cumulative, 2),
        })

    # ── Cash runway ─────────────────────────────────────────────────────────
    monthly_avg_burn = (
        -total_net / n_months if total_net < 0 else 0.0
    )

    # Runway = opening cash / average monthly net burn.
    # Only meaningful if the entity is cash-flow negative on average.
    if monthly_avg_burn > 0:
        cash_runway_months = round(req.opening_balance / monthly_avg_burn, 1)
    else:
        cash_runway_months = None  # Cash-flow positive — no "runway" calculation needed

    # ── LCR calculation (banks only) ────────────────────────────────────────
    lcr = None
    lcr_status = None
    if req.hqla is not None and req.net_cash_outflows_30d is not None:
        if req.net_cash_outflows_30d > 0:
            lcr = round(req.hqla / req.net_cash_outflows_30d, 4)
            lcr_status = "adequate" if lcr >= 1.0 else "breach"
        else:
            lcr = None
            lcr_status = "not_applicable"

    # ── NSFR calculation (banks only) ───────────────────────────────────────
    nsfr = None
    nsfr_status = None
    if req.available_stable_funding is not None and req.required_stable_funding is not None:
        if req.required_stable_funding > 0:
            nsfr = round(req.available_stable_funding / req.required_stable_funding, 4)
            nsfr_status = "adequate" if nsfr >= 1.0 else "breach"

    return LiquidityResponse(
        cash_runway_months=cash_runway_months,
        monthly_average_burn=round(monthly_avg_burn, 2),
        lcr=lcr,
        lcr_status=lcr_status,
        nsfr=nsfr,
        nsfr_status=nsfr_status,
        gap_table=gap_table,
        shortfall_month=shortfall_month,
        trough_balance=round(trough, 2),
        trough_month=trough_month,
    )


# ─── Phase 3 / v3.0 Endpoints ────────────────────────────────────────────────────────

# Pydantic models for v3.0 request / response bodies.

class MLPDRequest(BaseModel):
    """Input financial ratios for the ML Probability of Default endpoint."""
    X1: float = Field(..., description="Working Capital / Total Assets")
    X2: float = Field(..., description="Retained Earnings / Total Assets")
    X3: float = Field(..., description="EBIT / Total Assets")
    X4: float = Field(..., description="Equity Value / Total Liabilities")
    X5: float = Field(..., description="Revenue / Total Assets")
    revenue_growth:   Optional[float] = Field(None, description="Revenue growth YoY (decimal, e.g. 0.05 for 5%)")
    leverage_ratio:   Optional[float] = Field(None, ge=0.0, description="Debt / Equity ratio")
    interest_coverage: Optional[float] = Field(None, description="EBIT / Interest Expense")


class ExportRequest(BaseModel):
    """Generic export request — data field matches the source command's output."""
    report_type: Literal["kri", "gap-table", "credit-risk", "risk-register", "backtest"] = Field(
        ..., description="Type of report to export"
    )
    data: dict = Field(..., description="The structured data from a prior VKKM Aegis command")
    title: Optional[str] = Field(None, description="Optional custom report title")


@app.get("/market-data", tags=["Live Data"])
def get_market_data(ticker: str = Query(..., description="Stock ticker, e.g. AAPL, MSFT, ^GSPC")):
    """
    Fetch a live market data snapshot for a given ticker via Yahoo Finance.

    Returns the current price, 30-day and 1-year realised volatility,
    1-year annualised return (mu), and the current risk-free rate.

    Data is cached in memory for 5 minutes to avoid rate-limiting.
    Soft-fails: if Yahoo Finance is unreachable, returns null fields
    instead of a 500 error.
    """
    if not LIVE_DATA_OK:
        raise HTTPException(
            status_code=503,
            detail="Live data module unavailable. Install: pip install yfinance>=0.2.37"
        )

    live = get_live_data()
    snapshot = live.get_full_market_snapshot(ticker)
    return snapshot


@app.get("/risk-free-rate", tags=["Live Data"])
def get_risk_free_rate():
    """
    Fetch the current 3-month US Treasury Bill yield as the risk-free rate.

    Source: Yahoo Finance ^IRX ticker (annualised, decimal).
    Falls back to a hardcoded 4.5% estimate if the live feed is unavailable.
    """
    if not LIVE_DATA_OK:
        return {"rate_decimal": 0.045, "rate_pct": 4.5, "source": "fallback", "is_live": False}

    live = get_live_data()
    rate = live.fetch_risk_free_rate()

    if rate is None:
        return {"rate_decimal": 0.045, "rate_pct": 4.5, "source": "fallback (Yahoo Finance unavailable)", "is_live": False}

    return {
        "rate_decimal": round(rate, 6),
        "rate_pct":     round(rate * 100, 4),
        "source":       "Yahoo Finance ^IRX (3-month T-Bill)",
        "is_live":      True,
    }


@app.post("/backtest", tags=["Model Risk"])
async def run_backtest(
    confidence: float = Query(0.99, ge=0.90, le=0.999, description="VaR confidence level"),
    var_estimate: float = Query(..., gt=0.0, description="VaR amount being tested (positive number)"),
    file: UploadFile = File(..., description="CSV file with a 'pnl' column of daily P&L values"),
):
    """
    Run the Kupiec Proportion of Failures (POF) test on a VaR model.

    Upload a CSV file with a column named 'pnl' containing daily P&L values
    (positive = gain, negative = loss). The endpoint returns:
      - Number and rate of VaR exceptions
      - Kupiec LR statistic and p-value
      - Basel traffic light zone (Green / Yellow / Red)
      - Exception clustering analysis
      - Plain-English verdict with recommended actions

    Basel Traffic Light (250 observations, 99% VaR):
      Green  → 0–4  exceptions  → model accepted
      Yellow → 5–9  exceptions  → model under review
      Red    → 10+ exceptions  → model rejected
    """
    if not BACKTEST_OK:
        raise HTTPException(
            status_code=503,
            detail="Backtesting module unavailable. Install scipy: pip install scipy>=1.12.0"
        )

    # Read and parse the uploaded CSV.
    try:
        contents = await file.read()
        # Support both comma and semicolon separators.
        import csv, io as _io
        text = contents.decode("utf-8")
        dialect = csv.Sniffer().sniff(text[:1024], delimiters=",;\t")
        reader = csv.DictReader(_io.StringIO(text), dialect=dialect)
        rows = list(reader)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse CSV file: {e}")

    # Extract the P&L column — accept 'pnl', 'PnL', 'P&L', 'return', 'returns'.
    pnl_col = None
    for candidate in ("pnl", "PnL", "P&L", "return", "returns", "daily_pnl", "pl"):
        if rows and candidate in rows[0]:
            pnl_col = candidate
            break

    if pnl_col is None:
        raise HTTPException(
            status_code=422,
            detail=(
                f"No P&L column found. Expected one of: pnl, returns, daily_pnl. "
                f"Found columns: {list(rows[0].keys()) if rows else 'none'}"
            )
        )

    try:
        pnl_series = np.array([float(r[pnl_col]) for r in rows if r[pnl_col].strip()])
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Non-numeric value in P&L column: {e}")

    if len(pnl_series) < 20:
        raise HTTPException(
            status_code=422,
            detail=f"At least 20 observations required for backtesting (got {len(pnl_series)})."
        )

    engine = BacktestEngine()
    result = engine.run(
        pnl_series=pnl_series,
        var_estimate=var_estimate,
        confidence=confidence,
    )
    return result


@app.post("/ml-pd", tags=["Credit Risk"])
def compute_ml_pd(req: MLPDRequest):
    """
    Predict the 1-year Probability of Default using a calibrated logistic
    regression model trained on 300 synthetic companies.

    Returns:
      - pd_pct         : Predicted PD as a percentage (e.g. 8.4)
      - ci_lower_pct   : Lower bound of 95% confidence interval
      - ci_upper_pct   : Upper bound of 95% confidence interval
      - pd_label       : Risk bucket (Very Low / Low / Moderate / High / Very High)
      - z_score        : Implied Altman Z'-score for comparison
      - model_quality  : High / Moderate (based on held-out test accuracy)
      - available      : True if ML model ran; False if Z' fallback was used

    The model auto-trains on first call if pd_model.pkl is not found
    (training takes < 1 second from the bundled synthetic dataset).
    """
    if not ML_PD_OK:
        raise HTTPException(
            status_code=503,
            detail="ML PD module unavailable. Install: pip install scikit-learn>=1.4.0 joblib pandas"
        )

    features = req.model_dump(exclude_none=True)
    model = get_ml_pd_model()
    result = model.predict_pd(features)
    return result


@app.post("/export/excel", tags=["Export"])
def export_excel(req: ExportRequest):
    """
    Generate a professionally formatted .xlsx Excel report from structured
    risk analysis data produced by any VKKM Aegis command.

    Supported report types:
      - kri           → KRI Dashboard (RAG colour-coded per cell)
      - gap-table     → Cash Flow Gap Analysis (red rows on shortfalls)
      - credit-risk   → Credit Risk Assessment (EL/UL/spread)
      - risk-register → ISO 31000 Risk Register (score-based colouring)
      - backtest      → VaR Backtest Report (Basel zone highlighted)

    Returns a streaming .xlsx binary response ready for download.
    """
    if not EXCEL_OK:
        raise HTTPException(
            status_code=503,
            detail="Excel export module unavailable. Install: pip install openpyxl>=3.1.0"
        )

    report_type = req.report_type
    data        = req.data

    try:
        if report_type == "kri":
            xlsx_bytes = generate_kri_excel(data.get("kri_data", [data]))
        elif report_type == "gap-table":
            xlsx_bytes = generate_gap_table_excel(data)
        elif report_type == "credit-risk":
            xlsx_bytes = generate_credit_risk_excel(data)
        elif report_type == "risk-register":
            xlsx_bytes = generate_risk_register_excel(data.get("register", [data]))
        elif report_type == "backtest":
            xlsx_bytes = generate_backtest_excel(data)
        else:
            raise HTTPException(status_code=422, detail=f"Unknown report_type: {report_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel generation failed: {e}")

    filename = f"vkkm-aegis-{report_type}.xlsx"
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/export/json", tags=["Export"])
def export_json(req: ExportRequest):
    """
    Wrap risk analysis data in the standardised VKKM Aegis v3 JSON schema.

    Adds a metadata envelope:
        {“schema”: “vkkm-aegis-v3”, “report_type”: "...", “generated_at”: "...",
         “plugin”: "...", “data”: {...}}

    Use this endpoint to integrate VKKM Aegis output with downstream systems
    (risk data warehouses, APIs, Power BI, Tableau).
    """
    if not EXCEL_OK:
        raise HTTPException(status_code=503, detail="Export module unavailable.")

    return generate_json_export(req.data, req.report_type)


# ─── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Run with: python mcp_server.py
    # Or via uvicorn: uvicorn mcp_server:app --port 8082 --reload
    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")
