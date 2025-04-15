from modules.agent_blueprints.graphs.requirements_gatherer import RequirementsGatherer
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.types.common.models.requirements import Requirements
from modules.enums.stages import Stages
import logging
logger = logging.getLogger(__name__)


class NodejsRequirementsGatherer(RequirementsGatherer):
    def __init__(
            self,
            process_id:str,
            team_memory:SharedPKLMemory    
        ):
        super().__init__(process_id=process_id,team_memory=team_memory)

    async def arun(self):
        await super().arun()