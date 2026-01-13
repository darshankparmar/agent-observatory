# Agent Observatory for Framework Authors

This document describes **how agent frameworks and runtimes should embed
Agent Observatory**.

It is written for:
- framework maintainers
- platform / infrastructure teams
- runtime authors building long-running or streaming agents

It is **not** intended for end users or application developers.

## What Agent Observatory Provides (in One Sentence)

Agent Observatory provides a **fail-open, session-centric instrumentation layer** for observing **long-running, streaming AI agents** without interfering with agent execution or existing observability infrastructure.

## Core Principle: Runtime Owns Observability

**Frameworks, not agents, own observability lifecycle.**

An agent should:
- receive a session object
- emit semantic spans and stream events
- never create or manage sessions

A runtime should:
- create and close sessions
- define session boundaries
- choose exporters
- control execution mode (inline vs server)

This separation is mandatory.

## Session Lifecycle (Required Pattern)

A **session represents one agent run**.

The runtime must create exactly one session per run and ensure it is closed.

```python
with observatory.start_session(runtime_ctx) as session:
    agent.run(session)
```

### Guarantees provided by a session

* all agent activity is buffered or safely dropped
* exporter failures never affect execution
* traces are flushed atomically on exit
* no global state is modified

Sessions are the **unit of correctness**.

```
See:
- `examples/reference/real_time_agent_runtime/runtime.py`
```

## Agent Instrumentation Semantics

Agents should explicitly describe **what they are doing**, not how observability works.

### Span kinds (recommended)

| Kind         | Meaning                              |
| ------------ | ------------------------------------ |
| `agent_step` | Reasoning, planning, decision phases |
| `llm_call`   | Any model invocation                 |
| `tool_call`  | External tool or function execution  |
| `stream`     | Long-lived or high-frequency output  |

Example:

```python
with session.span("plan", kind="agent_step"):
    ...

with session.span("llm_call", kind="llm_call"):
    ...

with session.span("tool:web_search", kind="tool_call"):
    ...
```

Spans must be:

* explicit
* nested meaningfully
* free of side effects

```
See:
- `examples/reference/real_time_agent_runtime/agent.py`
```

## Streaming Is First-Class

Streaming output (tokens, audio, events) must be observable **without blocking execution**.

```python
with session.stream("response_stream") as stream:
    for chunk in chunks:
        stream.emit_event("token", {"content": chunk})
```

### Streaming guarantees

* ordered emission
* in-memory buffering
* no await points required
* safe for high-frequency events

This is a primary differentiator from traditional tracing.

```
See:
- `examples/reference/real_time_agent_runtime/agent.py` (respond span)
- `examples/integrations/livekit/observability.py`
```

## Exporters Are Downstream

Exporters:

* receive a fully materialized session envelope
* are synchronous
* must never raise
* must never influence runtime behavior

Frameworks may:

* use one exporter
* fan-out to multiple exporters
* swap exporters without touching agent code

Example:

```python
exporters: list[Exporter] = [
    ConsoleExporter(),
    FileExporter("logs/demo_traces.jsonl"),
    OTelExporter(tracer),
]
```

Exporter choice is **runtime configuration**, not agent logic.

## OpenTelemetry Coexistence

Agent Observatory **does not configure OpenTelemetry**.

If a framework already uses OTEL:

* keep existing instrumentation untouched
* pass a pre-configured tracer to the AO OTEL exporter
* avoid global tracer provider mutation

Agent Observatory is designed to **coexist cleanly** with OTEL-instrumented systems.

## Failure Semantics (Non-Negotiable)

Agent Observatory is **fail-open by contract**.

Frameworks must assume:

* observability can drop data
* exporters can fail silently
* sessions may be incomplete under overload

Frameworks must **not**:

* retry observability operations
* block agent execution
* surface observability failures to agents

Agent reliability always wins over observability completeness.

## Reference Implementations

Framework authors should study these in order:

1. **Canonical runtime embedding**

   ```
   examples/reference/real_time_agent_runtime/
   ```

2. **Real-world real-time integration**

   ```
   integrations/livekit/
   ```

These are **reference patterns**, not demos.

## Non-Goals (Read This)

Agent Observatory intentionally does **not** provide:

* storage
* querying
* dashboards
* metrics
* analytics
* agent abstractions
* automatic configuration

Framework authors must respect these boundaries.

See:

```
docs/design/non-goals.md
```

Breaking these constraints is considered a **design regression**.

## When Agent Observatory Is a Good Fit

Agent Observatory is appropriate if your framework:

* runs agents longer than a single request
* emits streaming output
* needs observability without vendor lock-in
* must not crash or block on telemetry
* already has or plans to use OpenTelemetry

If your framework needs a turnkey UI or analytics platform,
Agent Observatory is **not** the right layer.

## Adopting Agent Observatory in Existing Frameworks

Agent Observatory is designed to coexist with existing observability approaches.

Frameworks typically adopt it by:
- keeping existing logging and metrics unchanged
- continuing to use OpenTelemetry for infrastructure spans
- adding Agent Observatory only for agent-level semantics

No migration or replacement of existing systems is required.

## Summary

Agent Observatory should be embedded as:

* a **runtime-owned session boundary**
* a **semantic description of agent behavior**
* a **fail-open bridge** to existing observability stacks

Frameworks that follow these patterns gain:

* safe observability
* clearer agent traces
* cleaner architecture
* zero coupling between agents and telemetry backends
