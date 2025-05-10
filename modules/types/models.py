from typing import TypedDict
from langchain_core.messages import BaseMessage

class Requirements(TypedDict):
    project_name: str
    project_description: str
    packages: list[str]
    technology : str

class FileInfo(TypedDict):
    name: str
    path : str
    dependencies : list[str]
    technical_specifications : str
    is_generated : bool
    code : str | None

class ResultState(TypedDict):
    messages : list[BaseMessage]
    success : bool
    error : str | None
    version : int
    retries : int