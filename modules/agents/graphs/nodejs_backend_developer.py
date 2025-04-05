from modules.agents.graphs.developer import Developer
from modules.agents.memory.developer_memory import DeveloperMemory
from modules.enums.technologies import Technologies
from modules.prompts.my_prompt_templates import MyPromptTemplates
from modules.utils.commands import NodeJsCommands
from modules.llms.default_llm import default_llm_with_temperature
from uuid import uuid4

class NodeJsBackendDeveloper(Developer):
    def __init__(
            self, 
            id:str,
            project_name:str, 
            project_description:str,
            llm_with_temperature=default_llm_with_temperature,
            max_recursion_allowed=1000,
            memory:DeveloperMemory = None,
            persist_memory:bool=True,
        ):

        # Nodejs Specifics
        technology=Technologies.NODEJS_BACKEND
        prompts = MyPromptTemplates(technology)
        nodejs_commands = NodeJsCommands()

        super().__init__(
            id=id,
            project_name=project_name,
            project_description=project_description,
            prompts=prompts,
            tech_specific_commands=nodejs_commands,
            llm_with_temperature=llm_with_temperature,
            max_recursion_allowed=max_recursion_allowed,
            memory=memory,
            persist_memory=persist_memory
        )