import logging
from dotenv import load_dotenv

from livekit.agents import (
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    metrics,
    room_io,
)
from livekit.plugins import cartesia, deepgram, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from agent_observatory import AgentContext
from observability import configure_otel, create_observatory
from agent import MyAgent

logger = logging.getLogger("server")

load_dotenv()

# -----------------------------------------------------------------------------
# LiveKit setup
# -----------------------------------------------------------------------------

server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    """
    One LiveKit RTC session == one Agent Observatory session
    """
    observatory = create_observatory()

    room_sid = str(ctx.room.sid)

    agent_ctx = AgentContext(
        session_id=room_sid,
        agent_id="livekit-agent",
        metadata={
            "room": ctx.room.name,
            "job_id": ctx.job.id,
        },
    )

    with observatory.start_session(agent_ctx) as obs_session:
        logger.info("Agent session started")

        session: AgentSession = AgentSession(
            stt=deepgram.STT(),
            llm="openai/gpt-4.1-mini",
            tts=cartesia.TTS(),
            turn_detection=MultilingualModel(),
            vad=ctx.proc.userdata["vad"],
            preemptive_generation=True,
            resume_false_interruption=True,
            false_interruption_timeout=1.0,
        )

        usage_collector = metrics.UsageCollector()

        @session.on("metrics_collected")
        def _on_metrics_collected(ev):
            usage_collector.collect(ev.metrics)

            # attach as a structured event
            with obs_session.span("metrics.snapshot", kind="agent_step") as span:
                span.emit_event(
                    "metrics.collected",
                    ev.metrics,
                )

        async def log_usage():
            summary = usage_collector.get_summary()
            logger.info("Usage summary: %s", summary)

        ctx.add_shutdown_callback(log_usage)

        await session.start(
            agent=MyAgent(obs_session),
            room=ctx.room,
            room_options=room_io.RoomOptions(
                audio_input=room_io.AudioInputOptions(),
            ),
        )

        logger.info("Agent session ended")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    configure_otel()
    cli.run_app(server)
