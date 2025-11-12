from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.genai.types import HttpRetryOptions

load_dotenv(".env")

model = Gemini(
    model="gemini-2.5-flash",
    retry_options=HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    ),
)
root_agent = Agent(
    model=model,
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
)


async def main():
    from google.adk.runners import InMemoryRunner

    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("What is the capital of France?")
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
