from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.pydantic_v1 import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
import os
import json
import time
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional, Literal, TypedDict
from dataclasses import dataclass, asdict

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    api_key=GOOGLE_API_KEY,
    temperature=0.1)


class Gemini:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=GOOGLE_API_KEY,
            temperature=0.1
        )

    def complete(self, system: str, user: str, **kwargs) -> str:
        messages = []
        if system.strip():
            messages.append({"role": "system", "content": system.strip()})
        messages.append({"role": "user", "content": user.strip()})

        resp = self.model.invoke(messages)
        return resp.content if hasattr(resp, "content") else str(resp)
    
@dataclass
class Constraint:
    tech_stack : Optional[str] = None
    deployment : Optional[str]= None
    priority : Optional[Literal["high", "medium", "low"]] = None 

@dataclass
class ProjectSpec:
    project_name : str
    description : str
    features : List[str]
    constraints : Constraint

LLM = Gemini()

class OrchestratorState(TypedDict, total = False):
    spec = Dict[str, Any]

    #Artifacts 
    user_stories: List[Dict[str, Any]]
    architecture : Dict[str, Any]
    plan : List[Dict[str, Any]]
    code_changes : Dict[str, str]
    tests : Dict[str, str]
    test_report : Dict[str, str]
    ci_cd : Dict[str, str]
    deployment : Dict[str, str]

    #these are for logging each nde in langgraph
    approvals : Dict[str, Any]
    repo_url : Optional[str]
    run_id : Optional[str]

def normalize_spec(raw : Dict[str, Any]) -> ProjectSpec:
    constraints = raw.get("constraints") or {}
    return ProjectSpec(
        project_name = raw.get("project_name", "Untitled Project"),
        description = raw.get("description", ""),
        features = raw.get("features", []),
        constraints= Constraint(
            tech_stack = constraints.get("tech_stack"),
            deployment = constraints.get("deployment"),
            priority = constraints.get("priority")
        ),
    )
import re
def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {}
    return {}

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