from google.adk.agents import Agent
from google.adk.tools import google_search

from multi_agent.config import model

research_agent = Agent(
    name="ResearchAgent",
    model=model,
    instruction="""You are a specialized research agent. Your only job is to use the
    google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
    tools=[google_search],
    output_key="research_findings",  # The result of this agent will be stored in the session state with this key.
)
summarizer_agent = Agent(
    name="SummarizerAgent",
    model=model,
    # The instruction is modified to request a bulleted list for a clear output format.
    instruction="""Read the provided research findings: {research_findings}
Create a concise summary as a bulleted list with 3-5 key points.""",
    output_key="final_summary",
)
