from modules.agents.states.base_state import BaseState
from modules.types.common.models.files import File
from modules.types.common.models.requirements import Requirements

class ProjectState(BaseState):
    id : str
    requirements: Requirements
    files: list[File]
    current_file_index : int