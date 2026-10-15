# GreenCampus AI — Agentic Campus Energy Optimizer

A responsive React + TypeScript + Vite MVP for campus energy monitoring. The local demo includes seeded 30-day meter readings, explainable anomaly rules, a bounded agent workflow, approval-gated recommendations, simulated action records, charts, CSV import/export, report export, configurable assumptions, and browser persistence.

## Requirements
- Node.js 20+ and npm
- Optional Python 3.10+ for the SQLite/FastAPI API starter

## Run the frontend
```bash
npm install
npm run dev
```
Open the local URL printed by Vite. No API key or backend is required for the demo.

## Build and tests
```bash
npm run build
npm test
```

## Optional FastAPI + SQLite API
The frontend currently persists to browser `localStorage`; it does not automatically connect to the API. Start the optional API separately:
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```
API health: `GET http://localhost:8000/health`; CRUD: `GET /api/records`, `PUT /api/records/{record_id}`, `DELETE /api/records/{record_id}`. The SQLite database is created at `backend/greencampus.db` by default. Set `GREEN_CAMPUS_DB` to choose another location and `CORS_ORIGINS` to configure allowed origins. Add authentication and authorization before any public deployment.

## Main structure
```text
greencampus-ai/
├── src/
│   ├── App.tsx          # App shell, pages, workflows and UI interactions
│   ├── engine.ts        # Seed data, calculations, anomaly rules, CSV helpers
│   ├── main.tsx         # React entry point
│   └── styles.css       # Responsive design system
├── backend/
│   ├── main.py          # Optional FastAPI + SQLite CRUD API
│   └── requirements.txt
├── tests/engine.test.ts # Deterministic calculation and detection tests
├── index.html
├── package.json
└── vite.config.ts
```

## Demo walkthrough
1. Open Overview and click **Run analysis**.
2. The agent logs reading retrieval, data validation, anomaly detection, ranking and action-plan creation.
3. Open Recommendations & actions and review the lab after-hours signal or the engineering-block spike.
4. Click **Approve**, then **Start work**, then **Mark simulated complete**.
5. Sustainability Impact reflects a provisional estimate, explicitly labelled simulated. Real savings require comparable follow-up meter readings; no physical equipment is controlled.

## Data and safety notes
- Seed data is deterministic and clearly simulated; five buildings have 30 daily readings each.
- Baseline comparisons are simple daily comparisons and are not normalized for weather/occupancy in this MVP.
- Carbon factor `0.716 kg CO2e/kWh` is a demo assumption, not asserted as an official regional factor.
- Estimated potential savings are not actual savings. The demo's completion workflow records a provisional estimate, not independently verified savings.
- Local browser data persists across refreshes in the same browser profile. Reset Demo restores the seeded state after confirmation.
- No LLM or device integration is configured. Rules and calculations are deterministic. Never put API keys in frontend code.
