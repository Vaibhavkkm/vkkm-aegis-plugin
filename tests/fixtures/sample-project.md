# Sample Project Brief — VKKM PayTrack

> **Test fixture for:** `/vkkm:risk-register` and `/vkkm:regulatory-check`
> **Paste this document into Claude and run the relevant command.**

---

## Project Overview

**Project Name:** VKKM PayTrack  
**Industry:** Fintech / B2B SaaS  
**Stage:** Pre-launch (4 weeks to go-live)  
**Region:** European Union (Germany-based, EU customer base)  
**Team Size:** 8 people (6 employees, 2 contractors)  
**Runway:** 18 months  

## What We're Building

PayTrack is a B2B SaaS platform that helps SMEs automatically reconcile their business
bank accounts with their accounting software. The platform:

1. Connects directly to business bank accounts via open banking (PSD2 / EU AISP access)
2. Reads transaction history and categorizes transactions automatically using AI
3. Syncs reconciled data into QuickBooks, Xero, and DATEV automatically
4. Provides a dashboard for finance leads and CFOs
5. Stores transaction data and PII (business owner names, account numbers) on AWS (Frankfurt region)

## Technology Stack

- Backend: Node.js on AWS EC2 (Frankfurt)
- Database: PostgreSQL on AWS RDS
- Authentication: Auth0
- Open Banking: Plaid EU + directly licensed AISP via Finapi (German TPP)
- AI categorization: OpenAI GPT-4o via API (data sent to OpenAI for processing)
- Payment: Stripe for subscription billing

## Current Status

- MVP is built and in private beta with 5 SME clients
- PSD2 AISP license: under application via Finapi — not yet confirmed
- GDPR: Privacy policy drafted, DPA with AWS signed, DPA with OpenAI pending
- SOC 2 Type I pending; no audit completed yet
- No penetration test completed
- No formal incident response plan in place

## Revenue Model

- Subscription: €49/month (SME) / €149/month (Growth tier)
- 12 target enterprise clients identified for outreach at €800+/month
- 5 current beta clients paying €0 (will convert at launch)

## Known Risks (as identified by the team)

1. We're not sure if we need a separate BaFin license beyond the AISP via Finapi
2. OpenAI API processes our users' financial transaction data — we haven't confirmed if this is GDPR-compliant
3. Our lead developer is the only person who understands the bank reconciliation core algorithm
4. AWS pricing may increase significantly if we grow faster than modeled

---

_Use this project brief with `/vkkm:risk-register` or `/vkkm:regulatory-check`_
