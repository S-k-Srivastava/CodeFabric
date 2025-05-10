from pydantic import BaseModel, Field

from modules.types.models import FileInfo

class PackagesFormatter(BaseModel):
    packages: list[str] = Field(...,description="List of exact packages names to install.")

    @property
    def to_model(self) -> list[str]:
        return self.packages
    
class FileInfoFormatter(BaseModel):
    name: str = Field(...,description="File Name with extension. Example : server.js")
    path : str = Field(...,description="Path to file from the project root. Example : /path/to/server.js")
    dependencies : list[str] = Field(...,description="List of other file dependencies `path` for the file. Example : ['/path/to/server.js']")
    technical_blueprint : str = Field(...,description="Technical BluePrint and Outline for the file.")

    @property
    def to_model(self) -> FileInfo:
        return FileInfo(
            name=self.name,
            path=self.path,
            dependencies=self.dependencies,
            technical_specifications=self.technical_blueprint,
            is_generated=False,
            code=None
        )

class FileInfosFormatter(BaseModel):
    files : list[FileInfoFormatter] = Field(...,description="List of file infos.")

    @property
    def to_model(self) -> list[FileInfo]:
        return [file.to_model for file in self.files]