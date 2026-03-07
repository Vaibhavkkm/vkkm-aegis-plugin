"""
VKKM Aegis — Data Package (Phase 3)
=====================================
Package containing all data acquisition, backtesting, ML modeling,
and export modules for the v3.0 enterprise feature set.

Modules:
    live_data      — yfinance market data (prices, vol, risk-free rate)
    backtest       — Kupiec POF test + Basel traffic light
    generate_dataset — Synthetic default training data generator
    ml_pd_model    — scikit-learn logistic regression PD model
    excel_export   — openpyxl Excel report generator
"""
