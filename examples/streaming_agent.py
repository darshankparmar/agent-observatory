from agent_observatory import Observatory, AgentContext
from agent_observatory.exporters.json import JSONExporter


def run_streaming_agent():
    obs = Observatory(
        exporter=JSONExporter(),
        inline=True,  # inline for demo; async worker in prod
    )

    ctx = AgentContext(
        session_id="streaming-session-1",
        agent_id="streaming-agent",
    )

    with obs.start_session(ctx) as session:
        with session.stream(
            "audio_stream",
            attributes={
                "codec": "opus",
                "sample_rate": 48000,
            },
        ) as stream:
            for i in range(1000):
                stream.emit_event(
                    "audio.chunk",
                    {
                        "seq": i,
                        "bytes": 4096,
                        "duration_ms": 20,
                    },
                )


if __name__ == "__main__":
    run_streaming_agent()
