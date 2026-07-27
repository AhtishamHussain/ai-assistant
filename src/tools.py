import os
import subprocess
from langchain_core.tools import tool


@tool
def read_repo_structure(repo_path: str) -> str:
    """Scans and lists directory topologies up to 3 levels deep."""
    tree = []
    for root, dirs, files in os.walk(repo_path):
        if any(x in root for x in [".git", "__pycache__", "venv", "node_modules"]):
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
def execute_system_tests(repo_path: str) -> str:
    """Executes the local testing suite safely using subprocess."""
    try:
        result = subprocess.run(["pytest"], cwd=repo_path, capture_output=True, text=True, timeout=30)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except FileNotFoundError:
        return "ERROR: 'pytest' engine not found on the active system path."
    except subprocess.TimeoutExpired:
        return "ERROR: Testing suite execution timed out."


@tool
def write_file_patch(file_path: str, source_code: str) -> str:
    """Overwrites or updates code segments on the hard drive."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(source_code)
        return f"SUCCESS: File mutated at {file_path}."
    except Exception as e:
        return f"FAILURE: File modification error: {str(e)}"


@tool
def create_github_issue_and_pr(repo_path: str, branch: str, title: str, body: str) -> str:
    """Uses official GitHub CLI to publish issues and pull requests to cloud servers."""
    try:
        subprocess.run(["git", "checkout", "-b", branch], cwd=repo_path, check=True)
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", f"fix: AI automated patch for {title}"], cwd=repo_path, check=True)
        subprocess.run(["git", "push", "origin", branch], cwd=repo_path, check=True)

        subprocess.run(["gh", "issue", "create", "--title", title, "--body", body], cwd=repo_path, capture_output=True,
                       text=True)
        subprocess.run(["gh", "pr", "create", "--title", f"Fix: {title}", "--body", body], cwd=repo_path,
                       capture_output=True, text=True)

        return f"PROCESSED: GitHub Issue & Pull Request opened successfully."
    except subprocess.CalledProcessError as e:
        return f"GITHUB EXCEPTION: Failed git/gh operation: {str(e)}"
