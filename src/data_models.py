from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import dataclass

@dataclass
class Constraint:
    tech_stack: Optional[str] = None
    deployment: Optional[str] = None
    priority: Optional[Literal["high", "medium", "low"]] = None

@dataclass
class ProjectSpec:
    project_name: str
    description: str
    features: List[str]
    constraints: Constraint

class OrchestratorState(TypedDict, total=False):
    spec: Dict[str, Any]
    user_stories: List[Dict[str, Any]]
    architecture: Dict[str, Any]
    plan: List[Dict[str, Any]]
    code_changes: Dict[str, str]
    tests: Dict[str, str]
    test_report: Dict[str, Any]
    ci_cd: Dict[str, str]
    deployment: Dict[str, Any]
    approvals: Dict[str, Any]
    repo_url: Optional[str]
    run_id: Optional[str]
