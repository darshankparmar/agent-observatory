from time import sleep

from tools import web_search


class Agent:
    def run(self, session) -> None:
        # High-level planning step
        with session.span("plan", kind="agent_step"):
            sleep(0.1)

        # Simulated LLM call
        with session.span("llm_call", kind="llm_call"):
            sleep(0.2)

        # Tool invocation
        with session.span("tool:web_search", kind="tool_call"):
            result = web_search("agent observability patterns")
            print(f"Tool result: {result}")

        # Streaming output (tokens, audio, events, etc.)
        with session.span("respond", kind="agent_step"):
            with session.stream("response_stream") as stream:
                for i in range(5):
                    stream.emit_event(
                        "token",
                        {
                            "index": i,
                            "content": f"token-{i}",
                        },
                    )
                    sleep(0.05)

        # Final reasoning step
        with session.span("finalize", kind="agent_step"):
            sleep(0.1)
