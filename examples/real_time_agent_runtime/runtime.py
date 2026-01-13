from agent import Agent
from exporters import build_exporter

from agent_observatory import Observatory


def main() -> None:
    # Runtime-level context (request id, room id, agent id, etc.)
    runtime_ctx = {
        "session_id": "runtime-session-001",
        "agent": "demo-agent",
        "runtime": "real_time_agent_runtime",
    }

    exporters = build_exporter()
    observatory = Observatory(exporters=exporters, inline=True)

    agent = Agent()

    # IMPORTANT:
    # The runtime owns the observability session.
    # The agent does NOT create or manage sessions.
    with observatory.start_session(runtime_ctx) as session:
        agent.run(session)


if __name__ == "__main__":
    main()
