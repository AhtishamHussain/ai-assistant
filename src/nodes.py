from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from src.state import AssistantState
from src.tools import read_repo_structure, execute_system_tests, write_file_patch, create_github_issue_and_pr

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)


def supervisor_node(state: AssistantState):
    intent = state["messages"][-1].content.lower()
    if "explain" in intent or "architecture" in intent:
        return {"next_step": "architect"}
    elif "fix" in intent or "bug" in intent or "test" in intent:
        return {"next_step": "engineer"}
    return {"next_step": "end"}


def architect_node(state: AssistantState):
    structure = read_repo_structure.invoke({"repo_path": state["repo_path"]})
    prompt = f"Analyze this architecture and explain layout patterns:\n{structure}"
    response = llm.invoke(prompt)
    return {
        "messages": [AIMessage(content=response.content)],
        "documentation": [response.content],
        "next_step": "supervisor"
    }


def engineer_node(state: AssistantState):
    test_logs = execute_system_tests.invoke({"repo_path": state["repo_path"]})

    if "failed" in test_logs.lower() or "error" in test_logs.lower():
        fix_prompt = f"Fix this broken code based on test data:\n{test_logs}"
        corrected_code = llm.invoke(fix_prompt).content

        write_file_patch.invoke({"file_path": state["target_file"], "source_code": corrected_code})

        create_github_issue_and_pr.invoke({
            "repo_path": state["repo_path"],
            "branch": "fix/ai-patch-automation",
            "title": state.get("issue_title", "Automated Bug Repair Session"),
            "body": f"AI identified failure logs:\n{test_logs}"
        })
        return {"messages": [AIMessage(
            content="❌ Faults intercepted. Applied local repair files and triggered GitHub branch PR creation.")],
                "next_step": "supervisor"}

    return {"messages": [AIMessage(content="✅ Code validation targets verified. 0 defects recorded.")],
            "next_step": "supervisor"}
