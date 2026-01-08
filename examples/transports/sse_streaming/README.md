# Server-Sent Events (SSE) Streaming Example

This example demonstrates how to build a Server-Sent Events (SSE) based streaming agent for web browsers. It shows how to push real-time updates to web clients while maintaining full observability.

## What It Demonstrates

- Server-Sent Events for unidirectional streaming to browsers
- Real-time agent updates in web browsers
- Simple web-based client interface
- Connection management and automatic reconnection
- Observability for SSE request/response lifecycle
- Browser-native event consumption

## File Overview

- [`server.py`](server.py): FastAPI server with SSE endpoints
- [`web_client.html`](web_client.html): Browser client consuming SSE events

## Running

```bash
# Install dependencies
uv pip install -r requirements.txt

# Start the server
uv run server.py

# Open browser and navigate to:
http://localhost:8000
```

## Key Takeaway

SSE provides a simple, browser-native approach for real-time agent updates without requiring WebSocket connections or client-side libraries.
