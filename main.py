from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.utils.memory_watcher import MemoryWatcher
from modules.utils.memory_based_input_handler import INPUT_MEMORY_KEY,INPUT_REQUESTS_KEY,INPUT_RESPONSES_KEY

process_id = "1054e58c-0d23-4b95-9a48-1d6b3b0bbcb8"
memory = SharedPKLMemory(process_id
                         ) 
def handle_memory_change():
    memory = SharedPKLMemory(process_id) 
    input_memory = memory.get_memory(INPUT_MEMORY_KEY)
    if input_memory.get(INPUT_REQUESTS_KEY) is not None:

        print("Input requests are available")

        input_responses = []
        for input_req in input_memory.get(INPUT_REQUESTS_KEY):
            in_res = input(input_req.title)
            input_responses.append(in_res)

        input_memory.add(INPUT_RESPONSES_KEY,input_responses)
        input_memory.delete(INPUT_REQUESTS_KEY)
        
watcher = MemoryWatcher(memory.file_path,on_change=handle_memory_change)
watcher.watch()