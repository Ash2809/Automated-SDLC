from langgraph.graph import StateGraph, END
from .data_models import OrchestratorState
from .nodes.requirements import requirements_node
from .nodes.design import design_node
from .nodes.planning import planning_node
from .nodes.implementation import implementation_node
from .nodes.testing import testing_node
from .nodes.deployment import deployment_node
from .nodes.gates import hitl_gate

def build_graph():
    graph = StateGraph(OrchestratorState)
    graph.add_node("requirements_node", requirements_node)
    graph.add_node("design_node", design_node)
    graph.add_node("planning_node", planning_node)
    graph.add_node("implementation_node", implementation_node)
    graph.add_node("testing_node", testing_node)
    graph.add_node("deployment_node", deployment_node)

    # HITL gates
    graph.add_node("hitl_requirements_node", lambda s: hitl_gate(s, "requirements_review", ["user_stories"]))
    graph.add_node("hitl_design_node",      lambda s: hitl_gate(s, "architecture_review", ["architecture"]))
    graph.add_node("hitl_preprod_node",     lambda s: hitl_gate(s, "preprod_release", ["test_report", "ci_cd"]))
    graph.add_node("hitl_prod_node",        lambda s: hitl_gate(s, "prod_release", ["deployment"]))

    # Edges
    graph.set_entry_point("requirements_node")
    graph.add_edge("requirements_node", "hitl_requirements_node")
    graph.add_edge("hitl_requirements_node", "design_node")
    graph.add_edge("design_node", "hitl_design_node")
    graph.add_edge("hitl_design_node", "planning_node")
    graph.add_edge("planning_node", "implementation_node")
    graph.add_edge("implementation_node", "testing_node")
    graph.add_edge("testing_node", "hitl_preprod_node")
    graph.add_edge("hitl_preprod_node", "deployment_node")
    graph.add_edge("deployment_node", "hitl_prod_node")
    graph.add_edge("hitl_prod_node", END)

    return graph.compile()

if __name__ == "__main__":
    graph = build_graph()
    print("Graph built successfully with nodes:", list(graph.nodes.keys()))