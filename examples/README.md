# Agent Observatory Examples

This directory contains **small, focused examples** demonstrating how to use
Agent Observatory in different execution models and environments.

Each example is intentionally minimal and highlights **one core concept at a time**.

## Example Overview

### `basic/`

Minimal usage of spans and exporters.

- [`basic_tracing.py`](basic/basic_tracing.py): Sync scripting mode.
- [`realtime_debug.py`](basic/realtime_debug.py): **New** Live pretty-print feedback.
- [`file_logging.py`](basic/file_logging.py): **New** JSONL logging for the `obs-view` CLI.

**Start here** if you're new to Agent Observatory.

### `streaming/`
Streaming-first observability.

- stream spans
- high-frequency events
- ordered event emission

Use this for token streams, audio, or real-time agent output.

### `transports/`
Real-time communication over different protocols.

- [`http_streaming/`](transports/http_streaming/): HTTP streaming with SSE
- [`grpc_streaming/`](transports/grpc_streaming/): Type-safe gRPC streaming
- [`sse_streaming/`](transports/sse_streaming/): Browser-native Server-Sent Events

Choose based on your infrastructure needs - all maintain full observability.

### `integrations/`
Third-party service integrations.

- [`opentelemetry/`](integrations/opentelemetry/): Production monitoring stacks
- [`livekit/`](integrations/livekit/): Real-time voice and video agents

### `multi_exporter/`
Simultaneous export to multiple backends.

- [`multi_demo.py`](multi_exporter/multi_demo.py): Console + file + OTEL

## Running Examples

All examples assume:

- Python >= 3.10
- Agent Observatory installed
- Optional dependencies installed where required (e.g. OpenTelemetry, LiveKit)

Inline examples can be run directly:

```bash
uv run <example>.py
```
