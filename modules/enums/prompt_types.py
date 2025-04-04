from enum import Enum

class PromptTypes(Enum):
    GENERATE_FILE = "generate_file" 
    GENERATE_PROJECT_STRUCTURE = "generate_project_structure"
    SANITIZE_PROJECT_DESCRIPTION = "sanitize_project_description"