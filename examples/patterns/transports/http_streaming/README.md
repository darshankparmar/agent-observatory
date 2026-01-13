# HTTP Streaming Example

This example demonstrates how to build an HTTP-based streaming agent using FastAPI. It shows how to stream LLM responses token-by-token while maintaining full observability.

## What It Demonstrates

- HTTP streaming responses with Server-Sent Events
- Token-by-token LLM response streaming
- Backpressure handling and connection management
- Observability for HTTP request/response lifecycle
- Error handling and graceful disconnections

## File Overview

- [`server.py`](server.py): FastAPI server with streaming endpoints
- [`client.py`](client.py): HTTP client consuming streaming responses

## Running

```bash
# Install dependencies
uv pip install -r requirements.txt

# Start the server
uv run server.py

# In another terminal, test with client
uv run client.py
```

## Key Takeaway

HTTP streaming provides a simple, standards-based approach for real-time agent communication without requiring WebSocket connections or specialized protocols.