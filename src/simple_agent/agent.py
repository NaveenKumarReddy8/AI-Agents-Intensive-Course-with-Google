from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

load_dotenv(".env")

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504]
)

root_agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    name="root_agent",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current information or if unsure.",
    tools=[google_search],
)

runner = InMemoryRunner(agent=root_agent)


async def run():
    response = await runner.run_debug("What's the weather in Hyderabad?")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
