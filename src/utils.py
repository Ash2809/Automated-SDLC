import json, re
from typing import Any, Dict
from dataclasses import asdict
from .data_models import ProjectSpec, Constraint

def normalize_spec(raw: Dict[str, Any]) -> ProjectSpec:
    constraints = raw.get("constraints") or {}
    return ProjectSpec(
        project_name=raw.get("project_name", "Untitled Project"),
        description=raw.get("description", ""),
        features=list(raw.get("features", [])),
        constraints=Constraint(
            tech_stack=constraints.get("tech_stack"),
            deployment=constraints.get("deployment"),
            priority=constraints.get("priority"),
        ),
    )

def to_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {}
    return {}
