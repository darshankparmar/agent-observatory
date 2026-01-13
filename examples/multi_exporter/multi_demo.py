"""
Multi-exporter demonstration.

Shows how to send traces to multiple destinations simultaneously:
- Console for immediate feedback
- File for persistence
- OpenTelemetry for production monitoring

Run with:
    uv run multi_demo.py
"""

from importlib.metadata import version
from typing import Any

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from agent_observatory import (
    AgentContext,
    ConsoleExporter,
    Exporter,
    FileExporter,
    Observatory,
    OpenTelemetryExporter,
    trace_agent_step,
    trace_tool_call,
)


def configure_otel() -> None:
    """
    Configure OpenTelemetry for the application.

    IMPORTANT:
    - Agent Observatory does NOT configure OpenTelemetry.
    - This must be done by the application.
    """
    SERVICE_VERSION = version("agent-observatory")

    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": "multi-exporter-demo",
                "service.version": SERVICE_VERSION,
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


def create_multi_exporter() -> list[Exporter]:
    """Create a multi-exporter with all available backends."""

    tracer = trace.get_tracer("multi-exporter-demo")
    otel_exporter = OpenTelemetryExporter(tracer)

    exporters: list[Exporter] = [
        ConsoleExporter(),
        FileExporter("logs/demo_traces.jsonl"),
        otel_exporter,
    ]

    return exporters


def failing_exporter() -> Any:
    """Create an exporter that always fails for error testing."""

    class FailingExporter:
        def export(self, payload: dict[str, Any]) -> None:
            raise RuntimeError("Simulated exporter failure")

    return FailingExporter()


@trace_agent_step("process_data")
def process_data(data: str) -> str:
    """Sample function with tool calls."""
    return transform_data(data)


@trace_tool_call("transform")
def transform_data(data: str) -> str:
    """Tool that transforms data."""
    return data.upper()


def main() -> None:
    """Run the multi-exporter demonstration."""
    configure_otel()

    # Create observatory with multiple exporters
    multi_exporter = create_multi_exporter()
    obs = Observatory(exporters=multi_exporter, inline=True)

    # Create context
    ctx = AgentContext(
        session_id="multi-demo-1",
        agent_id="demo-agent",
        user_id="developer",
    )

    print("Running agent with multiple exporters...")

    with obs.start_session(ctx) as session:
        with session.agent_step("main_workflow") as span:
            # Process some data
            result = process_data("hello world")

            with session.tool_call("validate_result"):
                if result == "HELLO WORLD":
                    span.event("validation_success", {"result": result})
                else:
                    span.event("validation_failed", {"result": result})

    # Demonstrate error isolation
    error_exporter: list[Exporter] = [
        ConsoleExporter(),
        failing_exporter(),  # This will fail
        FileExporter("logs/error_demo.jsonl"),
    ]

    obs_error = Observatory(exporters=error_exporter, inline=True)

    with obs_error.start_session(ctx) as session:
        with session.agent_step("error_test") as span:
            span.event("test_event", {"message": "Other exporters continue despite failure"})


if __name__ == "__main__":
    main()
