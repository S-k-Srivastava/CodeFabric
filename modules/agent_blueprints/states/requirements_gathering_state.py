from modules.agent_blueprints.states.base_state import BaseState
from modules.types.common.models.requirements import Requirements


class DeveloperState(BaseState):
    requirements: Requirements