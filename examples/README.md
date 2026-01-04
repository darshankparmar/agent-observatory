# Agent Observatory Examples

This directory contains **small, focused examples** demonstrating how to use
Agent Observatory in different execution models and environments.

Each example is intentionally minimal and highlights **one core concept at a time**.

---

## Example Overview

### `basic/`
Minimal inline usage.

- inline execution mode
- single agent session
- basic spans

**Start here** if you’re new to Agent Observatory.

---

### `streaming/`
Streaming-first observability.

- stream spans
- high-frequency events
- ordered event emission

Use this for token streams, audio, or real-time agent output.

---

### `opentelemetry/`
OpenTelemetry integration.

- external OTEL configuration
- OpenTelemetryExporter usage
- zero global state ownership

Recommended for production observability stacks.

---

### `livekit/`
Real-world LiveKit agent example.

- long-running server
- agent lifecycle instrumentation
- metrics as structured events
- realistic production setup

This is the most advanced example.

---

## Running Examples

All examples assume:

- Python >= 3.10
- Agent Observatory installed
- Optional dependencies installed where required (e.g. OpenTelemetry, LiveKit)

Inline examples can be run directly:

```bash
uv run <example>.py
