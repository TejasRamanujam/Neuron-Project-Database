# Neuron — Project Database

![CI](https://github.com/TejasRamanujam/Neuron-Project-Database/actions/workflows/ci.yml/badge.svg)

**Live: https://neuron-database.vercel.app**

A searchable catalogue of CS project build plans: keyword search, tag filtering, and difficulty grading over a REST API.

## Features
- Full-text search across 24 curated project specs
- Filter by difficulty grade and taxonomy tags
- Each entry: stack, taxonomy, and a complete build plan
- Keyboard-first navigation

## Stack
React + TypeScript (Vite) · FastAPI on Vercel functions · SQLAlchemy · Neon Postgres

## Run locally
```bash
cd frontend && npm install && npm run dev
cd backend && pip install -r ../requirements.txt && uvicorn main:app --reload
```
