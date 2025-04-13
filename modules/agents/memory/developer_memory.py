import logging
from modules.agents.states.project_state import ProjectState
from modules.persistence.pickle_memory import PickleMemory
logger = logging.getLogger(__name__)

class DeveloperMemory:
    def __init__(self, id: str,override_past_memory:bool=False):
        self._id = id
        self.have_past_memory = self.load_from_disk()

        if not self.have_past_memory or override_past_memory:
            if self.have_past_memory:
                PickleMemory.delete_pkl(id)
            self.memory = PickleMemory(id)
            logger.info("🧠 Developer memory initialized.")
        elif self.have_past_memory:
            logger.info("🧠 Developer has past memory loaded.")
    
    def save_memory(
        self,
        state:ProjectState,
        current_node:str,
    ):
        self._add_graph_state(state)
        self._add_current_node(current_node)
        self.memory.save_as_pkl()

    def load_from_disk(self) -> bool:
        try:
            self.memory = PickleMemory.load_from_pkl(self._id)
            return True
        except FileNotFoundError as e:
            return False

    def _add_graph_state(self,state:ProjectState):
        self.memory.add('graph_state',state)
    
    def _add_current_node(self,node:str):
        self.memory.add('current_node',node)
    
    @property
    def graph_state(self) -> ProjectState:
        return self.memory.get('graph_state')
    
    @property
    def current_node(self) -> str:
        return self.memory.get('current_node')
