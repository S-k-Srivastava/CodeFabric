from modules.agent_blueprints.team.team import Team
import logging
from modules.implementations.nodejs.developer import NodeJsDeveloper
from modules.implementations.nodejs.requirements_gatherer import NodejsRequirementsGatherer
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.llms.llms import deep_infra_with_temperature
from modules.enums.stages import Stages
logger = logging.getLogger(__name__)

class NodeJsTeam(Team):
    def __init__(self,process_id:str,prefered_llm=deep_infra_with_temperature):
        super().__init__()
        logger.info("🚀 Team is ready to build your Node.js backend project...")
        self.prefered_llm = prefered_llm
        self.process_id = process_id
        logger.info(f"🚀 Process ID: {self.process_id}")
        self.team_memory = SharedPKLMemory(id=self.process_id)
        logger.info("🚀 Team memory initialized...")

    async def start_working(self):

        requirement_analyst = NodejsRequirementsGatherer(
            process_id=self.process_id,
            team_memory=self.team_memory,
        )
        await requirement_analyst.arun()

        requirements = self.team_memory.get_memory(Stages.REQUIREMENTS_GATHERING).get('requirements')

        developer = NodeJsDeveloper(
            id=self.process_id,
            requirements=requirements,
            llm_with_temperature=self.prefered_llm,
            team_memory=self.team_memory
        )

        await developer.arun()