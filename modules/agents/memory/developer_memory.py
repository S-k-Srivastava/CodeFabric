import logging
from modules.agents.states.developer_state import DeveloperState
from modules.persistence.pickle_memory import PickleMemory
from langchain_community.vectorstores.chroma import Chroma
from langchain.docstore.document import Document
from modules.rag.rag_helper import RagHelper
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
        state:DeveloperState,
        current_node:str,
        vector_store:Chroma,
    ):
        self._add_graph_state(state)
        self._add_current_node(current_node)
        self._add_vector_store(vector_store)
        self.memory.save_as_pkl()

    def load_from_disk(self) -> bool:
        try:
            self.memory = PickleMemory.load_from_pkl(self._id)
            return True
        except FileNotFoundError as e:
            return False

    def _add_graph_state(self,state:DeveloperState):
        self.memory.add('graph_state',state)
    
    def _add_current_node(self,node:str):
        self.memory.add('current_node',node)
    
    def _add_vector_store(self,vector_store:Chroma):
        data = vector_store.get(include=['documents','metadatas'])
        vector_docs = {
            'documents':data['documents'],
            'metadatas':data['metadatas']
        }
        self.memory.add('vector_docs',vector_docs)

    @property
    def graph_state(self) -> DeveloperState:
        return self.memory.get('graph_state')
    
    @property
    def current_node(self) -> str:
        return self.memory.get('current_node')
    
    @property
    def vector_store(self) -> Chroma:
        vector_docs = self.memory.get('vector_docs')
        vector_store = RagHelper.get_vector_store()

        length = len(vector_docs['documents'])
        docs = []
        for i in range(length):
            doc = Document(page_content=vector_docs['documents'][i],metadata=vector_docs['metadatas'][i])
            docs.append(doc)
        
        if len(docs) > 0:
            vector_store.add_documents(docs)
        
        return vector_store
