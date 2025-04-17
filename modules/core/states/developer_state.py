from modules.core.models.files import File
from modules.core.models.requirements import Requirements
from modules.core.states.base_state import BaseState

class DeveloperState(BaseState):
    id : str
    requirements: Requirements
    files: list[File]
    current_file_index : int
    cwd : str