from pydantic import BaseModel

class CurrentFile(BaseModel):
    index : int = -1
    code : str | None = None