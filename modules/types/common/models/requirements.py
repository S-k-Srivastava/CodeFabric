from pydantic import BaseModel
from typing import List

from modules.types.common.output_formatters.packages_formatter import PackagesFormatter

class Requirements(BaseModel):
    project_name: str
    description: str
    packages: list[str]

    def __str__(self):
        return (
            f"Project Name: {self.project_name}\n"
            f"Packages: {', '.join(self.packages)}\n"
            f"Description: {self.description}"
        )