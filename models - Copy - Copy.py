from pydantic import BaseModel, Field
from typing import Optional, List

class RepoRequest(BaseModel):
    source: str = Field(..., min_length=1)

class TaskRequest(BaseModel):
    repo_path: str
    task: str = Field(..., min_length=3)

class TestRequest(BaseModel):
    repo_path: str
    command: Optional[str] = None

class PatchRequest(BaseModel):
    repo_path: str
    task: str
    patch: str

class LoopRequest(BaseModel):
    repo_path: str
    task: str
    max_attempts: int = Field(default=2, ge=1, le=3)
