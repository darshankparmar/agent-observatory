# Agent Observatory Examples

This directory contains examples demonstrating how Agent Observatory is embedded at different layers of an agent system, from minimal scripts to full runtime integrations.

Some examples are intentionally minimal, while others act as **reference embeddings** for framework and runtime authors.

## Example Overview

### `real_time_agent_runtime/` (Reference Integration)

A **production-shaped reference embedding** showing how an agent runtime owns session lifecycle, instruments long-running execution and observes high-frequency streams without affecting agent behavior.

This example demonstrates:

- runtime-owned session lifecycle
- explicit agent semantics (agent steps, tool calls, LLM calls)
- streaming-first observability under load
- exporter neutrality
- fail-open guarantees in practice

**Framework and platform authors should start here.**

### `basic/`

Minimal usage of spans and exporters.

- [`basic_tracing.py`](basic/basic_tracing.py): Sync scripting mode.
- [`realtime_debug.py`](basic/realtime_debug.py): **New** Live pretty-print feedback.
- [`file_logging.py`](basic/file_logging.py): **New** JSONL logging for the `obs-view` CLI.

**Start here** if you're new to Agent Observatory and want a quick, minimal overview.

### `streaming/`
Streaming-first observability.

- stream spans
- high-frequency events
- ordered event emission

Use this for token streams, audio or real-time agent output.

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
