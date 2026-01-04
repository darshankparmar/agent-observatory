"""
LiveKit agent implementation with Agent Observatory instrumentation.

This example demonstrates:
- instrumenting agent lifecycle hooks
- tracing tool calls
- emitting structured input/output events
- keeping observability separate from agent logic
"""

import logging

from livekit.agents import Agent, RunContext
from livekit.agents.llm import function_tool

logger = logging.getLogger("agent")


class MyAgent(Agent):
    def __init__(self, obs_session):
        """
        Initialize the agent.

        `obs_session` is an Agent Observatory session instance,
        scoped to the lifetime of this agent run.
        """
        super().__init__(
            instructions=(
                "Your name is Kelly. You interact via voice. "
                "Be concise, friendly and clear."
            )
        )
        self.obs = obs_session

    async def on_enter(self):
        """
        Called when the agent becomes active.

        We wrap the lifecycle hook in a span to make
        agent startup visible in traces.
        """
        with self.obs.span("agent.on_enter", kind="agent_step"):
            self.session.generate_reply(allow_interruptions=False)

    @function_tool
    async def lookup_weather(
        self,
        context: RunContext,
        location: str,
        latitude: str,
        longitude: str,
    ):
        """
        Example tool call with observability instrumentation.

        Demonstrates:
        - tool-level spans
        - structured input/output events
        - separation of business logic and observability
        """
        with self.obs.span("tool.lookup_weather", kind="tool_call") as span:
            # --- Tool input ---
            span.emit_event(
                "tool.input",
                {
                    "location": location,
                    "lat": latitude,
                    "lon": longitude,
                },
            )

            logger.info("Looking up weather for %s", location)

            # Simulated external call
            result = "Sunny, 70 degrees"

            # --- Tool output ---
            span.emit_event(
                "tool.output",
                {
                    "result": result,
                },
            )

            return result
