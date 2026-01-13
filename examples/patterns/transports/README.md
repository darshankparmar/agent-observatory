# Transport Layer Examples

This folder demonstrates how Agent Observatory works with different transport protocols for real-time agent communication. Each example shows the same observability patterns applied to different communication layers.

## Transport Examples

### [`http_streaming/`](http_streaming/)
HTTP-based streaming with Server-Sent Events.

- **Use Case**: Web applications, simple client-server communication
- **Protocol**: HTTP/1.1 with SSE
- **Features**: Token streaming, tool integration, backpressure handling
- **Files**: [`server.py`](http_streaming/server.py), [`client.py`](http_streaming/client.py)

### [`grpc_streaming/`](grpc_streaming/)
Type-safe bidirectional streaming with gRPC.

- **Use Case**: Production microservices, type-safe contracts
- **Protocol**: gRPC with Protocol Buffers
- **Features**: Bidirectional streaming, code generation, production patterns
- **Files**: [`agent_service.proto`](grpc_streaming/agent_service.proto), [`server.py`](grpc_streaming/server.py), [`client.py`](grpc_streaming/client.py)

### [`sse_streaming/`](sse_streaming/)
Browser-native streaming with Server-Sent Events.

- **Use Case**: Web browsers, simple real-time updates
- **Protocol**: Server-Sent Events (SSE)
- **Features**: Browser client, real-time updates, no WebSocket dependency
- **Files**: [`server.py`](sse_streaming/server.py), [`web_client.html`](sse_streaming/web_client.html)

## Key Concepts Demonstrated

### Observability Patterns
All transport examples demonstrate:
- **Connection lifecycle** - Track connection start/end events
- **Message flow tracing** - Observe request/response patterns
- **Error handling** - Graceful failure handling with observability
- **Performance monitoring** - Duration and throughput metrics

### Transport-Specific Insights
- **HTTP** - Request/response boundaries, streaming chunks
- **gRPC** - Method-level tracing, metadata propagation
- **SSE** - Event-driven updates, client disconnections
