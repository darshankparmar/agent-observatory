# Integration Examples

This folder demonstrates how Agent Observatory integrates with third-party services and frameworks.

## Examples

- [`livekit/`](livekit/) - Real-time voice and video agents
- [`opentelemetry/`](opentelemetry/) - Production monitoring and observability stacks

## Key Concepts

- **Zero global state**: Agent Observatory never configures global state
- **Application responsibility**: All configuration is done by the application
- **Fail-open**: Integration failures never crash agent execution