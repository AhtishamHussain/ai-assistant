from langgraph.graph import StateGraph, END
from src.state import AssistantState
from src.nodes import supervisor_node, architect_node, engineer_node
from langchain_core.messages import HumanMessage

workflow = StateGraph(AssistantState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("architect", architect_node)
workflow.add_node("engineer", engineer_node)

workflow.set_entry_point("supervisor")
workflow.add_conditional_edges("supervisor", lambda state: state["next_step"], {"architect": "architect", "engineer": "engineer", "end": END})
workflow.add_edge("architect", "supervisor")
workflow.add_edge("engineer", "supervisor")

app = workflow.compile()

# ⚠️ DOUBLE CHECK THIS SPELLING: Must be exactly double underscores
if __name__ == "__main__":
    print("🚀 Enterprise Multi-Agent Graph Engine Active...")
    inputs = {
        "messages": [HumanMessage(content="Run our system bug test and patch failures")],
        "repo_path": "./",
        "target_file": "app_target.py",
        "issue_title": "Fix Broken App Logic Pipeline",
        "issue_body": "",
        "test_results": "",
        "next_step": ""
    }
    for event in app.stream(inputs):
        print(event)
