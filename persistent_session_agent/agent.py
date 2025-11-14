from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

load_dotenv(".env")

MODEL_NAME = "gemini-2.5-flash-lite"
APP_NAME = "default"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session

model = Gemini(
    model=MODEL_NAME,
    retry_options=types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    ),
)

chatbot_agent = Agent(
    model=model,
    name="text_chat_bot",
    description="A text chatbot with persistent memory",
)

# Step 2: Switch to DatabaseSessionService
# SQLite database will be created automatically
db_url = "sqlite:///my_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)

# Step 3: Create a new runner with persistent storage
runner = Runner(agent=chatbot_agent, app_name=APP_NAME, session_service=session_service)


async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(app_name=app_name, user_id=USER_ID, session_id=session_name)
    except AlreadyExistsError:
        session = await session_service.get_session(app_name=app_name, user_id=USER_ID, session_id=session_name)

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if isinstance(user_queries, str):
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(user_id=USER_ID, session_id=session.id, new_message=query):
                # Check if the event contains valid content
                # print(f"event is: {event}")
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if event.content.parts[0].text != "None" and event.content.parts[0].text:
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")


async def main():
    await run_session(
        runner,
        [
            "Hi, I am Sam! What is the capital of United States?",
            "Hello! What is my name?",  # This time, the agent should remember!
        ],
        "stateful-agentic-session",
    )

    await run_session(
        runner,
        ["What did I ask you about earlier?", "And remind me, what's my name?"],
        "stateful-agentic-session",
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
