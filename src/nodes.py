from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from src.state import AssistantState
from src.tools import read_repo_structure, execute_system_tests, write_file_patch, create_github_issue_and_pr

# Initialize local LLM
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

def supervisor_node(state: AssistantState):
    \"\"\"Uses the LLM model to intelligently analyze intent and route tasks.\"\"\"
    user_intent = state["messages"][-1].content
    
    routing_prompt = (
        "You are an AI Software Team Supervisor Router.\n"
        "Analyze this user instruction and decide which specialized agent node should run next.\n"
        f"User Instruction: '{user_intent}'\n\n"
        "Your choices are exactly one of these lowercase strings:\n"
        "- 'architect' (If they want to analyze layout structures, folders, configs, or explain architecture)\n"
        "- 'engineer' (If they want to fix bugs, test code, build pages, write functions, or create scripts)\n"
        "- 'end' (If they want to exit, or if the task is complete)\n\n"
        "Reply with ONLY the literal string name of the node. Do not write explanations or markdown blocks."
    )
    
    decision = llm.invoke(routing_prompt).content.strip().lower()
    
    if "architect" in decision:
        return {"next_step": "architect"}
    elif "engineer" in decision or "fix" in decision or "build" in decision:
        return {"next_step": "engineer"}
    else:
        return {"next_step": "end"}

def architect_node(state: AssistantState):
    \"\"\"Maps project topology layouts and returns analysis.\"\"\"
    structure = read_repo_structure.invoke({"repo_path": state["repo_path"]})
    prompt = f"Analyze this workspace mapping configuration map layout and explain its core architectural design patterns:\n{structure}"
    response = llm.invoke(prompt)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "documentation": [response.content],
        "next_step": "supervisor"
    }

def engineer_node(state: AssistantState):
    \"\"\"Scans for software breakage anomalies and runs file update operations.\"\"\"
    test_logs = execute_system_tests.invoke({"repo_path": state["repo_path"]})
    
    if "failed" in test_logs.lower() or "error" in test_logs.lower() or "not found" in test_logs.lower():
        fix_prompt = f"Write the full missing source code logic to completely satisfy this system test environment data:\n{test_logs}"
        corrected_code = llm.invoke(fix_prompt).content
        
        write_file_patch.invoke({"file_path": state["target_file"], "source_code": corrected_code})
        
        create_github_issue_and_pr.invoke({
            "repo_path": state["repo_path"],
            "branch": "fix/ai-patch-automation",
            "title": state.get("issue_title", "Automated Feature Evolution Session"),
            "body": f"AI identified failure trace elements:\n{test_logs}"
        })
        
        return {
            "messages": [AIMessage(content="?? Action Update: Intercepted broken layout environments. Applied physical code fixes to storage tracks and pushed pull request to remote server.")],
            "next_step": "supervisor"
        }
        
    return {
        "messages": [AIMessage(content="? System Status: Existing project testing routines passed with 0 errors.")],
        "next_step": "supervisor"
    }
