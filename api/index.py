"""Vercel serverless entrypoint for the Project Database API.

Self-contained FastAPI app (mirrors backend/main.py) so Vercel's Python
build traces all dependencies reliably. Reads DATABASE_URL (Neon Postgres
in production; falls back to SQLite locally).
"""
import os
from typing import Optional, List

from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, or_, cast, String, Column, Integer, Text, JSON
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from pydantic import BaseModel

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./projects.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    problem_statement = Column(Text, nullable=False)
    tech_stack = Column(JSON, nullable=False)
    architectures_used = Column(JSON, nullable=False)
    libraries_used = Column(JSON, nullable=False)
    difficulty = Column(String, nullable=False)
    build_plan = Column(Text, nullable=False)
    ui_components = Column(JSON, nullable=False)
    repo_inspiration = Column(JSON, nullable=False)
    resume_gap_filled = Column(Text, nullable=False)
    key_features = Column(JSON, nullable=False)
    learning_outcomes = Column(JSON, nullable=False)
    tags = Column(JSON, nullable=False)


class ProjectResponse(BaseModel):
    id: int
    title: str
    subtitle: str
    description: str
    problem_statement: str
    tech_stack: list
    architectures_used: list
    libraries_used: list
    difficulty: str
    build_plan: str
    ui_components: list
    repo_inspiration: list
    resume_gap_filled: str
    key_features: list
    learning_outcomes: list
    tags: list

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
