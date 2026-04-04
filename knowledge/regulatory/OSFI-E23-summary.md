# OSFI Guideline E-23 — Model Risk Management Summary

**Source:** Office of the Superintendent of Financial Institutions (OSFI)
**Effective:** May 1, 2027 (all federally regulated financial institutions)
**Document type:** Public regulatory summary — safe for reference

---

## What It Is

OSFI E-23 requires all federally regulated financial institutions (FRFIs) — banks, insurance companies, trust companies — to implement enterprise-wide model risk management (MRM) frameworks covering AI and ML models through their full lifecycle.

---

## Who It Affects

Any model used to make or inform decisions at a regulated FI:
- Credit scoring models
- Fraud detection models
- AML/transaction monitoring models
- Risk quantification models (market, credit, operational)
- Customer segmentation and targeting models
- AI tools used in regulated decisions

---

## Key Requirements

### 1. Model Inventory
- All models must be catalogued in a central inventory
- Include model purpose, data inputs, outputs, owner, and last validation date
- Covers internal models AND third-party/vendor models ("black box" models)

### 2. Model Validation
- Independent validation required before deployment
- Ongoing periodic revalidation
- Challenger model testing where feasible
- Particular scrutiny for models using unstructured data or LLMs

### 3. Governance
- Board/senior management accountability for MRM
- Clear ownership (model developer vs. validator vs. user)
- Multi-disciplinary review including legal, ethics, and risk
- Change management: material model changes require re-validation

### 4. Third-Party Models
- Banks cannot disclaim responsibility for vendor models
- Must assess black-box models for explainability and bias
- Data processing agreements required for external AI APIs
- Vendor risk assessments must address model transparency

### 5. Documentation
- All model development, validation, and change decisions must be documented
- Rationale for model selection and rejection of alternatives
- Known limitations and assumptions must be disclosed

---

## Implications for AI Tools

Any AI tool that informs a regulated decision (credit, fraud, risk, compliance) falls under E-23:
- Generic LLM APIs used in regulated workflows = third-party model under E-23
- Requires: vendor assessment, DPA, explainability review, change management process
- Note: E-23 does NOT apply to productivity/drafting tools that don't directly inform regulated decisions

---

## Compliance Deadline

**May 1, 2027** — full MRM framework must be operational at all FRFIs

---

## BA/BSA Relevance

When writing requirements for any AI or ML feature:
- Add NFR: "Model must be inventoried per OSFI E-23 model inventory requirements"
- Add NFR: "Model documentation must meet OSFI E-23 validation standards"
- Add AC: "Compliance/Risk team has reviewed model for E-23 applicability"
- Flag any third-party AI API as requiring vendor risk assessment

---

*Public source: osfi-bsif.gc.ca | Last reviewed: 2026-04*
