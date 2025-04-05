from langchain_google_genai import ChatGoogleGenerativeAI

default_llm_with_temperature = lambda x : ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21",temperature=x)