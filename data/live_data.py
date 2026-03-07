#!/usr/bin/env python3
"""
VKKM Aegis — Live Market Data Module (Phase 3)
================================================
Provides soft-failure wrappers around yfinance to fetch real-time and
historical market data. All functions return None on network or API errors
so the MCP server NEVER crashes — it simply falls back to ILLUSTRATIVE mode.

Fetched data is cached in memory for 5 minutes to avoid hammering Yahoo
Finance on repeated requests within the same session.

Usage:
    from data.live_data import LiveMarketData
    data = LiveMarketData()
    price = data.fetch_price("AAPL")   # Returns float or None

Author : VKKM (vaibhavkkm.com)
Version: 3.0
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple, Any

import numpy as np

# yfinance is an optional dependency — import safely.
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logging.warning(
        "yfinance not installed — live market data unavailable. "
        "Run: pip install yfinance>=0.2.37"
    )

logger = logging.getLogger(__name__)

# ─── In-memory cache ─────────────────────────────────────────────────────────

# Simple TTL cache to avoid hitting Yahoo Finance rate limits.
# Maps cache_key -> (timestamp, value). An in-memory dict works fine 
# for a lightweight MCP server; no need to stand up Redis yet.
_CACHE: Dict[str, Tuple[float, Any]] = {}
_CACHE_TTL_SECONDS = 300  # 5 minutes


def _cache_get(key: str):
    """Return cached value or None if missing / expired."""
    if key in _CACHE:
        ts, value = _CACHE[key]
        if time.time() - ts < _CACHE_TTL_SECONDS:
            return value
        del _CACHE[key]
    return None


def _cache_set(key: str, value) -> None:
    """Store a value in the cache with the current timestamp."""
    _CACHE[key] = (time.time(), value)


# ─── LiveMarketData class ─────────────────────────────────────────────────────

class LiveMarketData:
    """
    Soft-failure wrapper around Yahoo Finance for real-time and historical
    market data. Never raises exceptions — returns None on any failure.

    All returned values are checked and validated before being returned
    to prevent corrupted data from flowing into risk calculations.
    """

    def fetch_price(self, ticker: str) -> Optional[float]:
        """
        Return the latest closing price for a ticker.

        Tries the 'fast info' endpoint first (low-latency single-value).
        Falls back to downloading the last 2-day OHLCV series.

        Returns:
            float  — last closing price in the ticker's native currency
            None   — if ticker invalid, offline, or rate-limited
        """
        if not YFINANCE_AVAILABLE:
            return None

        cache_key = f"price:{ticker.upper()}"
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            stock = yf.Ticker(ticker)
            # First attempt: Try the 'fast_info' property. It avoids full history 
            # downloads and is significantly faster + less prone to rate limits.
            # (Note: yfinance changed the key from lastPrice to last_price in v0.2.x)
            price = stock.fast_info.get("last_price") or stock.fast_info.get("lastPrice")
            if price and price > 0:
                _cache_set(cache_key, float(price))
                logger.info(f"Live price fetched: {ticker} = {price}")
                return float(price)

            # Fallback: download last 2 trading days
            hist = stock.history(period="2d")
            if hist.empty:
                logger.warning(f"No price data returned for ticker: {ticker}")
                return None
            price = float(hist["Close"].iloc[-1])
            _cache_set(cache_key, price)
            return price

        except Exception as e:
            logger.warning(f"fetch_price({ticker}) failed: {e}")
            return None

    def fetch_realised_vol(self, ticker: str, window: int = 30) -> Optional[float]:
        """
        Compute the annualised realised (historical) volatility over the
        last `window` trading days from daily log-returns.

        Formula:
            σ_annualised = std(log(P_t / P_{t-1})) × √252

        Returns:
            float  — annualised volatility as a decimal (e.g. 0.22 for 22%)
            None   — on any failure
        """
        if not YFINANCE_AVAILABLE:
            return None

        cache_key = f"vol:{ticker.upper()}:{window}"
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            # Download window + 5 extra days to account for market holidays.
            stock = yf.Ticker(ticker)
            hist = stock.history(period=f"{window + 10}d")
            if hist.empty or len(hist) < 5:
                logger.warning(f"Insufficient price history for {ticker}")
                return None

            # Calculate daily log-returns from closing prices.
            # We use log returns since they are time-additive, which is standard for Vol calculations.
            closes = hist["Close"].values
            log_returns = np.log(closes[1:] / closes[:-1])
            # Take the final `window` returns.
            log_returns = log_returns[-window:]

            vol = float(np.std(log_returns, ddof=1) * np.sqrt(252))
            if vol <= 0:
                return None

            _cache_set(cache_key, vol)
            logger.info(f"Realised vol fetched: {ticker} ({window}d) = {vol:.4f}")
            return vol

        except Exception as e:
            logger.warning(f"fetch_realised_vol({ticker}) failed: {e}")
            return None

    def fetch_historical_returns(
        self, ticker: str, years: int = 3
    ) -> Optional[np.ndarray]:
        """
        Return an array of daily log-returns for the past `years` years.
        Used as the raw input for historical VaR and backtesting.

        Returns:
            np.ndarray  — shape (N,) daily log-returns
            None        — on failure
        """
        if not YFINANCE_AVAILABLE:
            return None

        cache_key = f"returns:{ticker.upper()}:{years}y"
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            end   = datetime.now()
            start = end - timedelta(days=years * 365 + 30)
            stock = yf.Ticker(ticker)
            hist  = stock.history(start=start.strftime("%Y-%m-%d"),
                                  end=end.strftime("%Y-%m-%d"))

            if hist.empty or len(hist) < 30:
                logger.warning(f"Insufficient history for {ticker} ({years}yr)")
                return None

            closes  = hist["Close"].values
            returns = np.log(closes[1:] / closes[:-1])
            _cache_set(cache_key, returns)
            logger.info(f"Returns fetched: {ticker} ({years}yr) → {len(returns)} days")
            return returns

        except Exception as e:
            logger.warning(f"fetch_historical_returns({ticker}) failed: {e}")
            return None

    def fetch_risk_free_rate(self) -> Optional[float]:
        """
        Fetch the current annualised 3-month US Treasury Bill yield as the
        risk-free rate (^IRX ticker on Yahoo Finance, quoted in percent).

        Returns:
            float  — annual risk-free rate as a decimal (e.g. 0.0435 for 4.35%)
            None   — on failure (caller should use a sensible default like 0.04)
        """
        if not YFINANCE_AVAILABLE:
            return None

        cache_key = "rfr:3m"
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

        try:
            tbill = yf.Ticker("^IRX")
            hist  = tbill.history(period="5d")
            if hist.empty:
                return None

            # ^IRX is quoted in percent (e.g. 5.22 for 5.22%).
            rate_pct = float(hist["Close"].iloc[-1])
            rate     = rate_pct / 100.0

            if rate < 0 or rate > 0.25:  # Sanity check: 0–25% range
                logger.warning(f"Implausible risk-free rate: {rate:.4f}")
                return None

            _cache_set(cache_key, rate)
            logger.info(f"Risk-free rate: {rate:.4f} ({rate_pct:.2f}%)")
            return rate

        except Exception as e:
            logger.warning(f"fetch_risk_free_rate() failed: {e}")
            return None

    def get_full_market_snapshot(self, ticker: str) -> dict:
        """
        Return a consolidated market data snapshot for a ticker.
        This is what the /market-data endpoint returns — all four
        data points in a single call.

        Always returns a dict — partial data (some None values) is valid.
        The caller checks which fields are populated.
        """
        price    = self.fetch_price(ticker)
        vol_30d  = self.fetch_realised_vol(ticker, window=30)
        vol_1yr  = self.fetch_realised_vol(ticker, window=252)
        rfr      = self.fetch_risk_free_rate()

        # Compute simple annualised return (mu) from 1-year price change.
        mu_1yr = None
        try:
            hist = yf.Ticker(ticker).history(period="1y") if YFINANCE_AVAILABLE else None
            if hist is not None and len(hist) >= 2:
                mu_1yr = float(
                    np.log(hist["Close"].iloc[-1] / hist["Close"].iloc[0])
                )
        except Exception:
            pass

        is_live = price is not None
        label   = "DATA-GROUNDED" if is_live else "ILLUSTRATIVE ESTIMATE"

        return {
            "ticker":             ticker.upper(),
            "last_price":         price,
            "realised_vol_30d":   vol_30d,
            "realised_vol_1yr":   vol_1yr,
            "annual_return_1yr":  mu_1yr,
            "risk_free_rate":     rfr,
            "data_label":         label,
            "is_live":            is_live,
            "cache_ttl_seconds":  _CACHE_TTL_SECONDS,
        }


# Module-level singleton — reuse to benefit from cache.
_live_data = LiveMarketData()


def get_live_data() -> LiveMarketData:
    """Return the module-level LiveMarketData singleton."""
    return _live_data
