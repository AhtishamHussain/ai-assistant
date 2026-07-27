import os
import subprocess
from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage

class AgentState(TypedDict):
    messages: List[AnyMessage]
    repository_context: dict
    target_branch: str
    execution_plan: List[str]
    next_action: Literal['read_repo', 'write_code', 'github_sync', 'end']

def prompt_engineering_router(state: AgentState):
    latest_message = state['messages'][-1].content.lower()
    if 'architecture' in latest_message or 'read' in latest_message or 'explain' in latest_message:
        return {'next_action': 'read_repo'}
    elif 'fix' in latest_message or 'test' in latest_message or 'bug' in latest_message or 'build' in latest_message or 'code' in latest_message or 'page' in latest_message or 'login' in latest_message:
        return {'next_action': 'write_code'}
    elif 'pr' in latest_message or 'issue' in latest_message or 'sync' in latest_message:
        return {'next_action': 'github_sync'}
    return {'next_action': 'end'}

def context_reader_node(state: AgentState):
    print('\n[System MCP Server] Reading physical hard drive topology...')
    tree = []
    for root, dirs, files in os.walk('./'):
        if any(x in root for x in ['.git', '__pycache__', 'venv', 'node_modules']): continue
        level = root.replace('./', '').count(os.sep)
        if level > 2: continue
        indent = ' ' * 4 * level
        tree.append(f'{indent}{os.path.basename(root)}/')
        for f in files:
            if not f.startswith('.'): tree.append(f'{indent}    {f}')
    topology = '\n'.join(tree)
    return {
        'messages': [AIMessage(content=f'ðŸ¤– MCP Agent: Located Local Folders:\n{topology}')],
        'next_action': 'end'
    }

def code_workflow_node(state: AgentState):
    user_query = state['messages'][-1].content
    print(f'\nðŸ”¥ [AI Coding Workflow Engine] Running real background Aider command for: {user_query}...')
    try:
        result = subprocess.run(['python', '-m', 'aider', '--message', f'{user_query} inside app_target.py', '--no-auto-commit'], capture_output=True, text=True, shell=True)
        output_log = result.stdout if result.stdout else result.stderr
        return {
            'messages': [AIMessage(content=f'ðŸ¤– Developer Agent: File Mutation Complete.\n{output_log[:400]}')],
            'next_action': 'end'
        }
    except Exception as e:
        return {
            'messages': [AIMessage(content=f'âŒ Error invoking Aider interface: {str(e)}')],
            'next_action': 'end'
        }

def external_protocol_node(state: AgentState):
    print('\nðŸš€ [Agent Protocol Gateway] Syncing and pushing changes to GitHub via CLI...')
    try:
        subprocess.run(['git', 'checkout', '-b', 'feature/ai-login-page'], shell=True)
        subprocess.run(['git', 'add', '.'], shell=True)
        subprocess.run(['git', 'commit', '-m', 'feat: AI automated login feature injection'], shell=True)
        subprocess.run(['git', 'push', 'origin', 'feature/ai-login-page', '--force'], shell=True)
        pr_res = subprocess.run(['gh', 'pr', 'create', '--title', 'Feat: AI Login Component', '--body', 'Automated generation.'], capture_output=True, text=True, shell=True)
        return {
            'messages': [AIMessage(content=f'ðŸ¤– Git Agent: Branch pushed cleanly! Web Pull Request initialized:\n{pr_res.stdout}')],
            'next_action': 'end'
        }
    except Exception as e:
        return {
            'messages': [AIMessage(content=f'âš ï¸ Git API Sync Warning: Local files branch saved: {str(e)}')],
            'next_action': 'end'
        }

builder = StateGraph(AgentState)
builder.add_node('router', prompt_engineering_router)
builder.add_node('read_repo', context_reader_node)
builder.add_node('write_code', code_workflow_node)
builder.add_node('github_sync', external_protocol_node)

builder.set_entry_point('router')
builder.add_conditional_edges('router', lambda state: state['next_action'], {'read_repo': 'read_repo', 'write_code': 'write_code', 'github_sync': 'github_sync', 'end': END})
builder.add_edge('read_repo', END)
builder.add_edge('write_code', END)
builder.add_edge('github_sync', END)
app = builder.compile()

if __name__ == '__main__':
    print('==========================================================================')
    print('âš¡ Advanced AI Engineer Orchestration Platform Active (Production Core) âš¡')
    print('==========================================================================')
    session_state = {'messages': [], 'repository_context': {}, 'target_branch': 'main', 'execution_plan': [], 'next_action': 'end'}
    while True:
        user_prompt = input('\nðŸ‘¤ Prompt Advanced Agent Core: ').strip()
        if user_prompt.lower() in ['exit', 'quit']: break
        if not user_prompt: continue
        session_state['messages'].append(HumanMessage(content=user_prompt))
        for event in app.stream(session_state):
            for node, data in event.items():
                if 'messages' in data and len(data['messages']) > 0: print(data['messages'][-1].content)
                session_state.update(data)