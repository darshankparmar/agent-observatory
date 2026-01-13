# Real-Time Agent Runtime (Reference Example)

This example demonstrates how a **long-running agent runtime** embeds Agent Observatory as an **instrumentation layer**, without shaping runtime or agent architecture around it.

## What This Simulates

- One runtime-controlled agent session
- Long-lived execution
- Nested agent reasoning steps
- Tool calls as first-class actions
- High-frequency streaming events
- Exporter-neutral observability

## Who This Is For

- Agent framework maintainers
- Platform / infrastructure engineers
- Runtime authors integrating observability

## What This Demonstrates

- The runtime owns session lifecycle
- Agents emit semantic spans explicitly
- Streaming is first-class and safe
- Exporters are downstream and swappable
- Observability failures never affect execution
