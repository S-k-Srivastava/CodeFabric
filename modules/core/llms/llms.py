from langchain_deepinfra import ChatDeepInfra
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY")

"""
Define lambda functions returning llms with type LLM_WITH_TEMPERATURE
"""

deep_infra_with_temperature = lambda x : ChatDeepInfra(
    model="meta-llama/Llama-3.3-70B-Instruct",
    temperature=x,
    api_key=DEEPINFRA_API_KEY
)

google_with_temperature = lambda x : ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    temperature=x
)

openai_with_temperature = lambda x : ChatOpenAI(
    model="gpt-4o",
    temperature=x
)