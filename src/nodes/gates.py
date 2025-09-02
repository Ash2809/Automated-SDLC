from ..hitl import hitl_provider
from ..data_models import OrchestratorState
from typing import List

def hitl_gate(state: OrchestratorState, gate: str, payload_keys: List[str]) -> OrchestratorState:
    payload = {k: state.get(k) for k in payload_keys}
    decision = hitl_provider.request(gate, payload)
    approvals = state.get("approvals", {})
    approvals[gate] = {k: v for k, v in decision.items() if k != "payload"}
    updated = {**state, **(decision.get("payload") or {})}
    updated["approvals"] = approvals
    if not decision.get("approved", True):
        raise Exception(f"Gate {gate} rejected: {decision.get('notes', 'No reason provided')}")
    return updated
