from dotenv import load_dotenv
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai.types import HttpRetryOptions

load_dotenv(".env")

retry_config = HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504]
)

gemini_model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config,
)

tech_researcher_agent = Agent(
    model=gemini_model,
    name="TechResearchedAgent",
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
    tools=[google_search],
    output_key="tech_research",
)

health_researcher_agent = Agent(
    name="HealthResearcher",
    model=gemini_model,
    instruction="""Research recent medical breakthroughs. Include 3 significant advances,
their practical applications, and estimated timelines. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="health_research",  # The result will be stored with this key.
)


finance_researcher_agent = Agent(
    name="FinanceResearcher",
    model=gemini_model,
    instruction="""Research current fintech trends. Include 3 key trends,
their market implications, and the future outlook. Keep the report concise (100 words).""",
    tools=[google_search],
    output_key="finance_research",  # The result will be stored with this key.
)

aggregator_agent = Agent(
    name="AggregatorAgent",
    model=gemini_model,
    # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
    instruction="""Combine these three research findings into a single executive summary:

    **Technology Trends:**
    {tech_research}
    
    **Health Breakthroughs:**
    {health_research}
    
    **Finance Innovations:**
    {finance_research}
    
    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
    output_key="executive_summary",  # This will be the final output of the entire system.
)

parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[
        tech_researcher_agent,
        health_researcher_agent,
        finance_researcher_agent,
    ],
)

root_agent = SequentialAgent(
    name="ResearchSystem", sub_agents=[parallel_research_team, aggregator_agent]
)


runner = InMemoryRunner(agent=root_agent)


async def main():
    response = await runner.run_debug(
        "Let me know about Health, Finance, and Technology research."
    )
    print(response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
