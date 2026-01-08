# Multiple Exporters Example

This example demonstrates how to use multiple exporters simultaneously with Agent Observatory, sending traces to console, file and OpenTelemetry at the same time.

## What It Demonstrates

- Simultaneous export to multiple backends
- Error isolation between exporters
- Development vs production configurations
- Redundant logging for critical systems

## File Overview

- [`multi_demo.py`](multi_demo.py): example using multiple exporters

## Running

```bash
uv run multi_demo.py
```

## Key Takeaway

MultiExporter enables flexible observability configurations - debug locally with console output while persisting to files and ship to production with OTEL integration.