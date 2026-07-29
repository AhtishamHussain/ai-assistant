import os

readme_content = """# 🚀 Enterprise Multi-Agent AI Coding Assistant

An autonomous, local software engineering agent pipeline built on a cyclical state-graph machine. It acts as an on-demand engineer inside your terminal, taking local workspace repositories as constraints to perform code analysis, file mutations, and Git automation entirely offline and for free.

---

## 🖥️ Terminal Interface Preview
When you initialize the application, it launches a persistent, interactive command-line interface dashboard:

```text
============================================================
🚀 ENTERPRISE MULTI-AGENT GRAPH SYSTEM RUNNING
📂 Linked Workspace Project: C:\\Users\\shami\\Bank_app
============================================================

✨ AVAILABLE AI CODER ASSISTANT CAPABILITIES & OPTIONS:
------------------------------------------------------------
 📖 Read Repo            -> Automatically scans active files
 💡 Explain Architecture  -> Breaks down codebase structures
 📦 Create Issues         -> Generates bug tracking alerts
 🛠️  Fix Bugs             -> Mutates and applies secure patches
 🧪 Write Tests          -> Generates regression unit tests
 🔀 Open Pull Request    -> Deploys a live branch & PR request
------------------------------------------------------------
💡 QUICK EXAMPLES TO TRY:
 • 'explain architecture layout'
 • 'fix bugs in transaction code'
 • 'write unit tests for bank system'
 • 'open pull request for latest patch'
------------------------------------------------------------
👉 Type your requirement below or type 'exit' to quit.

🤖 Ask AI Assistant > _
```

---

## 🏛️ System Core Architecture Matrix

| Component Name | What It Is | Engineering Justification (Why We Use It) |
| :--- | :--- | :--- |
| **LangGraph Framework (`StateGraph`)** | Cyclical graph routing framework | Standard scripts execute line-by-line and exit. LangGraph creates recursive worker loops to pass data back and forth until conditions are met. |
| **Multi-Agent Setup (Nodes & Edges)** | Split operational workflow roles | Separates operational concerns. The `supervisor_node` manages the lifecycle while the `engineer_node` runs core code operations. |
| **Local AI Engine (`ChatOllama`)** | Local open-source Llama3 brain | Keeps this system 100% free, private, and secure. Proprietary source code never leaves the host machine's physical disk space. |
| **Context Engine (`read_repository_code_files`)** | Recursive workspace scanner | Filters out repository noise (like `.git`, `venv`, `__pycache__`) so the AI only reads relevant code files within its token window. |
| **File Mutation Writer (`apply_code_patch`)** | Automated file-stream controller | Gives the assistant digital hands to overwrite outdated code files on your hard drive with clean patches autonomously. |
| **Memory Matrix (`TypedDict`)** | Strongly typed global memory state | Guarantees critical pipeline variables like `repo_path`, `task`, and `next_step` stay locked into safe slots without getting corrupted. |
| **System Subprocess Bridge** | Direct low-level shell executable hook | Connects Python to your system shell to trigger local binaries like `git` and `gh` (GitHub CLI) to manage deployment chains. |
| **Persistent Console Loop** | Continuous `while True` input shell | Connects a workspace directory once and keeps a live session open for endless development prompts without script restarts. |

---

## 🔄 End-to-End Workflow Execution Sequence

```text
 [Terminal Prompt Input] -> (argparse CLI captures path & prompt parameters)
        │
        ▼
 ┌──────────────┐
 │  Supervisor  │ ◄─── (Evaluates State: If "__end__" is flagged, terminates execution)
 └──────┬───────┘
        │ (Routes if tasks are outstanding)
        ▼
 ┌──────────────┐
 │ Conditional  │ ───► [Matches exact keywords inside user string input]
 └──────┬───────┘
        │
        ├─► "explain architecture" ──► (Scans tree layout -> triggers local LLM)
        ├─► "fix bugs" ────────────► (Rewrites target workspace application files)
        ├─► "write test" ──────────► (Generates automated unit test files)
        └─► "pull request" ────────► (Triggers Git automation subprocesses)
        │
        ▼
 ┌──────────────┐
 │   Engineer   │ ───► (Applies modifications -> updates next_step parameter state)
 └──────┬───────┘
        │
        ▼
 (Loops control flow loop safely back to Supervisor to cleanly terminate execution)
```

---

## 🛠️ Installation & Local Setup

### 1. Environment Activation
Clone this repository to your machine, open a PowerShell terminal inside the project root directory, and initialize your workspace:
```powershell
cd C:\\Users\\shami\\ai-assistant
.\\venv\\Scripts\\Activate.ps1
\$env:PYTHONPATH="src"
```

### 2. Verify Local Prerequisites
Ensure you have **Ollama** running locally with the Llama3 model pulled, and make sure your **GitHub CLI** tool is authorized:
```powershell
ollama run llama3
gh auth status
```

### 3. Launch the Interactive Assistant Engine
Target any repository directory dynamically from the command line using the `--repo` flag parameter string:
```powershell
python src/graph.py --repo "C:\\Users\\shami\\Bank_app"
```

---
*Note: Designed for enterprise localized workspace maintenance loops. Built with LangGraph, Python 3.14+, and Ollama.*
"""

# Ensure target workspace path directory exists safely on machine
os.makedirs("generated", exist_ok=True)
with open("generated/README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)
