# CS Project Database

A searchable database of high-impact CS project ideas designed to elevate your resume. Each project uses meaningfully high-level architectures (FastAPI, microservices, event-driven), modern libraries (XGBoost, LightGBM, LangChain, Celery), and strong UI components.

## 🔗 Live Demo

**[https://project-database-seven.vercel.app](https://project-database-seven.vercel.app)** — React + FastAPI on Vercel, backed by Neon Postgres.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python seed.py        # Seeds 18 projects into SQLite
uvicorn main:app --port 8001
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev          # Runs on :5173, proxies /api to :8001
```

Open http://localhost:5173

## Features

- **Keyword search** across titles, tech stacks, libraries, and tags
- **Difficulty filter** (Beginner / Intermediate / Advanced)
- **Tag filter** (ML/AI, Full-Stack, Real-Time, DevOps, Security, etc.)
- **Project detail modal** with full specs: problem, architecture, features, UI components, learning outcomes, resume impact
- **Build plan** — each project includes a detailed step-by-step build plan covering every phase, library, architecture, and UI component
- **Responsive grid** layout for browsing

## 18 Projects Included

| Project | Difficulty | Key Libraries |
|---|---|---|
| AI Code Review Pipeline | Advanced | XGBoost, OpenAI, Celery |
| Real-Time Collaborative Whiteboard | Advanced | WebSockets, CRDT, Redis |
| ML Model Registry & A/B Testing Platform | Advanced | MLflow, XGBoost, LightGBM |
| Distributed Task Orchestrator & Monitor | Advanced | Celery, Redis, APScheduler |
| Personal Finance Intelligence Engine | Intermediate | LightGBM, XGBoost, Plaid |
| Semantic Document Search & QA Platform | Intermediate | LangChain, ChromaDB, OpenAI |
| IoT Sensor Data Lake & Alerting System | Advanced | TensorFlow, TimescaleDB, MQTT |
| API Gateway & Developer Portal | Intermediate | Redis, Traefik, OpenAPI |
| Social Media OSINT Analyzer | Advanced | Neo4j, Playwright, D3.js |
| Multi-Agent AI Workflow Engine | Advanced | LangChain, React Flow, Celery |
| Infrastructure Cost Optimizer | Intermediate | XGBoost, boto3, Azure SDK |
| Real-Time Dashboard Builder | Intermediate | react-grid-layout, Recharts |
| AI-Powered Meeting Minutes & Action Tracker | Advanced | Whisper, LangChain, Google/Outlook API |
| ML Data Drift Monitor & Alert System | Advanced | Evidently AI, XGBoost, LightGBM |
| Competitive Programming Arena | Advanced | Docker SDK, Monaco Editor |
| Hackathon Hub — Event & Project Manager | Intermediate | WebSockets, react-beautiful-dnd |
| Personal Knowledge Graph & Second Brain | Intermediate | Neo4j, OpenAI embeddings, TipTap |
| API Security Fuzzer & Vulnerability Scanner | Advanced | httpx, OWASP, CI/CD |

## Inspired By

- [career-ops](https://github.com/santifer/career-ops) — AI-powered job search system
- [maigret](https://github.com/soxoj/maigret) — OSINT username search across 3000+ sites
- [Archon](https://github.com/coleam00/Archon) — AI coding workflow engine
