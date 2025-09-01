from src.llm import LLM
from src.utils import to_json, extract_json
from src.data_models import ProjectSpec, OrchestratorState, Constraint
from src.utils import normalize_spec
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import asdict
import json


def requirements_node(state: OrchestratorState) -> OrchestratorState:
    spec = normalize_spec(state["spec"])
    prompt_sys = (
        "You are a senior product manager. Convert the input spec into precise, testable user stories. "
        "Use INVEST. Include acceptance criteria and non-functional requirements when relevant."
    )
    prompt_user = f"SPEC:\n{to_json(asdict(spec))}\nReturn JSON with fields: user_stories[]."

    text = LLM.complete(system=prompt_sys, user=prompt_user)
    # print("LLM response (truncated):", text[:1000])

    # Extract the first valid JSON object
    data = extract_json(text)
    stories = data.get("user_stories", [])
    return {**state, "user_stories": stories}


if __name__ == "__main__":
    sample_state = {
        "spec": {
            "project_name": "Task Manager",
            "description": "A simple task management app",
            "features": ["add task", "list tasks", "mark task done"],
            "constraints": {"tech_stack": "Python + FastAPI"}
        }
    }

    result = requirements_node(sample_state)
    print(json.dumps(result, indent=2))
