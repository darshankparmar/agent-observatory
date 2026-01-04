"""
Basic Agent Observatory example.

Demonstrates:
- inline execution mode
- a single agent session
- basic span usage

Run with:
    uv run simple_agent.py
"""

from agent_observatory import AgentContext, Observatory
from agent_observatory.exporters.json import JSONExporter


def run_agent() -> None:
    # --- Observatory setup (inline mode) ---
    # Inline mode is synchronous and deterministic.
    # Ideal for scripts, tests and examples.
    obs = Observatory(
        exporter=JSONExporter(),
        inline=True,
    )

    # --- Agent context ---
    # Represents a single agent run.
    ctx = AgentContext(
        session_id="simple-session-1",
        agent_id="simple-agent",
        user_id="test-user",
        metadata={"env": "dev"},
    )

    # --- Agent session ---
    # Session automatically flushes on exit.
    with obs.start_session(ctx) as session:
        # --- Planning step ---
        with session.span("plan", kind="agent_step"):
            # simulate planning work
            pass

        # --- Execution step ---
        with session.span("execute", kind="agent_step"):
            # simulate execution work
            pass


if __name__ == "__main__":
    run_agent()
