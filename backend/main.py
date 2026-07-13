import json
import os
import urllib.request

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, cast, String
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db, engine, Base
from models import Project
from schemas import ProjectResponse, TailorRequest, TailorResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Database API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/projects", response_model=List[ProjectResponse])
def list_projects(
    query: Optional[str] = Query("", description="Search in title, subtitle, description, tags"),
    tags: Optional[str] = Query(None, description="Comma-separated tag filter"),
    difficulty: Optional[str] = Query(None, description="Comma-separated difficulty filter"),
    db: Session = Depends(get_db),
):
    q = db.query(Project)

    if query:
        like = f"%{query}%"
        q = q.filter(
            or_(
                Project.title.ilike(like),
                Project.subtitle.ilike(like),
                Project.description.ilike(like),
                cast(Project.tags, String).ilike(like),
                cast(Project.tech_stack, String).ilike(like),
                cast(Project.libraries_used, String).ilike(like),
            )
        )

    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        for tag in tag_list:
            q = q.filter(cast(Project.tags, String).ilike(f"%{tag}%"))

    if difficulty:
        diff_list = [d.strip() for d in difficulty.split(",") if d.strip()]
        q = q.filter(Project.difficulty.in_(diff_list))

    return q.order_by(Project.title).all()


@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.id == project_id).first()


@app.post("/api/projects/{project_id}/tailor", response_model=TailorResponse)
def tailor_plan(project_id: int, body: TailorRequest, db: Session = Depends(get_db)):
    """Rewrite a project's build plan for the visitor's constraint via Gemini."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="AI tailoring is not configured")
    p = db.query(Project).filter(Project.id == project_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Project not found")
    constraint = body.constraint.strip()[:300]
    if not constraint:
        raise HTTPException(status_code=422, detail="Constraint is empty")

    prompt = (
        "You are the archivist of a catalogue of CS project build plans. "
        f'Rewrite the build plan below for a builder with this constraint: "{constraint}".\n'
        "Keep the exact markdown dialect of the original: '## Phase N: Title' headings, "
        "each phase containing '**Step N: title.** body' paragraphs separated by blank lines. "
        "Use 3 to 5 phases. Be concrete about tools and order of work; no preamble before "
        "the first heading and nothing after the last step.\n\n"
        f"Project: {p.title} — {p.subtitle}\n"
        f"Description: {p.description}\n\n"
        f"Original plan:\n{p.build_plan}"
    )
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    )
    try:
        out = json.load(urllib.request.urlopen(req, timeout=55))
        text = out["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raise HTTPException(status_code=502, detail="The archivist could not draft the plan")
    return {"plan": text}


@app.get("/api/tags")
def list_tags(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    tag_set = set()
    for p in projects:
        for t in p.tags:
            tag_set.add(t)
    return sorted(tag_set)


@app.get("/api/difficulties")
def list_difficulties(db: Session = Depends(get_db)):
    projects = db.query(Project.difficulty).distinct().all()
    return sorted([d[0] for d in projects])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
