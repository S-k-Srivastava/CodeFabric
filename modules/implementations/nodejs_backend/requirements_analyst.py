from modules.agent_blueprints.graphs.requirements_analyst import REQUIREMENTS_ANALYST_MEMORY_KEY, RequirementsAnalyst
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.types.common.models.requirements import Requirements
import logging
logger = logging.getLogger(__name__)


class NodejsBackendRequirementsAnalyst(RequirementsAnalyst):
    def __init__(
            self,
            process_id:str,
            team_memory:SharedPKLMemory    
        ):
        super().__init__()
        self.process_id = process_id
        self.memory = team_memory.get_memory(REQUIREMENTS_ANALYST_MEMORY_KEY)

    async def arun(self):
        if self.memory.get('requirements') is None:

            requirements = Requirements(
                project_name="",
                description="project_description",
                packages=[]
            )

            self.memory.add('requirements',requirements)
        else:
            logger.info("🚀 Requirements are already gathered...")