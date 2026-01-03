# LiveKit Agent with Agent Observatory

This example shows how to integrate **Agent Observatory** with a **LiveKit Agent** and export agent traces to **OpenTelemetry / Jaeger**.

It demonstrates the **recommended production pattern**:

* OpenTelemetry configured at the application level
* Agent Observatory used as an event-based observability layer
* Compatible with LiveKit’s built-in OTEL instrumentation

---

## Setup

### 1. Install Agent Observatory

```bash
uv pip install -e ../../
```

### 2. Install example dependencies

```bash
uv add python-dotenv livekit-agents
uv add livekit-plugins-cartesia livekit-plugins-deepgram livekit-plugins-silero
uv add livekit-plugins-turn-detector
```

### 3. Configure environment

Create `.env` with your LiveKit and model credentials.

---

## Run Jaeger (local)

```bash
docker run -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one
```

Jaeger UI: [http://localhost:16686](http://localhost:16686)

---

## Run the agent

```bash
uv run server.py console
```

Traces will appear in Jaeger under the configured service name.

---

## Notes

* `inline=True` is used to ensure traces are exported synchronously
* Agent Observatory does **not** configure OpenTelemetry
* Works safely alongside LiveKit’s native OTEL spans
