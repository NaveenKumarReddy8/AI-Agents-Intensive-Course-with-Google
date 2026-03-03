from dotenv import load_dotenv

load_dotenv(".env")

from google.adk.models.google_llm import Gemini
from google.genai.types import HttpRetryOptions

http_retry_config = HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

model = Gemini(name="gemini-2.5-flash-lite", retry_options=http_retry_config)
