from src.llm import LLM
from src.utils import to_json, extract_json
from src.data_models import ProjectSpec, OrchestratorState, Constraint
from src.utils import normalize_spec
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import asdict
import json

def planning_node(state: OrchestratorState) -> OrchestratorState:
    prompt_sys = (
        "You are an agile tech lead. Turn user stories and architecture into a plan: "
        "epics, tasks, estimates, and dependencies."
    )
    
    prompt_user = (
        f"Stories: {to_json(state.get('user_stories', []))}\n"
        f"Arch: {to_json(state.get('architecture', {}))}\n"
        f"Return JSON with field 'plan' as a list."
    )

    text = LLM.complete(system=prompt_sys, user=prompt_user)
    # print("LLM raw response (truncated):", text[:10])  

    data = extract_json(text)
    plan = data.get("plan", [])

    return {**state, "plan": plan}


if __name__ == "__main__":
    sample_state = {
        "spec": {
            "project_name": "Task Manager",
            "description": "A simple task management app",
            "features": ["add task", "list tasks", "mark task done"],
            "constraints": {"tech_stack": "Python + FastAPI"}
        },
        "user_stories": [
            {
                "id": "US001",
                "title": "As a user, I want to add a task",
                "acceptance_criteria": [
                    "User can enter a task description",
                    "Task is saved and visible in task list"
                ],
                "priority": "High"
            },
            {
                "id": "US002",
                "title": "As a user, I want to list my tasks",
                "acceptance_criteria": [
                    "System shows all tasks with descriptions",
                    "Tasks can be sorted by due date"
                ],
                "priority": "High"
            }
        ],
        "architecture": {
            "services": [
                {"name": "API Gateway", "description": "Handles incoming API requests"},
                {"name": "Task Service", "description": "Manages task CRUD operations"}
            ]
        }
    }

    result = planning_node(sample_state)

    print("=== Final Plan Output ===")
    print(json.dumps(result, indent=2))
