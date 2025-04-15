from modules.enums.stages import Stages
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.types.common.models.requirements import Requirements
import logging
from modules.utils.memory_based_input_handler import MemoryBasedInputHanlder,Input

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
            
            inputs_required = [
                Input(
                    title="Project Name",
                    description="Enter the name of the project",
                    multiline=False
                ),
                Input(
                    title="Project Description",
                    description="Enter the description of the project",
                    multiline=True
                )
            ]
            
            input_handler = MemoryBasedInputHanlder(process_id=self.process_id)
            responses = input_handler.request_inputs(inputs_required)

            requirements = Requirements(
                project_name=responses[0],
                description=responses[1],
                packages=[]
            )

            self.memory.add('requirements',requirements)
        else:
            logger.info("🚀 Requirements are already gathered...")