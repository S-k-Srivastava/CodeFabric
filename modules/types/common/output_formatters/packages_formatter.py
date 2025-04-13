from pydantic import BaseModel, Field


class PackagesFormatter(BaseModel):
    packages: list[str] = Field(...,description="List of exact packages to install.")