"""
HTTP streaming server for agent responses.

Demonstrates:
- FastAPI streaming responses
- Token-by-token LLM simulation
- Request lifecycle observability
- Backpressure handling

Run with:
    uv run server.py
"""

import asyncio
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from agent_observatory import (
    AgentContext,
    ConsoleExporter,
    FileExporter,
    MultiExporter,
    Observatory,
)

# Global observatory instance
obs: Observatory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage observatory lifecycle."""
    # Start background worker for production
    await obs.start()
    yield
    # Graceful shutdown
    await obs.shutdown()


app = FastAPI(
    title="Streaming Agent API",
    description="HTTP streaming agent with observability",
    lifespan=lifespan,
)


async def simulate_llm_tokens(prompt: str) -> AsyncGenerator[str, None]:
    """Simulate LLM token generation."""
    # Simple simulation - in real usage, this would call an LLM
    response = f"This is a simulated response to: {prompt}"
    words = response.split()

    for word in words:
        yield word + " "
        await asyncio.sleep(0.1)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chat/stream", response_model=None)
async def chat_stream(prompt: str = "Hello, agent!"):
    async def event_stream() -> AsyncGenerator[str, None]:
        ctx = AgentContext(
            session_id=f"http-{int(time.time() * 1000)}",
            agent_id="http-streaming-agent",
            user_id="web-client",
            metadata={"endpoint": "/chat/stream", "prompt_length": len(prompt)},
        )

        with obs.start_session(ctx) as session:
            with session.agent_step("process_http_request") as request_span:
                request_span.event("request_received", {"prompt": prompt})

                with session.llm_call("generate_response") as llm_span:
                    llm_span.event("llm_start", {"prompt": prompt})

                    full_response = ""
                    async for token in simulate_llm_tokens(prompt):
                        full_response += token

                        llm_span.event(
                            "token_emitted",
                            {
                                "token": token.strip(),
                                "response_length": len(full_response),
                            },
                        )

                        yield f"data: {token}\n\n"

                    llm_span.event(
                        "llm_complete",
                        {
                            "full_response": full_response,
                            "total_tokens": len(full_response.split()),
                        },
                    )

                request_span.event(
                    "request_complete",
                    {
                        "response_length": len(full_response),
                        "status": "success",
                    },
                )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


@app.post("/chat/stream-with-tools", response_model=None)
async def chat_stream_with_tools(prompt: str = "What's the weather?"):
    async def event_stream() -> AsyncGenerator[str, None]:
        ctx = AgentContext(
            session_id=f"http-tools-{int(time.time() * 1000)}",
            agent_id="http-tools-agent",
            user_id="web-client",
            metadata={"endpoint": "/chat/stream-with-tools"},
        )

        with obs.start_session(ctx) as session:
            with session.agent_step("process_request_with_tools"):
                # Tool invocation
                if "weather" in prompt.lower():
                    with session.tool_call("get_weather") as tool_span:
                        tool_span.event("tool_start", {"query": prompt})

                        await asyncio.sleep(0.5)
                        weather_data = {"temp": 72, "condition": "sunny"}

                        tool_span.event("tool_complete", {"result": weather_data})

                        yield (
                            f"data: Weather: {weather_data['temp']}°F, "
                            f"{weather_data['condition']}\n\n"
                        )

                # Continue with normal response
                yield "data: Based on the data, here's my response...\n\n"

                async for token in simulate_llm_tokens(prompt):
                    yield f"data: {token}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


def main() -> None:
    """Start the HTTP streaming server."""
    global obs

    # Configure multi-exporter for development
    exporters = MultiExporter(
        [
            ConsoleExporter(),
            FileExporter("logs/http_streaming.jsonl"),
        ]
    )

    # Use async mode for production server
    obs = Observatory(exporter=exporters, inline=False)

    print("Starting HTTP streaming server on http://localhost:8000")
    print("Try: curl -N http://localhost:8000/chat/stream")
    print("Or run: uv run client.py")

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
