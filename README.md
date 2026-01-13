# Agent Observatory

[![PyPI version](https://img.shields.io/pypi/v/agent-observatory.svg)](https://pypi.org/project/agent-observatory/)
[![Python versions](https://img.shields.io/pypi/pyversions/agent-observatory.svg)](https://pypi.org/project/agent-observatory/)
[![License](https://img.shields.io/pypi/l/agent-observatory.svg)](LICENSE)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/darshankparmar/agent-observatory)

Agent Observatory is a **fail-open instrumentation layer** that lets you observe **long-running, streaming AI agents** without breaking execution, blocking streams or mutating global observability state.

It provides structured, streaming-safe tracing primitives for:

* agent steps and reasoning phases
* tool and function calls
* LLM interactions
* token / audio / event streams
* hierarchical, long-running agent execution

Agent Observatory is intentionally **infrastructure, not a platform**.
It defines *what* to observe, not *how* to store, visualize or monetize it.

## Who This Is For

Agent Observatory is primarily designed for:

* **framework authors** building agent runtimes
* **platform / infrastructure teams** supporting AI agents
* **real-time or streaming agent systems** (e.g. LiveKit)
* teams that already operate an observability stack (OTEL, Jaeger, Tempo, etc.)

It is **not** a turnkey observability product for end users.
Instead, it is meant to be embedded *inside* agent frameworks and systems.

## Why Agent Observatory Exists

Modern AI agents are fundamentally different from request/response services.

They are often:

* long-running
* stateful
* streaming
* hierarchical
* partially autonomous

Traditional tracing breaks down under these conditions.

Agent Observatory focuses on:

* **agent-aware semantics** → *clear visibility into agent reasoning and decisions*
* **streaming-first tracing** → *safe observation of token, audio and event streams*
* **minimal overhead** → *negligible impact on agent latency*
* **fail-open execution** → *observability never crashes agents*
* **clean integration with existing observability stacks** → *use your current OTEL backend*

Think of it as **“OpenTelemetry semantics for agents”**, designed to *complement*, not replace, OTEL.

## Core Concepts

### Sessions

A session guarantees that **all agent activity is captured or safely dropped**, but never partially exported or allowed to affect execution.

```python
with observatory.start_session(ctx) as session:  # ctx = agent / request / runtime context
    ...
```

A session:

* owns a trace ID
* buffers events in memory
* flushes automatically on exit
* never raises on failure (fail-open)

### Spans

Spans represent logical units of agent work.

```python
with session.span("plan", kind="agent_step"):
    ...
```

Common span kinds include:

* `agent_step`
* `tool_call`
* `llm_call`
* `stream`

Spans are nestable and tracked via context propagation.

### Streaming Events

Streaming is a first-class concern.

```python
with session.stream("audio_stream") as stream:
    stream.emit_event("chunk", {"seq": 1})
```
Streaming events are buffered and ordered in-memory, allowing high-frequency emission without backpressure or await points in agent code.

Streaming events:

* are associated with a span
* are safe for high-frequency emission
* preserve ordering
* map cleanly to OpenTelemetry span events

## Architecture Overview

```
┌──────────────┐
│ Agent Code   │
└─────┬────────┘
      │
      ▼
┌──────────────┐
│ AgentSession │
│ (buffering)  │
└─────┬────────┘
      │ trace envelope
      ▼
┌───────────────────────┐
│ Exporter Worker       │
│  inline | async       │
└─────┬─────────────────┘
      │
      ▼
┌────────────────────────┐
│ Exporters              │
│ JSON | OTEL | Custom   │
└────────────────────────┘
```

This architecture ensures observability is **downstream of agent execution**, never on the critical path.

## Runtime Integration Modes

Agent Observatory supports **two execution modes**.

### Inline Mode (Recommended for Scripts & Examples)

```python
obs = Observatory(exporter=exporter, inline=True)

with obs.start_session(ctx):
    ...
```

* synchronous
* deterministic
* exporter called immediately
* ideal for CLIs, tests, notebooks, short-lived agents

### Server Mode (Long-Running Agents)

```python
obs = Observatory(exporter)
await obs.start()

# handle many concurrent sessions

await obs.shutdown()
```

* background exporter worker
* buffered exporting
* backpressure handling
* designed for servers and agent hosts

Sessions may be created concurrently **after** `start()` is called.

⚠️ Server mode requires explicit shutdown to flush buffered sessions.

## Exporters

Exporters are intentionally simple: they receive a fully materialized session trace and must never influence agent behavior.

### Exporter Contract

All exporters must:

* be synchronous
* never raise
* fail open
* accept a full session envelope

```python
class Exporter:
    def export(self, payload: dict) -> None:
        ...
```

### Reference Exporters

Agent Observatory ships with **minimal reference exporters** to demonstrate integration patterns. They are not intended to be production observability solutions.

* JSON exporter (debugging, inspection)
* file-based logging
* OpenTelemetry integration
* simple console / debug exporters

These are intentionally lightweight and designed as **reference implementations**, not opinionated solutions.

> For concrete usage examples, see the `examples/` directory.

### Multiple Exporters

Agent Observatory supports exporting the same session to **multiple exporters**.

This is useful for:

* local debugging + production telemetry
* file capture + OTEL export
* experimentation without changing agent code

Refer to the `examples/multi_exporter/` directory for concrete patterns.

### Custom Exporters

Because exporters operate on a fully materialized session envelope, writing a custom exporter is straightforward.

Typical use cases include:

* sending traces to internal systems
* domain-specific aggregation
* bridging to non-OTEL backends

## Failure Semantics

Agent Observatory is **fail-open by design**.

* exporter failures never crash agents
* queue overflows drop traces (oldest first)
* internal errors are swallowed (optionally surfaced via debug logging)
* agent execution is never blocked

These behaviors are **contractual guarantees**. Breaking them is considered a bug.

## What Agent Observatory Is Not

* ❌ not a tracing backend
* ❌ not a UI
* ❌ not a metrics platform
* ❌ not a logging framework
* ❌ not opinionated about storage

It is a **semantic and runtime observability primitive**.

For explicit design boundaries, see [`docs/design/non-goals.md`](docs/design/non-goals.md).

## Installation

```bash
# Core (zero required dependencies)
uv pip install agent-observatory

# With OpenTelemetry exporter
uv pip install agent-observatory[otel]

# All extras (examples, dev tools)
uv pip install agent-observatory[all]
```

## Versioning & Stability

* `v0.x`: APIs may evolve
* core execution model is stable
* exporter contract is stable
* inline vs async semantics are stable

## Contributing

Contributions are welcome.

Please respect:

* synchronous exporter contract
* fail-open guarantees
* zero global side effects
* minimal dependencies

See `CONTRIBUTING.md`.

## Feedback Welcome

Agent Observatory is early-stage infrastructure.

Design feedback, critique and edge-case discussion are very welcome.
Please open a Discussion or Issue.
