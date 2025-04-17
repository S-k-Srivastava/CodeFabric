
import logging

from modules.core.enums.stages import Stages
from modules.core.models.requirements import Requirements
from modules.core.persistence.shared_pkl_memory import SharedPKLMemory

logger = logging.getLogger(__name__)

class RequirementsGatherer:
    def __init__(
            self,
            process_id:str,
            team_memory:SharedPKLMemory
        ):
        self.process_id = process_id
        self.memory = team_memory.get_memory(Stages.REQUIREMENTS_GATHERING)

    async def arun(self):
        if self.memory.get('requirements') is None:

            logger.info("🚀 Gathering requirements...")

            project_name = input("Project Name: ")
            description = input("Description: ")

            requirements = Requirements(
                project_name=project_name,
                description=description,
                packages=[]
            )

            self.memory.add('requirements',requirements)
        else:
            logger.info("🚀 Requirements are already gathered...")