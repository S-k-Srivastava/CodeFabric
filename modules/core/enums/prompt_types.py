from enum import Enum

class BasePromptTypes(Enum):
    """
    Base Enums for prompt types
    """
    pass

class PromptTypes(BasePromptTypes):
    """
    Enums for prompt types
    """
    GENERATE_PROJECT_STRUCTURE = "generate_project_structure"
    DECIDE_PACKAGES = "decide_packages"
    GENERATE_FILE = "generate_file" 