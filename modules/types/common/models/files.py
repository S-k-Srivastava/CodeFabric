from pydantic import BaseModel

class File(BaseModel):
    name: str
    path : str
    technical_specifications : str
    dependencies : list[str]
    is_generated : bool
    code : str
