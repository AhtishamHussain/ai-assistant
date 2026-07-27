import os
import subprocess
from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage

# ==========================================
# 1. DEFINE STATE & LOCAL CONFIGURATION
# ==========================================
class AssistantState(TypedDict):
    messages: List[AnyMessage]
    repo_path: str
    documentation: List[str]
    test_results: str
    next_step: str

# 💻 Connects to your local machine running Ollama offline (No API key needed!)
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

# ==========================================
# 2. DEFINE SYSTEM TOOLS
# ==========================================
@tool
def read_repo_structure(repo_path: str) -> str:
    """Recursively lists repository directory tree up to 3 levels deep."""
    tree = []
    for root, dirs, files in os.walk(repo_path):
        if any(ignored in root for ignored in [".git", "__pycache__", "venv", "node_modules"]):
            continue
        level = root.replace(repo_path, '').count(os.sep)
        if level > 2: continue
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            if not f.startswith('.'):
                tree.append(f"{indent}    {f}")
    return "\n".join(tree)

@tool
def run_tests(repo_path: str) -> str:
    """Runs pytest inside the repository directory and returns output."""
    result = subprocess.run(["pytest"], cwd=repo_path, capture_output=True, text=True)
    return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

# ==========================================
# 3. DEFINE AGENT NODES
# ==========================================
def supervisor_node(state: AssistantState):
    """Central router analyzing user instructions to choose the next node."""
    user_intent = state["messages"][-1].content.lower()
    
    if "explain" in user_intent or "architecture" in user_intent:
        return {"next_step": "architect"}
    elif "fix" in user_intent or "test" in user_intent:
        return {"next_step": "engineer"}
    return {"next_step": "end"}

def architect_node(state: AssistantState):
    """Analyzes the project topology and answers architecture questions."""
    structure = read_repo_structure.invoke({"repo_path": state["repo_path"]})
    prompt = f"Analyze this workspace mapping and explain its core layout architectural design pattern:\n{structure}"
    response = llm.invoke(prompt)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "documentation": [response.content]
    }

def engineer_node(state: AssistantState):
    """Executes existing tests and handles testing validation feedback loops."""
    test_output = run_tests.invoke({"repo_path": state["repo_path"]})
    summary = "Tests passed successfully!" if "failed" not in test_output.lower() else "Test failures detected."
    
    return {
        "messages": [AIMessage(content=f"QA Scan Complete: {summary}")],
        "test_results": test_output
    }

# ==========================================
# 4. BUILD THE GRAPH FLOW
# ==========================================
workflow = StateGraph(AssistantState)

# Add processing nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("architect", architect_node)
workflow.add_node("engineer", engineer_node)

# Establish execution edges
workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda state: state["next_step"],
    {
        "architect": "architect",
        "engineer": "engineer",
        "end": END
    }
)

# Return loops back to supervisor for clean exit routing
workflow.add_edge("architect", "supervisor")
workflow.add_edge("engineer", "supervisor")

app = workflow.compile()

# ==========================================
# 5. INTERACTIVE TERMINAL LOOP
# ==========================================
if __name__ == "__main__":
    print("🤖 AI Coding Assistant Engine Initialized (Local Mode)...")
    print("💡 Type 'explain architecture' or 'run tests' to prompt the graph.")
    print("❌ Type 'exit' or 'quit' to stop.")
    print("-" * 50)
    
    # Maintain global workspace memory across your conversation session
    session_state = {
        "messages": [],
        "repo_path": "./",  
        "documentation": [],
        "test_results": "",
        "next_step": ""
    }
    
    while True:
        user_query = input("\n👤 You: ").strip()
        
        # Check for escape triggers
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Shutting down agent engine. Goodbye!")
            break
            
        if not user_query:
            continue
            
        # Append the new user prompt into the session message memory
        session_state["messages"].append(HumanMessage(content=user_query))
        
        # Execute the LangGraph streaming engine
        for event in app.stream(session_state, config={"configurable": {"thread_id": "interactive_session"}}):
            for node, data in event.items():
                print(f"\n--- Node Executed: {node} ---")
                
                # Print conversational responses as they finish executing
                if "messages" in data and len(data["messages"]) > 0:
                    print(data["messages"][-1].content)
                
                # Merge current execution delta back into long term graph state memory
                session_state.update(data)
