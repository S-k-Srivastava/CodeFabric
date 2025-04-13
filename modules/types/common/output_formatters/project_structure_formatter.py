from pydantic import BaseModel, Field
from modules.types.common.models.files import File
class FileFormatter(BaseModel):
    file_name: str = Field(...,description="full file name including proper extension")
    file_path : str = Field(...,description="relative path of the file including file name and extension")
    technical_specifications : list[str] = Field(...,description="List of technical specifications for the given file,including functions to be created with their inputs and return value or any other features.")
    dependencies : list[str] = Field(...,description="list of `path` of dependencies for the given file")

    def __str__(self):
        return (
            f"Name: {self.file_name}\n"
            f"Path: {self.file_path}\n"
            f"Dependencies: {', '.join(self.dependencies)}\n"
            f"Technical Specifications: {self.technical_specifications}"
        )
    
    def to_file(self)->File:
        return File(
            name=self.file_name,
            path=self.file_path,
            technical_specifications='\n'.join(f"{i + 1}. {self.technical_specifications[i]}" for i in range(len(self.technical_specifications))),
            dependencies=self.dependencies,
            is_generated=False,
            code=""
        )

class ProjectStructureFormatter(BaseModel):
    files: list[FileFormatter] = Field(...,description="list of all the files to be generated for the given project")

    def to_files(self)->list[File]:
        return [file.to_file() for file in self.files]