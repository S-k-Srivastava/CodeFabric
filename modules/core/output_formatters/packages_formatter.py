from pydantic import BaseModel, Field

class PackagesFormatter(BaseModel):
    """
    This is a pyndantic model for the structured output for listing packages
    """
    packages: list[str] = Field(...,description="List of exact packages to install.")