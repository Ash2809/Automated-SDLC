# api.py
import sys, os, time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

sys.path.append(os.path.dirname(__file__))

from src.workflow import build_graph
from src.data_models import OrchestratorState

app = FastAPI(
    title="Automated SDLC API",
    version="0.1",
    description="Accepts a project spec JSON, executes the SDLC workflow, and returns the final state"
)


# ---- Request model ----
class WorkflowRequest(BaseModel):
    spec: Dict[str, Any]   # matches the shape of your example_input()


@app.get("/")
def root():
    return {"status": "ok", "message": "Automated SDLC API is running"}


@app.post("/run_workflow")
def run_workflow(req: WorkflowRequest):
    """
    Execute the full SDLC workflow for the provided project spec.
    """
    try:
        workflow = build_graph()
        init: OrchestratorState = {
            "spec": req.spec,
            "approvals": {},
            "repo_url": None,
            "run_id": str(int(time.time())),
        }

        final_state = workflow.invoke(init)
        return {"final_state": final_state}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
