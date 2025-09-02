from src.llm import LLM
from src.utils import to_json, extract_json
from src.data_models import ProjectSpec, OrchestratorState, Constraint
from src.utils import normalize_spec
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import asdict
import json

def deployment_node(state: OrchestratorState) -> OrchestratorState:
    spec = normalize_spec(state["spec"])  

    prompt_sys = (
        "You are a DevOps engineer. Produce CI/CD config and containerization files. "
        "Return valid JSON only, no markdown code fences, no explanations."
    )

    prompt_user = (
        f"Deployment: {getattr(spec.constraints, 'deployment', 'unspecified')}\n"
        "Output JSON with:\n"
        "  - 'ci_cd': {filename: content}, where content is plain text (no markdown fences)\n"
        "  - 'deployment': {strategy, envs}"
    )

    text = LLM.complete(prompt_sys, prompt_user)
    print("LLM raw response (truncated):", text[:500])

    try:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(json)?", "", cleaned, flags=re.IGNORECASE).strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        data = json.loads(cleaned)
        ci_cd = data.get("ci_cd", {})
        deployment = data.get("deployment", {})
    except Exception as e:
        print("Failed to parse deployment JSON:", e)
        ci_cd, deployment = {}, {}

    return {**state, "ci_cd": ci_cd, "deployment": deployment}

if __name__ == "__main__":
    sample_state = {
        "spec": {
            "project_name": "Task Manager",
            "description": "A simple task management app",
            "features": ["add task", "list tasks", "mark task done"],
            "constraints": {
                "tech_stack": "Python + FastAPI",
                "deployment": "Docker + GitHub Actions"
            }
        }
    }

    result = deployment_node(sample_state)

    print("=== Generated CI/CD Configs ===")
    for filename, content in result.get("ci_cd", {}).items():
        print(f"\n--- {filename} ---\n{content[:300]}...\n")  # preview first 300 chars

    print("=== Deployment Strategy ===")
    print(result.get("deployment", {}))
