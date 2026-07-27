from typing import List, TypedDict
from langchain_core.messages import AnyMessage

class AssistantState(TypedDict):
    messages: List[AnyMessage]
    repo_path: str
    target_file: str
    issue_title: str
    issue_body: str
    test_results: str
    next_step: str
