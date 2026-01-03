from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from agent_observatory import Observatory
from agent_observatory.exporters.otel import OpenTelemetryExporter


def configure_otel() -> None:
    """
    Configure OpenTelemetry ONCE per process.
    """
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": "livekit-agent",
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


def create_observatory() -> Observatory:
    tracer = trace.get_tracer("livekit-agent")
    exporter = OpenTelemetryExporter(tracer)

    # Inline mode is correct for agent lifecycles
    return Observatory(exporter=exporter, inline=True)
