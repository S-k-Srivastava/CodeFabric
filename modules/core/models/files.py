from pydantic import BaseModel

class File(BaseModel):
    """
    For storing files and related information,
    Do not extended this until you are a pro developer.
    """
    name: str
    path : str
    description : str
    dependencies : list[str]
    is_generated : bool
    code : str