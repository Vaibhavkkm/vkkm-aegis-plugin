# VKKM Aegis — Deployment Guide (Hugging Face Spaces) 🚀

This guide explains how to host your **VKKM Aegis v3.0** backend for free so that 50+ people can use it simultaneously.

---

## 1. Is Hugging Face Spaces Free?
**Yes.** As long as you choose the **"CPU Basic"** instance type, it is **$0.00 forever.**
- **CPU:** 2 vCPUs
- **RAM:** 16GB (This is huge! It handles our 1 Million path simulations easily)
- **Disk:** 50GB

You do **not** need to enter a credit card for the free tier.

---

## 2. Setting Up the Space

1.  **Create an Account:** Go to [huggingface.co](https://huggingface.co) and sign up.
2.  **New Space:** Click the **"+" (New)** button in the top right and select **Space**.
3.  **Name Your Project:** e.g., `vkkm-aegis-engine`.
4.  **Select SDK:** Choose **Docker**.
5.  **Instance:** Choose **CPU Basic (Free - 2 vCPU · 16GB · 0.00/h)**.
6.  **Visibility:** Set to **Public** if you want others to use it easily.

---

## 3. Uploading Code

You can either connect your GitHub repo or upload files manually:
1.  Go to the **Files** tab in your new Space.
2.  Upload `mcp_server.py`, `requirements.txt`, `Dockerfile`, and the entire `data/` folder.
3.  Hugging Face will automatically start building the container. Once it says **Running**, it's live!

---

## 4. Making it "Live" on Claude

Once the building is finished, you will see a public URL. It usually looks like:
`https://<your-username>-<space-name>.hf.space`

To make it live for users:
1.  **For individual users:** They add the URL to their `claude_desktop_config.json`.
2.  **For a Claude Project:** (Easiest for a 50-person trial) 
    - Create a **Claude Project**.
    - Invite your 50 people to it.
    - Paste the `skills/risk-management/SKILL.md` into the Project Instructions.
    - Note: For the "1 Million Path" math to work in a Project, you would typically need to host the server behind an OpenAPI spec (which our FastAPI server already provides at `/openapi.json`).

---

## 5. Security Note
Hugging Face URLs are public. Since this is a trial, it's fine. If you move to "Enterprise" later, you would add an **API Key** (Bearer Token) to the headers so only your Claude plugin can talk to your server.

---

**Built by VKKM** — *Protecting you before things go wrong.*
