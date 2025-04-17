from pydantic import BaseModel, Field
from modules.core.models.files import File

class FileFormatter(BaseModel):
    """
    This is a pyndantic model for the structured output for listing files,
    This can be extended and overridden to add custom fields for language specific stuffs.
    """
    file_name: str = Field(...,description="file name including proper extension(example- server.js)")
    file_path : str = Field(...,description="relative `path` (with respect to the root) of the file including file name and extension")
    technical_specifications : list[str] = Field(...,description="technical specifications")
    dependencies : list[str] = Field(...,description="list of `path` of other dependencies files(only internal dependencies,not the packages)")

    def __str__(self):
        return (
            f"Name: {self.file_name}\n"
            f"Path: {self.file_path}\n"
            f"Dependencies: {', '.join(self.dependencies)}\n"
            f"Technical Specifications: {"\n".join(self.technical_specifications)}"
        )
    
    def to_file(self)->File:
        """
        Converts FileFormatter to File with some extra feilds to be used in the workflow
        """
        return File(
            name=self.file_name,
            path=self.file_path,
            technical_specifications="\n".join(self.technical_specifications),
            dependencies=self.dependencies,
            is_generated=False,
            code=""
        )

class ProjectPlanFormatter(BaseModel):
    """
    List of FileFormatter
    """
    files: list[FileFormatter] = Field(...,description="list of all the files to be generated for the given project")

    def to_files(self)->list[File]:
        """
        Converts list of FileFormatter to list of File
        """
        return [file.to_file() for file in self.files]