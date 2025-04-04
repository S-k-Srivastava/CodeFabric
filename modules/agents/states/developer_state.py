from modules.agents.states.base_state import BaseState
from modules.types.current_file import CurrentFile
from modules.types.project_structure import File
from modules.types.requirements import Requirements

class DeveloperState(BaseState):
    id : str
    requirements: Requirements
    files: list[File]
    current_file : CurrentFile