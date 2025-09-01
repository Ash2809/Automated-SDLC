from src.llm import LLM
from src.utils import to_json, extract_json
from src.data_models import ProjectSpec, OrchestratorState, Constraint
from src.utils import normalize_spec
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import asdict
import json

def design_node(state : OrchestratorState) -> OrchestratorState:
    spec = normalize_spec(state["spec"])

    prompt_sys = (
        "You are a pragmatic software architect. Propose a simple, scalable architecture. "
        "Include: system diagram (text), services, data model, API contracts, and key trade-offs."
    )
    prompt_user = (
        f"PROJECT: {spec.project_name}\nDESC: {spec.description}\nFEATURES: {to_json(spec.features)}\n"
        f"CONSTRAINTS: {to_json(asdict(spec.constraints))}\nReturn JSON field 'architecture'."
    )

    text = LLM.complete(system=prompt_sys, user=prompt_user)
    # print("LLM raw response:", text[:100])

    data = extract_json(text)
    arch = data.get("architecture", {})

    return {**state, "architecture": arch}


if __name__ == "__main__":
    sample_state = {
        "spec": {
            "project_name": "Task Manager",
            "description": "A simple task management app",
            "features": ["add task", "list tasks", "mark task done"],
            "constraints": {"tech_stack": "Python + FastAPI"}
        }
    }

    result = design_node(sample_state)
    print("=== Final Output ===")
    print(json.dumps(result, indent=2))

