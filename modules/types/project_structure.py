from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
class File(BaseModel):
    name: str = Field(...,description="file name with proper extension.")
    path : str = Field(...,description="relative file path.")
    documentation : str = Field(...,description="File documentation,Breif info about this file and how to use the `dependencies` listed.")
    dependencies : list[str] = Field(...,description="list of path of all other files that this file depends on. I.e these files must be generated before this file.")
    is_generated : bool = Field(default=False,description="LEAVE IT FALSE")
    code : str = Field(default="",description="LEAVE IT EMPTY STRING")

class ProjectStructure(BaseModel):
    files: list[File] = Field(...,description="list of all the files to be generated for the given project")