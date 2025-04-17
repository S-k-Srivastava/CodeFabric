from typing import Callable
from langchain.chat_models.base import BaseChatModel

"""
This is a custom type for LLMs with temperature, so that we can pass the temperature to the LLM based on use case.
"""

LLM_WITH_TEMPRATURE = Callable[[float], BaseChatModel]
