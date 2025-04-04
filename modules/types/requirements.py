from pydantic import BaseModel, Field
from typing import List

class Requirements(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="Detailed santized description of the project")
    packages: List[str] = Field(..., description="List of npm packages to be used in the project")

    def __str__(self):
        return (
            f"Project Name: {self.project_name}\n"
            f"Packages: {', '.join(self.packages)}\n"
            f"Description: {self.description}\n\n"
        )