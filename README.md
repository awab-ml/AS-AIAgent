# Architecting Secure AI Agents: System-Level Defense Prototype

<p align="center">
  <img src="assets/logo.png" alt="AS-AIAgent " width="300"/>
</p>

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Prototype-yellow)

This project is a functional, offline prototype implementing the **system-level defense architecture** for AI agents, as proposed in the research paper: *"Architecting Secure AI Agents: Perspectives on System-Level Defenses Against Indirect Prompt Injection Attacks" (Zagieboylo et al.)*. 

Unlike traditional agent loops that treat the LLM as a black box and rely strictly on model-level prompt robustness, this architecture breaks the agent execution cycle into distinct, bounded operations that validate data provenance and restrict dangerous actions at a system level.

---

## 🛡️ Core Defense Mechanics

This prototype enforces security through the following components (mapping directly to the paper's proposals):

1. **Orchestrator & Dynamic Policy** (`core/orchestrator.py`)
   Dynamically generates an execution `Plan` and calculates the *minimum necessary* `Policy` required to execute it (`Least Privilege`), adapting to runtime failures safely.
   
2. **Constrained Approver & HITL** (`core/approver.py`)
   Before a new Plan/Policy runs, a dedicated LLM judge reviews a structured diff of the changes. If it is high-risk, it falls back to a **Human-In-The-Loop (HITL)** terminal prompt for explicit authorization.

3. **Decoupled Instruction Verification** (`core/executor.py`)
   **Proposal 1 from the paper:** Before proposing any specific tool execution payload (like `send_money`), the LLM Executor is forced to explicitly *verbalize* the specific localized instructions it intends to follow and flag their origin (User Prompt vs. External Web/Email Data).

4. **Policy Enforcer** (`core/enforcer.py`)
   Intercepts intended execution strictly. If the Executor admits the instruction is sourced from an "untrusted" email or webpage (e.g., an indirect prompt injection), execution is aggressively completely blocked without triggering the environment. 

---

## 📂 Project Structure

```text
secure_agent/
 ├── core/
 │   ├── models.py            # Pydantic structured schemas (Plan, Policy, ExecutorOutput)
 │   ├── orchestrator.py      # Generates minimum Plan & Policy
 │   ├── approver.py          # Approves plan with bounded LLM/HITL fallbacks
 │   ├── executor.py          # Enforces instruction-following verbalization
 │   └── enforcer.py          # Analyzes provenance & blocks attacks
 ├── env/
 │   └── tools.py             # Mock environment containing an Indirect Prompt Injection email
 ├── llm/
 │   └── client.py            # Isolated LLM client wrapper (offline demo mocked interactions)
 ├── security/                # Future expansion: custom rule parsers
 └── hitl/                    # Future expansion: usable security learning
run.py                        # Default CLI Runner interacting with components
tests/
 └── test_agent.py            # Pytest test suite validating provenance constraints
```

---

## 🚀 Quickstart

This application is built offline utilizing mock implementations inside `secure_agent/llm/client.py` so you can verify the defense principles immediately without external API keys.

### 1. Installation

This project utilizes `uv` for lightning-fast Python dependency management.
```bash
# Clone the repository
git clone https://github.com/yourusername/secure-ai-agents.git
cd secure-ai-agents

# Activate your virtual environment and install dependencies
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Running the Agent Loop

Execute the CLI runner:
```bash
python run.py
```
**Demo Scenario Behavior:**
- The task is to "read emails and process urgent payments".
- **Turn 1:** Reads the inbox cleanly.
- **Turn 2:** Encounters Email #2 (a mock indirect prompt injection demanding an unauthorized $1000 transfer). The Executor reads the payload but marks its source as the *environment*.
- **Turn 3:** The `Enforcer` automatically intercepts the operation and blocks it due to its untrusted provenance!

---

## 🧪 Running Tests

The repository includes a suite of automated functional tests utilizing Pytest that validates the strict properties of the `Enforcer` module against prompt injection payloads.

```bash
pytest tests/ -v
```

---

## 💡 Real LLM Support

This prototype has built-in support for real OpenAI models (default: `gpt-4o-mini`) leveraging native Pydantic structured outputs. This ensures model responses perfectly adhere to the strict `Plan`, `Policy`, and `Executor` constraints detailed in the defense architecture.

To use the real LLM instead of the offline mock:
1. Copy `.env.example` to `.env`: `cp .env.example .env`
2. Add your valid `OPENAI_API_KEY` to the `.env` file. 

**Offline Behavior:** The project seamlessly falls back to local mocked behaviors if you do not define an API key (or if you set `USE_MOCK_LLM=true`). This guarantees you can always run the `run.py` demonstration or complete `pytest` validation without external dependencies.

> *Note: This codebase is intended as a proof-of-concept for system-level security constraints and shouldn't be deployed to production systems without hardened validation/sandboxing infrastructure.*
