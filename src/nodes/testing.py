from src.llm import LLM
from src.utils import to_json, extract_json
from src.data_models import ProjectSpec, OrchestratorState, Constraint
from src.utils import normalize_spec
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import asdict
import json


def testing_node(state : OrchestratorState) -> OrchestratorState:
    prompt_sys = (
        "You are a test engineer. Generate unit & integration tests to cover core behaviors."
    )
    prompt_user = (
        f"Given code files: {list((state.get('code_changes') or {}).keys())}\n"
        "Return JSON with 'tests' (filename->content) and 'test_plan' summary."
    )

    text = LLM.complete(prompt_sys, prompt_user)

    print("LLM raw response (truncated):", text[:500])

    tests: Dict[str, str]
    test_plan: Dict[str, Any]

    try:
        data = extract_json(text)
        tests = data.get("tests", {})
        test_plan = data.get("test_plan", {})

    except Exception as e:
        print("Failed to parse:", e)
        tests, test_plan = {}, {}


    report = {"summary": "stubbed", "passed": True, "coverage": 0.0, "notes": "Replace with real runner"}
    return {**state, "tests": tests, "test_plan": test_plan, "test_report": report}


if __name__ == "__main__":
    # simulate state coming out of implementation_node
    sample_state = {
        "spec": {
            "project_name": "Task Manager",
            "description": "A simple task management app",
            "features": ["add task", "list tasks", "mark task done"],
            "constraints": {"tech_stack": "Python + FastAPI"}
        },
        "code_changes": {
            "api/tasks.py": """\"\"\"Tasks API\"\"\"
            from fastapi import APIRouter

            router = APIRouter()

            @router.get("/tasks")
            def list_tasks():
                return []  # TODO: implement
        """
        }
    }

    result = testing_node(sample_state)

    print("\n=== Generated Test Plan ===")
    print(result.get("test_plan", {}))

    print("\n=== Generated Tests ===")
    for filename, content in result.get("tests", {}).items():
        print(f"\n--- {filename} ---\n{content[:300]}...\n")  

    print("\n=== Test Report (stubbed) ===")
    print(result.get("test_report"))