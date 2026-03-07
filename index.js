#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";

const API_BASE_URL = process.env.VKKM_API_URL || "https://vaibhavkkm-vkkm-aegis.hf.space";

const server = new Server(
  {
    name: "vkkm-aegis",
    version: "4.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

/**
 * Define the available tools that map to the Python API
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "monte_carlo_var",
        description: "Run a 1,000,000-path Monte Carlo VaR simulation using Geometric Brownian Motion.",
        inputSchema: {
          type: "object",
          properties: {
            assets: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  name: { type: "string" },
                  weight: { type: "number" },
                  mu: { type: "number" },
                  sigma: { type: "number" },
                },
                required: ["name", "weight", "mu", "sigma"],
              },
            },
            portfolio_value: { type: "number" },
            horizon_days: { type: "number", default: 1 },
            confidence: { type: "number", default: 0.99 },
            simulations: { type: "number", default: 1000000 },
          },
          required: ["assets", "portfolio_value"],
        },
      },
      {
        name: "greeks",
        description: "Calculate Black-Scholes Greeks (Delta, Gamma, Vega, Theta, Rho) for European options.",
        inputSchema: {
          type: "object",
          properties: {
            S: { type: "number", description: "Current price" },
            K: { type: "number", description: "Strike price" },
            T_days: { type: "number", description: "Days to expiry" },
            r: { type: "number", description: "Risk-free rate (decimal, e.g. 0.03)" },
            sigma: { type: "number", description: "Implied volatility (decimal, e.g. 0.2)" },
            option_type: { type: "string", enum: ["call", "put"] },
          },
          required: ["S", "K", "T_days", "r", "sigma", "option_type"],
        },
      },
      {
        name: "credit_risk",
        description: "Calculate Expected Loss (EL) and Unexpected Loss (UL) given PD, EAD, and LGD.",
        inputSchema: {
          type: "object",
          properties: {
            pd: { type: "number", description: "Probability of Default (decimal)" },
            ead: { type: "number", description: "Exposure at Default" },
            lgd: { type: "number", description: "Loss Given Default (decimal)" },
          },
          required: ["pd", "ead", "lgd"],
        },
      },
      {
        name: "liquidity",
        description: "Calculate Cash Runway, LCR, NSFR, and Gap Table.",
        inputSchema: {
          type: "object",
          properties: {
            opening_balance: { type: "number" },
            monthly_cash_flows: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  month: { type: "number" },
                  inflows: { type: "number" },
                  outflows: { type: "number" },
                },
                required: ["month", "inflows", "outflows"],
              },
            },
            hqla: { type: "number" },
            net_cash_outflows_30d: { type: "number" },
            available_stable_funding: { type: "number" },
            required_stable_funding: { type: "number" },
          },
          required: ["opening_balance", "monthly_cash_flows"],
        },
      },
      {
        name: "zscore",
        description: "Calculate Altman Z-Score for public or private companies.",
        inputSchema: {
          type: "object",
          properties: {
            working_capital: { type: "number" },
            total_assets: { type: "number" },
            retained_earnings: { type: "number" },
            ebit: { type: "number" },
            equity_value: { type: "number" },
            total_liabilities: { type: "number" },
            revenue: { type: "number" },
            is_public: { type: "boolean" },
          },
          required: ["working_capital", "total_assets", "retained_earnings", "ebit", "equity_value", "total_liabilities", "revenue", "is_public"],
        },
      },
      {
        name: "market_data",
        description: "Fetch live market data (price, volatility, return) via yfinance.",
        inputSchema: {
          type: "object",
          properties: {
            ticker: { type: "string" },
          },
          required: ["ticker"],
        },
      },
      {
        name: "ml_pd",
        description: "Calculate ML-based Probability of Default.",
        inputSchema: {
          type: "object",
          properties: {
            X1: { type: "number" },
            X2: { type: "number" },
            X3: { type: "number" },
            X4: { type: "number" },
            X5: { type: "number" },
            revenue_growth: { type: "number" },
            leverage_ratio: { type: "number" },
            interest_coverage: { type: "number" },
          },
        },
      },
      {
        name: "fetch_portfolio_sql",
        description: "Fetch live portfolio data directly from an enterprise SQL database.",
        inputSchema: {
          type: "object",
          properties: {
            db_url: { type: "string", description: "SQLAlchemy connection string (e.g., sqlite:///data.db, postgresql://user:pass@host/db)" },
            query: { type: "string", description: "SQL SELECT query that returns name, weight, mu, sigma columns" },
          },
          required: ["db_url", "query"],
        },
      },
    ],
  };
});

/**
 * Handle tool execution by forwarding to the Python FastAPI backend
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    let endpoint = "";
    let method = "POST";
    let data = request.params.arguments;
    let params = null;

    switch (request.params.name) {
      case "monte_carlo_var":
        endpoint = "/monte-carlo";
        break;
      case "greeks":
        endpoint = "/greeks";
        break;
      case "credit_risk":
        endpoint = "/credit-risk";
        break;
      case "liquidity":
        endpoint = "/liquidity";
        break;
      case "zscore":
        endpoint = "/zscore";
        break;
      case "market_data":
        endpoint = "/market-data";
        method = "GET";
        params = data;
        data = null;
        break;
      case "ml_pd":
        endpoint = "/ml-pd";
        break;
      case "fetch_portfolio_sql":
        endpoint = "/portfolio/sql";
        break;
      default:
        throw new Error(`Unknown tool: ${request.params.name}`);
    }

    const response = await axios({
      method,
      url: `${API_BASE_URL}${endpoint}`,
      data,
      params,
    });

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(response.data, null, 2),
        },
      ],
    };
  } catch (error) {
    const errorMsg = error.response ? JSON.stringify(error.response.data) : error.message;
    return {
      content: [
        {
          type: "text",
          text: `Error calling API: ${errorMsg}`,
        },
      ],
      isError: true,
    };
  }
});

/**
 * Start the MCP server
 */
async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("VKKM Aegis MCP Server (Node.js Connector) running on stdio");
  console.error("Backend API:", API_BASE_URL);
}

run().catch((error) => {
  console.error("Fatal error starting server:", error);
  process.exit(1);
});
