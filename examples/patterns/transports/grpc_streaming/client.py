"""
gRPC streaming client for testing the agent service.

Demonstrates:
- Bidirectional streaming consumption
- Connection management
- Error handling and reconnection

Run with:
    uv run client.py
"""

import asyncio
import logging
import sys

# Generated from agent_service.proto
import agent_service_pb2
import agent_service_pb2_grpc
import grpc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_message(
    stub: agent_service_pb2_grpc.AgentServiceStub, session_id: str, message: str
) -> None:
    """Send a single message and stream the response."""
    try:
        # Create request iterator
        async def request_iterator():
            yield agent_service_pb2.ChatRequest(
                session_id=session_id, message=message, metadata={"client": "python-grpc"}
            )

        # Stream responses
        response_stream = stub.StreamChat(request_iterator())

        print("\n🤖 Agent: ", end="", flush=True)

        async for response in response_stream:
            if response.content:
                print(response.content, end="", flush=True)

            if response.is_complete:
                print("\n")
                break

    except grpc.RpcError as e:
        print(f"\n❌ gRPC error: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


async def interactive_client() -> None:
    """Interactive client for testing multiple messages."""
    print("gRPC Streaming Client")
    print("=" * 50)
    print("Type messages to send to the agent.")
    print("Type 'quit' to exit.")
    print()

    # Connect to server
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = agent_service_pb2_grpc.AgentServiceStub(channel)

        session_id = f"session-{asyncio.get_event_loop().time()}"

        while True:
            try:
                message = input("You> ").strip()

                if not message:
                    continue
                elif message.lower() == "quit":
                    break

                await send_message(stub, session_id, message)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


async def test_messages() -> None:
    """Test with predefined messages."""
    test_messages = ["Hello, agent!", "What's the weather like?", "Tell me about gRPC streaming"]

    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = agent_service_pb2_grpc.AgentServiceStub(channel)

        session_id = f"test-{asyncio.get_event_loop().time()}"

        for message in test_messages:
            print(f"\n📤 Sending: {message}")
            await send_message(stub, session_id, message)


async def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        await test_messages()
    else:
        await interactive_client()


if __name__ == "__main__":
    asyncio.run(main())
