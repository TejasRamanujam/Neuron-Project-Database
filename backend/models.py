from sqlalchemy import Column, Integer, String, Text, JSON
from database import Base


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
    estimated_time = Column(String, nullable=False)
    ui_components = Column(JSON, nullable=False)
    repo_inspiration = Column(JSON, nullable=False)
    resume_gap_filled = Column(Text, nullable=False)
    key_features = Column(JSON, nullable=False)
    learning_outcomes = Column(JSON, nullable=False)
    tags = Column(JSON, nullable=False)
