import logging
from modules.core.enums.stages import Stages
from modules.core.persistence.shared_pkl_memory import SharedPKLMemory
from modules.core.team.team import Team
from modules.core.types.llm_with_temperature import LLM_WITH_TEMPRATURE
from modules.implementations.nodejs.graphs.developer import NodeJsDeveloper
from modules.implementations.nodejs.graphs.requirements_gatherer import NodejsRequirementsGatherer
logger = logging.getLogger(__name__)

class NodeJsTeam(Team):
    def __init__(self,process_id:str,llm:LLM_WITH_TEMPRATURE):
        super().__init__(process_id=process_id,llm=llm)
        logger.info("🚀 Team is ready to build your Node.js backend project...")
        logger.info(f"🚀 Process ID: {self.process_id}")
        self.team_memory = SharedPKLMemory(id=self.process_id)
        logger.info("🚀 Team memory initialized...")

    async def start_working(self):

        requirement_analyst = NodejsRequirementsGatherer(
            process_id=self.process_id,
            team_memory=self.team_memory,
        )
        await requirement_analyst.arun()

        requirements = self.team_memory.get_memory(Stages.REQUIREMENTS_GATHERING).get('graph_state')['requirements']

        developer = NodeJsDeveloper(
            process_id=self.process_id,
            requirements=requirements,
            llm=self.llm,
            team_memory=self.team_memory
        )

        await developer.arun()