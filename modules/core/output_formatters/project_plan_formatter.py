from pydantic import BaseModel, Field
from modules.core.models.files import File

class FileFormatter(BaseModel):
    """
    This is a pyndantic model for the structured output for listing files,
    This can be extended and overridden to add custom fields for language specific stuffs.
    """
    file_name: str = Field(...,description="full file name including proper extension")
    file_path : str = Field(...,description="relative path of the file including file name and extension")
    description : str = Field(...,description="detailed technical specifications/purposes/descriptions of the given file, which will be used to generate the file")
    dependencies : list[str] = Field(...,description="list of `path` of other dependencies files (only user generated not the libraries) for the given file")

    def __str__(self):
        return (
            f"Name: {self.file_name}\n"
            f"Path: {self.file_path}\n"
            f"Dependencies: {', '.join(self.dependencies)}\n"
            f"Description: {self.description}"
        )
    
    def to_file(self)->File:
        """
        Converts FileFormatter to File with some extra feilds to be used in the workflow
        """
        return File(
            name=self.file_name,
            path=self.file_path,
            description=self.description,
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