from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.genai.types import HttpRetryOptions

load_dotenv(".env")

retry_config = HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504]
)

gemini_model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config,
)

outline_agent = Agent(
    model=gemini_model,
    name="OutlineAgent",
    instruction="""Create a blog outline for the given topic with:
    1. A catchy Headline.
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each.
    4. A concluding thought.
    """,
    output_key="blog_outline",
)

writer_agent = Agent(
    model=gemini_model,
    name="WriterAgent",
    instruction="""Following the outline strictly: {blog_outline}
    Write a brief, 200 to 300 word blog post with an engaging and informative tone.
    """,
    output_key="blog_draft",
)

editor_agent = Agent(
    model=gemini_model,
    name="EditorAgent",
    instruction="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow
    and sentence structure, and enhancing overall clarity.
    """,
    output_key="final_blog",
)

root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent],
)
