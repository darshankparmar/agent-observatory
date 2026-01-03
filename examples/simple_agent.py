from agent_observatory import Observatory, AgentContext
from agent_observatory.exporters.json import JSONExporter


def run_agent():
    obs = Observatory(
        exporter=JSONExporter(),
        inline=True,  # deterministic execution for scripts
    )

    ctx = AgentContext(
        session_id="simple-session-1",
        agent_id="simple-agent",
        user_id=None,
        metadata={"env": "dev"},
    )

    with obs.start_session(ctx) as session:
        with session.span("plan", kind="agent_step"):
            # simulate planning work
            pass

        with session.span("execute", kind="agent_step"):
            # simulate execution work
            pass


if __name__ == "__main__":
    run_agent()
