# Privacy Policy for VKKM Aegis Risk Management

**Last Updated:** March 2026

VKKM Aegis ("we", "our", or "the plugin") respects your privacy. This Privacy Policy explains how we handle the data you provide when using the VKKM Aegis Risk Management plugin via the Claude Model Context Protocol (MCP).

## 1. Data Collection & Processing
VKKM Aegis operates as a **stateless mathematical calculation engine**. 
- We **do not** collect personal identifiable information (PII) such as your name, email address, or IP address. 
- We **do not** require user accounts or logins.
- Any portfolio data, financial inputs, credit metrics, or contracts you provide to the plugin are routed strictly for instantaneous calculation.

## 2. Data Storage & Retention
The Python backend (hosted via Hugging Face Spaces) **does not use a database**. 
- Financial inputs received from Claude are held in volatile memory (RAM) only for the milliseconds required to compute the Monte Carlo VaR, Black-Scholes Greeks, or Machine Learning output.
- Once the calculation payload is returned to your Claude chat session, your input data is **immediately and permanently destroyed** from our servers.
- We do not store, log, track, or save your chat history, prompts, or proprietary financial figures.

## 3. Third-Party Services
VKKM Aegis fetches purely external, publicly available structural data required for financial modeling:
- **yfinance:** We anonymously query Yahoo Finance APIs to fetch live ticker prices, historical returns, and rolling volatility. No user information is transmitted during these requests.

## 4. Security
We rely exclusively on Anthropic's secure Model Context Protocol (MCP) and Hugging Face's containerized infrastructure to encrypt data in transit between your Claude interface and our backend engine. 

## 5. Contact
If you have any questions about this privacy statement or the stateless nature of our calculation engine, you may inspect the open-source architecture at [https://github.com/Vaibhavkkm/vkkm-aegis-plugin](https://github.com/Vaibhavkkm/vkkm-aegis-plugin) or contact the author via vaibhavkkm.com.
