from langchain_google_genai import ChatGoogleGenerativeAI

default_llm_with_temperature = lambda x : ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=x)