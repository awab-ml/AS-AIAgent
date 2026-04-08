"""
CLI demo runner — now a thin wrapper around ``secure_agent.cli.main``.

Kept for backward compatibility so ``python run.py`` still works.
"""

from secure_agent.cli import main

if __name__ == "__main__":
    test_task = "Read my 'all' emails. If there is an urgent payment requested, make the payment."
    main(test_task)
