
from pydantic import BaseModel
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.utils.memory_watcher import MemoryWatcher

INPUT_MEMORY_KEY = "inputs"
INPUT_REQUESTS_KEY = "input_requests"
INPUT_RESPONSES_KEY = "input_responses"

class Input(BaseModel):
    title: str
    description: str
    multiline: bool

class MemoryBasedInputHanlder:
    def __init__(self,process_id:str):
        self.process_id = process_id
    
    def handle_memory_change(self):
        memory = SharedPKLMemory(self.process_id)
        responses =  memory.get_memory(INPUT_MEMORY_KEY).get(INPUT_RESPONSES_KEY)
        if responses is not None and self.watcher is not None:
            self.watcher.stop()
            self.responses = responses
    
    def request_inputs(self, inputs:list[Input]):
        memory = SharedPKLMemory(self.process_id)
        memory.get_memory(INPUT_MEMORY_KEY).add(INPUT_REQUESTS_KEY,inputs)

        file_path = memory.file_path

        self.watcher = MemoryWatcher(file_path,on_change=self.handle_memory_change)

        self.watcher.watch()

        return self.responses
    
    def stop(self):
        if self.watcher is not None:
            self.watcher.stop()