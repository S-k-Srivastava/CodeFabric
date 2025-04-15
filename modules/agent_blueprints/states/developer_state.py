from modules.agent_blueprints.states.base_state import BaseState
from modules.types.common.models.files import File
from modules.types.common.models.requirements import Requirements

class DeveloperState(BaseState):
    id : str
    requirements: Requirements
    files: list[File]
    current_file_index : int
    cwd : str