from enum import Enum

class PromptTypes(Enum):
    GENERATE_FILE = "generate_file" 
    GENERATE_PROJECT_STRUCTURE = "generate_project_structure"
    DECIDE_PACKAGES = "decide_packages"