"""
HTTP streaming client for testing the server.

Demonstrates:
- Consuming Server-Sent Events
- Connection handling
- Error recovery

Run with:
    uv run client.py
"""

import asyncio
import sys

import httpx


async def consume_stream(url: str, prompt: str = "Hello, streaming agent!") -> None:
    """Consume streaming responses from the server."""
    print(f"Sending request to: {url}")
    print(f"Prompt: {prompt}")
    print("-" * 50)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("POST", url, params={"prompt": prompt}) as response:
                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    print(await response.aread())
                    return

                print("Streaming response:")
                print("-" * 30)

                # Consume Server-Sent Events
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        token = line[6:]  # Remove "data: " prefix
                        print(token, end="", flush=True)

                print("\n" + "-" * 30)
                print("Stream complete!")

    except httpx.ConnectError:
        print("Error: Could not connect to server")
        print("Make sure the server is running: uv run server.py")
    except asyncio.CancelledError:
        print("\nStream interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def test_tool_endpoint() -> None:
    """Test the tool-enabled endpoint."""
    print("\nTesting tool-enabled endpoint:")
    print("=" * 50)

    await consume_stream(
        "http://localhost:8000/chat/stream-with-tools", "What's the weather like today?"
    )


async def interactive_client() -> None:
    """Interactive client for testing multiple prompts."""
    print("HTTP Streaming Client")
    print("=" * 50)
    print("Type prompts to send to the server.")
    print("Type 'quit' to exit, 'tools' to test tool endpoint.")
    print()

    base_url = "http://localhost:8000/chat/stream"

    while True:
        try:
            prompt = input("Prompt> ").strip()

            if not prompt:
                continue
            elif prompt.lower() == "quit":
                break
            elif prompt.lower() == "tools":
                await test_tool_endpoint()
                continue

            await consume_stream(base_url, prompt)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


async def main() -> None:
    """Main entry point."""
    if len(sys.argv) > 1:
        # Command line mode
        prompt = " ".join(sys.argv[1:])
        await consume_stream("http://localhost:8000/chat/stream", prompt)
    else:
        # Interactive mode
        await interactive_client()


if __name__ == "__main__":
    asyncio.run(main())
