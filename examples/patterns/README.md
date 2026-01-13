# Agent Observatory Patterns

This directory contains **focused implementation patterns** demonstrating individual observability techniques supported by Agent Observatory.

These examples are **not full runtimes** and are **not reference embeddings**. They isolate specific concepts for learning, experimentation or adaptation.

Framework authors should treat these as **building blocks**, not templates.

## Available Patterns

### `basic/`

Minimal, synchronous examples demonstrating core concepts:

- creating spans
- exporting traces
- inline execution mode
- console and file-based exporters

Use these to understand the absolute basics of Agent Observatory.

### `streaming/`

Streaming-first observability patterns:

- high-frequency event emission
- ordered stream events
- span-attached streaming output

Useful for token streams, audio chunks or real-time agent output.

### `multi_exporter/`

Demonstrates exporting the same session to **multiple exporters** simultaneously.

Shows how to:
- combine console, file and OTEL exporters
- swap exporters without changing agent logic

### `transports/`

Protocol-specific streaming patterns demonstrating how Agent Observatory fits into different transport layers.

Includes:

- `grpc_streaming/` – type-safe gRPC streaming
- `http_streaming/` – HTTP streaming / SSE
- `sse_streaming/` – browser-native Server-Sent Events

These examples focus on **transport mechanics**, not agent lifecycle design.

## How to Use These Patterns

- Read **after** the reference implementation
- Copy selectively into your own runtime
- Adapt semantics to your framework’s lifecycle
- Do not assume these represent full production setups

## What These Patterns Do Not Show

- runtime-owned session lifecycle
- framework-level embedding decisions
- production deployment guidance

For those, see:

```
examples/reference/real_time_agent_runtime/
```