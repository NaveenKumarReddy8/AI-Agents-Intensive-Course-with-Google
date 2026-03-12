from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

from simple_agent.config import model

root_agent = Agent(
    name="helpful_assistant",
    model=model,
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)


async def main():
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug(
        "What is Agent Development Kit from Google? What languages is the SDK available in?",
    )
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
