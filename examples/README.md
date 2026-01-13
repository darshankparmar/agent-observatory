# Agent Observatory Examples

This directory contains **reference implementations, integrations and patterns** demonstrating how Agent Observatory is embedded at different layers of an agent system.

The examples are **not equal in intent**. They are organized by **role and level of abstraction**.

## Quick Start (Choose Your Path)

- **Framework / Runtime Authors**
  → Start with `reference/real_time_agent_runtime/`

- **Integration & Platform Engineers**
  → See `integrations/` for concrete service integrations

- **Exploring Specific Techniques**
  → Browse `patterns/` for isolated implementation patterns

## Reference Implementation

### `reference/real_time_agent_runtime/`

The **canonical embedding pattern** for Agent Observatory.

This example demonstrates:

- runtime-owned session lifecycle
- explicit agent semantics (`agent_step`, `llm_call`, `tool_call`)
- streaming-first observability
- exporter neutrality
- fail-open guarantees in practice

This is the **authoritative example** that framework authors should study and follow. All other examples build on the same principles.

## Service Integrations

### `integrations/`

Concrete integrations with third-party systems and production infrastructure.

- `integrations/livekit/`  
  Real-time voice and video agents using LiveKit. Demonstrates session mapping, streaming audio events and coexistence with existing OpenTelemetry spans.

- `integrations/opentelemetry/`  
  Integration with OpenTelemetry backends using a pre-configured tracer. Shows how Agent Observatory complements existing observability stacks.

These examples assume familiarity with the underlying services.

## Implementation Patterns

### `patterns/`

Focused, isolated examples demonstrating **specific observability techniques** without full runtime context.

Patterns are intentionally smaller and should be read **after** the reference implementation.

See `patterns/README.md` for details.

## Running Examples

All examples assume:

- Python >= 3.10
- Agent Observatory installed
- Optional dependencies installed where required (see each example’s README)

Inline examples can be run directly:

```bash
uv run <example>.py
```

## Notes

If you are building or maintaining an agent framework, **do not start with the patterns**. Begin with the reference implementation to understand the correct lifecycle and ownership model.