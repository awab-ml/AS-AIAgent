# Architecting Secure AI Agents Prototype

This project is a functional prototype of the system-level defense architecture described in the research paper *"Architecting Secure AI Agents: Perspectives on System-Level Defenses Against Indirect Prompt Injection Attacks" (Zagieboylo et al.)*.

## Architecture Overwiew

The system implements a secure agent loop divided into 5 phases:
1. **Orchestrate**: An LLM agent drafts a `Plan` and calculates the minimum necessary `Policy` required to execute it.
2. **Approve**: An LLM Judge reviews the structured proposed changes. If risky, it escalates to a Human-in-the-Loop (HITL) check.
3. **Execute**: The agent must explicitly *verbalize* the specific instructions it intends to follow and where it thinks they came from, before proposing a specific action (Proposal 1).
4. **Enforce**: A policy engine checks the proposed action against the dynamic policy. It automatically intercepts execution if the verbalized instructions trace back to untrusted environment inputs (e.g., prompt injections).
5. **Environment**: The isolated execution of the tool, returning feedback to the loop.

## Setup

1. Copy `.env.example` to `.env` and fill in your OpenAI API Key.
   ```bash
   cp .env.example .env
   ```
2. Make sure dependencies are installed:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Demo

Execute the agent loop:
```bash
python run.py
```

The default scenario tasks the agent to read emails and process urgent payments. Email #2 contains an embedded indirect prompt injection. The system-level defenses (Approver & Enforcer) should automatically catch and halt the attack.
