import time, json
from pathlib import Path
from src.workflow import build_graph
from src.data_models import OrchestratorState

def example_input():
    return {
        "project_name": "Task Manager",
        "description": "A simple web app to track personal tasks and reminders",
        "features": ["User authentication", "Task CRUD", "Reminders", "Tags and filters"],
        "constraints": {"tech_stack": "React + FastAPI + Postgres", "deployment": "docker", "priority": "high"},
    }

def run_once():
    workflow = build_graph()
    init: OrchestratorState = {
        "spec": example_input(),
        "approvals": {},
        "repo_url": None,
        "run_id": str(int(time.time())),
    }

    print("Starting orchestrator…\n")
    for event in workflow.stream(init):
        for node, payload in event.items():
            if node != "__end__":
                print(f"\n>>> Node: {node}")
                print("State keys:", list(payload.keys()))

    final = workflow.invoke(init)
    print("\n\n=== FINAL STATE KEYS ===")
    print(list(final.keys()))

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    outfile = output_dir / f"final_state_{init['run_id']}.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print(f"Final state saved to {outfile}")

if __name__ == "__main__":
    run_once()
