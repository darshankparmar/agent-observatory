import logging
from livekit.agents import Agent, RunContext
from livekit.agents.llm import function_tool

logger = logging.getLogger("agent")


class MyAgent(Agent):
    def __init__(self, obs_session):
        super().__init__(
            instructions=(
                "Your name is Kelly. You interact via voice. "
                "Be concise, friendly, and clear."
            )
        )
        self.obs = obs_session

    async def on_enter(self):
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
        with self.obs.span("tool.lookup_weather", kind="tool_call") as span:
            span.emit_event(
                "tool.input",
                {
                    "location": location,
                    "lat": latitude,
                    "lon": longitude,
                },
            )

            logger.info("Looking up weather for %s", location)

            result = "Sunny, 70 degrees"

            span.emit_event(
                "tool.output",
                {
                    "result": result,
                },
            )

            return result
