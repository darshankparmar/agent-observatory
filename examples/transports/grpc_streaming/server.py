"""
gRPC streaming server for agent responses.

Demonstrates:
- Bidirectional gRPC streaming
- Protocol buffer type safety
- Connection lifecycle management
- Production-ready error handling

Run with:
    uv run server.py
"""

import asyncio
import logging
from collections.abc import AsyncGenerator
from concurrent import futures

# Generated from agent_service.proto
import agent_service_pb2
import agent_service_pb2_grpc
import grpc

from agent_observatory import (
    AgentContext,
    ConsoleExporter,
    Exporter,
    FileExporter,
    Observatory,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentServicer(agent_service_pb2_grpc.AgentServiceServicer):
    """gRPC servicer implementing the AgentService."""

    def __init__(self, observatory: Observatory):
        self.obs = observatory

    async def StreamChat(
        self,
        request_iterator: AsyncGenerator[agent_service_pb2.ChatRequest, None],
        context: grpc.ServicerContext,
    ) -> AsyncGenerator[agent_service_pb2.ChatResponse, None]:
        """
        Handle bidirectional streaming chat.

        Demonstrates observability for:
        - Connection lifecycle
        - Message processing
        - Streaming responses
        """
        # Create unique session for this gRPC connection
        ctx = AgentContext(
            session_id=f"grpc-{context.peer()}",
            agent_id="grpc-agent",
            user_id="remote-user",
        )

        with self.obs.start_session(ctx) as session:
            with session.agent_step("grpc_connection") as span:
                try:
                    async for request in request_iterator:
                        # Process each message
                        async for response in self._process_message(session, request):
                            yield response

                except grpc.RpcError as e:
                    span.event("grpc_error", {"code": e.code(), "details": e.details()})
                    logger.error(f"gRPC error: {e}")
                except Exception as e:
                    span.event("unexpected_error", {"error": str(e)})
                    logger.error(f"Unexpected error: {e}")

    async def _process_message(
        self, session, request: agent_service_pb2.ChatRequest
    ) -> AsyncGenerator[agent_service_pb2.ChatResponse, None]:
        """Process a single message and stream response."""
        with session.agent_step("process_message") as span:
            span.event(
                "message_received", {"session_id": request.session_id, "message": request.message}
            )

            # Simulate LLM token streaming
            response_text = self._generate_response(request.message)

            # Stream response token by token
            accumulated = ""
            for token in response_text.split():
                accumulated += token + " "

                response = agent_service_pb2.ChatResponse(
                    content=token + " ", is_complete=False, metadata={"token_count": "1"}
                )

                span.event("token_sent", {"token": token})
                yield response

                # Simulate processing delay
                await asyncio.sleep(0.05)

            # Send final completion message
            final_response = agent_service_pb2.ChatResponse(
                content="",
                is_complete=True,
                metadata={"total_tokens": str(len(response_text.split()))},
            )

            span.event("stream_complete", {"total_tokens": len(response_text.split())})
            yield final_response

    def _generate_response(self, message: str) -> str:
        """Generate a response for the given message."""
        # Simple response generation - in real usage, this would call an LLM
        if "hello" in message.lower():
            return "Hello! How can I help you today?"
        elif "weather" in message.lower():
            return "I can't check the weather, but it's always a good day to learn!"
        else:
            return f"You said: '{message}'. That's interesting!"


async def serve() -> None:
    """Start the gRPC server."""
    # Create observatory with multiple exporters
    exporters: list[Exporter] = [
        ConsoleExporter(),
        FileExporter("logs/grpc_traces.jsonl"),
    ]

    obs = Observatory(exporters=exporters, inline=True)

    # Create server
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add servicer
    servicer = AgentServicer(obs)
    agent_service_pb2_grpc.add_AgentServiceServicer_to_server(servicer, server)

    # Configure port
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)

    logger.info(f"Starting gRPC server on {listen_addr}")
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await server.stop(5)


if __name__ == "__main__":
    asyncio.run(serve())
