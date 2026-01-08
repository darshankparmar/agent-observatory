# gRPC Streaming Example

This example demonstrates how to build a gRPC-based streaming agent with bidirectional communication. It shows how to stream agent responses and handle real-time interactions with type safety.

## What It Demonstrates

- Bidirectional gRPC streaming for real-time communication
- Protocol buffer type safety
- Streaming LLM responses over gRPC
- Connection management and error handling
- Observability for gRPC request/response lifecycle
- Production-ready patterns with proper lifecycle management

## File Overview

- [`agent_service.proto`](agent_service.proto): Protocol buffer definition for the agent service
- [`server.py`](server.py): gRPC server with streaming implementation
- [`client.py`](client.py): gRPC client with streaming consumer

## Running

```bash
# Install dependencies
uv pip install -r requirements.txt

# Generate Python code from proto
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. agent_service.proto

# Start the server
uv run server.py

# In another terminal, test with client
uv run client.py
```

## Key Takeaway

gRPC provides type-safe, high-performance bidirectional streaming ideal for production agent systems while maintaining full observability through Agent Observatory.