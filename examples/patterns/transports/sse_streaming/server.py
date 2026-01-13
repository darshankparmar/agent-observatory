"""
SSE streaming server for agent responses.

Run with:
    uv run server.py
"""

import asyncio
import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse

from agent_observatory import (
    AgentContext,
    ConsoleExporter,
    FileExporter,
    Observatory,
)

obs: Observatory


@asynccontextmanager
async def lifespan(app: FastAPI):
    await obs.start()
    yield
    await obs.shutdown()


app = FastAPI(
    title="SSE Streaming Agent API",
    lifespan=lifespan,
)


# ---------------------------------------------------------
# Simulated async agent response
# ---------------------------------------------------------


async def simulate_agent_response(prompt: str) -> AsyncGenerator[str, None]:
    parts = [
        f"Processing your request: '{prompt}'",
        "Analyzing the context...",
        "Generating response...",
        f"Here's my response to: {prompt}",
        "This is streamed in real-time using SSE.",
        "Each part arrives as a separate event.",
    ]

    for part in parts:
        yield part
        await asyncio.sleep(0.5)


# ---------------------------------------------------------
# Web client
# ---------------------------------------------------------


@app.get("/")
async def get_client():
    with open("web_client.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# ---------------------------------------------------------
# SSE endpoint (CORRECT FRAMING)
# ---------------------------------------------------------


@app.get("/chat/stream")
async def chat_stream(
    session_id: str = Query(...),
    message: str = Query(...),
):
    ctx = AgentContext(
        session_id=session_id,
        agent_id="sse-agent",
        user_id="web-user",
        metadata={"transport": "sse"},
    )

    async def event_stream():
        with obs.start_session(ctx) as session:
            with session.agent_step("sse_chat_response") as span:
                span.event("request_received", {"prompt": message})

                index = 0
                async for part in simulate_agent_response(message):
                    index += 1

                    yield {
                        "event": "content",
                        "data": json.dumps({"content": part}),
                    }

                yield {
                    "event": "complete",
                    "data": json.dumps({"message": "Response complete"}),
                }

                span.event("response_complete", {"status": "ok", "total_parts": index})

    return EventSourceResponse(event_stream())


@app.get("/health")
async def health():
    return {"status": "healthy"}


def main():
    global obs

    obs = Observatory(
        exporter=[
            ConsoleExporter(),
            FileExporter("logs/sse_traces.jsonl"),
        ],
        inline=True,
    )

    print("SSE Streaming Agent Server")
    print("Open http://localhost:8000")

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
