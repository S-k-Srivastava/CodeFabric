
import logging

from modules.core.graphs.requirements_gatherer import RequirementsGatherer
logger = logging.getLogger(__name__)


class NodejsRequirementsGatherer(RequirementsGatherer):
    def __init__(
            self,
            process_id:str
        ):
        super().__init__(process_id=process_id)

    async def arun(self):
        await super().arun()