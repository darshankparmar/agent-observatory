import asyncio
import random

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from agent_observatory import Observatory, AgentContext
from agent_observatory.exporters.otel import OpenTelemetryExporter


# ---------------------------------------------------------
# 1. Configure OpenTelemetry (once, at process start)
# ---------------------------------------------------------
def configure_otel():
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": "agent-observatory-demo",
                "service.version": "0.1.0",
            }
        )
    )

    provider.add_span_processor(
        SimpleSpanProcessor(
            OTLPSpanExporter(
                endpoint="http://127.0.0.1:4317",
                insecure=True,
            )
        )
    )

    trace.set_tracer_provider(provider)


# ---------------------------------------------------------
# 2. Simulated agent workflow
# ---------------------------------------------------------
async def run_agent(obs: Observatory):
    ctx = AgentContext(
        session_id="session_001",
        agent_id="demo-agent",
        metadata={"env": "local"},
    )

    # Root span for the entire agent run
    tracer = trace.get_tracer("agent-demo")

    with tracer.start_as_current_span("agent.run") as root:
        root.set_attribute("agent.id", ctx.agent_id)
        root.set_attribute("session.id", ctx.session_id)

        with obs.start_session(ctx) as session:
            # ---- Planning step
            with session.span("plan", kind="agent_step") as span:
                span.emit_event("planning.started")
                await asyncio.sleep(0.1)
                span.emit_event("planning.completed")

            # ---- Streaming output (tokens / audio / chunks)
            with session.stream("response_stream") as stream:
                for i in range(5):
                    stream.emit_event(
                        "chunk",
                        {
                            "index": i,
                            "text": f"token-{i}",
                        },
                    )
                    await asyncio.sleep(0.05)

            # ---- Final step with possible error
            try:
                with session.span("finalize", kind="agent_step"):
                    if random.random() < 0.3:
                        raise RuntimeError("model timeout")
                    await asyncio.sleep(0.05)
            except Exception as e:
                root.record_exception(e)
                root.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))


# ---------------------------------------------------------
# 3. Entrypoint
# ---------------------------------------------------------
async def main():
    configure_otel()

    tracer = trace.get_tracer("agent-demo")
    exporter = OpenTelemetryExporter(tracer)

    # Inline mode = simple & deterministic (great for examples)
    obs = Observatory(exporter=exporter, inline=True)

    await run_agent(obs)

    await obs.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
