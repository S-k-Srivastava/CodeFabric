import json
import logging
from modules.core.enums.stages import Stages
from modules.core.models.requirements import Requirements
from modules.core.persistence.my_redis_memory import MyRedisMemory,InputHanlder,Input
from modules.core.states.requirements_gathering_state import RequirementsGatheringState
from langgraph.graph import StateGraph,START,END

logger = logging.getLogger(__name__)

class RequirementsGatherer:
    def __init__(
            self,
            process_id:str
        ):
        self.process_id = process_id

        self.memory = MyRedisMemory(process_id=self.process_id).get_memory(Stages.REQUIREMENTS_GATHERING)

        # Initital State - Load from memory if exists
        logger.info(self.memory.get('current_node'))
        if self.memory.get('current_node') is not None:
            logger.info("🧠 Using past memory...")
            self.initial_node = self.memory.get('current_node')
            self.initial_state : RequirementsGatheringState = self.memory.get('current_state')
        else:
            self.initial_node = START
            self.initial_state = RequirementsGatheringState(
                requirements = Requirements(
                    project_name="",
                    description="",
                    packages=[]
                )
            )

        # Build Graph
        self.graph = self._build_graph()

        logger.info("🚀 Requirements Gathering process started! ID: %s", process_id)

    def _build_graph(self):

        logger.info("🚀 Building Graph...")

        graph_builder = StateGraph(RequirementsGatheringState)

        graph_builder.add_node('get_requirements',self.get_requirements)

        # Decide Start Node
        def decide_start_node(_: RequirementsGatheringState):
            if self.initial_node == START:
                return 'get_requirements'
            else:
                return self.initial_node
            
        graph_builder.add_conditional_edges(
            START,
            decide_start_node
        )

        graph_builder.add_edge('get_requirements',END)

        graph = graph_builder.compile()

        return graph
        
    async def arun(self):
        async for event in self.graph.astream(self.initial_state):
            current_node = list(event.keys())[0]
            current_state = event[current_node]
            self.memory.add('current_state',current_state)
            self.memory.add('current_node',current_node)
            logger.info(f"🧠 Saving memory for current node: {current_node}\n\n")
        
        self.memory.add('current_node',END)

        logger.info("🚀 Requirements Gathering process completed! ID: %s", self.process_id)

    def get_requirements(self,state:RequirementsGatheringState):
        logger.info("🚀 Gathering requirements...")

        project_name_req= Input(
            title="Project Name",
            description="Enter the name of your project",
            multiline=False
        )
        description_req = Input(
            title="Description",
            description="Enter a detailed description of your project",
            multiline=True
        )

        inputhandler = InputHanlder(process_id=self.process_id)
        responses = inputhandler.request_input([project_name_req,description_req])

        requirements = Requirements(
            project_name=responses[0],
            description=responses[1],
            packages=[]
        )

        self.memory.add('requirements',requirements)

        state['requirements'] = requirements

        return state
