from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, cast, String
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db, engine, Base
from models import Project
from schemas import ProjectResponse

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
