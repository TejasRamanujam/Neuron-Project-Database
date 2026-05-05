from pydantic import BaseModel
from typing import List, Optional


class ProjectBase(BaseModel):
    title: str
    subtitle: str
    description: str
    problem_statement: str
    tech_stack: List[str]
    architectures_used: List[str]
    libraries_used: List[str]
    difficulty: str
    estimated_time: str
    ui_components: List[str]
    repo_inspiration: List[str]
    resume_gap_filled: str
    key_features: List[str]
    learning_outcomes: List[str]
    tags: List[str]


class ProjectResponse(ProjectBase):
    id: int

    model_config = {"from_attributes": True}


class SearchParams(BaseModel):
    query: Optional[str] = ""
    tags: Optional[List[str]] = None
    difficulty: Optional[List[str]] = None
    min_learning: Optional[int] = None
