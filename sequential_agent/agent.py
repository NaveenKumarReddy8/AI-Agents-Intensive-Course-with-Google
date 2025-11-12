from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, AgentTool
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

outline_agent = Agent(
    name="OutlineAgent",
    model=model,
    instruction="""Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key="blog_outline",  # The result of this agent will be stored in the session state with this key.
)

writer_agent = Agent(
    name="WriterAgent",
    model=model,
    # The `{blog_outline}` placeholder automatically injects the state value from the previous agent's output.
    instruction="""Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key="blog_draft",  # The result of this agent will be stored with this key.
)

editor_agent = Agent(
    name="EditorAgent",
    model=model,
    # This agent receives the `{blog_draft}` from the writer agent's output.
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key="final_blog",  # This is the final output of the entire pipeline.
)

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)


async def main():
    from google.adk.runners import InMemoryRunner

    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("Research about latest trends in Generative AI")
    # print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
