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

if __name__ == "__main__":
    print("==========================================================================")
    print("?? Professional Multi-Agent Graph Shell Active (Local Inference Node)")
    print("?? Available Commands: 'explain architecture', 'fix bugs', or type 'exit'")
    print("==========================================================================")
    
    session_state = {
        "messages": [],
        "repo_path": "./",
        "target_file": "app_target.py",
        "issue_title": "Automated Code Evolution Session",
        "issue_body": "",
        "test_results": "",
        "next_step": ""
    }
    
    while True:
        user_prompt = input("\n?? Enter Prompt for AI Agent: ").strip()
        
        if user_prompt.lower() in ["exit", "quit"]:
            print("?? Shutting down agent terminal interface. Goodbye!")
            break
            
        if not user_prompt:
            continue
            
        session_state["messages"].append(HumanMessage(content=user_prompt))
        
        print("?? Executing autonomous workflow graph routing...")
        for event in app.stream(session_state):
            for node, data in event.items():
                print(f"\n--- Node Processed: {node} ---")
                if "messages" in data and len(data["messages"]) > 0:
                    print(data["messages"][-1].content)
                session_state.update(data)
