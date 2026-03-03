from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner

from .config import model

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
    runner = InMemoryRunner()
    response = await runner.run_debug(
        "Write a blog post about the benefits of multi-agent systems for software developers"
    )
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
