from pydantic import BaseModel

class Requirements(BaseModel):
    """
    This is a pydantic model for the initial user requirements in state
    """
    project_name: str
    description: str
    packages: list[str]

    def __str__(self):
        return (
            f"Project Name: {self.project_name}\n"
            f"Packages: {', '.join(self.packages)}\n"
            f"Description: {self.description}"
        )