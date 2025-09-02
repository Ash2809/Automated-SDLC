from src.llm import LLM
from src.utils import to_json, extract_json
from src.data_models import ProjectSpec, OrchestratorState, Constraint
from src.utils import normalize_spec
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import asdict
import json


def implementation_node(state: OrchestratorState) -> OrchestratorState:
    spec = normalize_spec(state["spec"])
    prompt_sys = (
        "You are a senior engineer. Generate minimal, production-ready code skeletons with docstrings and TODOs. "
        "Prefer simplicity and testability."
    )
    
    prompt_user = (
    f"Tech stack: {spec.constraints.tech_stack}\nPlan: {to_json(state.get('plan', []))}\n"
    "Output JSON with key 'code_changes' as {filename: content}. "
    "IMPORTANT: Return raw JSON only. Do not wrap code in markdown fences (no ```python, no ```). "
    "Each file's content must be a plain string value inside JSON."
    )


    text = LLM.complete(prompt_sys, prompt_user)
    print("LLM raw response (truncated):", text[:500])  

    try:
        data = extract_json(text)
        code_changes = data.get("code_changes", {})
    except Exception as e:
        print("Failed to parse JSON:", e)
        code_changes = {}

    return {**state, "code_changes": code_changes}


if __name__ == "__main__":
    sample_state = {
        "spec": {
            "project_name": "Task Manager",
            "description": "A simple task management app",
            "features": ["add task", "list tasks", "mark task done"],
            "constraints": {"tech_stack": "Python + FastAPI"}
        },
        "plan": [
            {
                "epic": "Task CRUD",
                "tasks": [
                    {"id": "T001", "description": "Implement add task API", "estimate": "2d"},
                    {"id": "T002", "description": "Implement list tasks API", "estimate": "1d"}
                ]
            }
        ]
    }

    result = implementation_node(sample_state)

    print("=== Final Code Changes ===")
    for filename, content in result.get("code_changes", {}).items():
        print(f"\n--- {filename} ---\n{content[:300]}...\n")
