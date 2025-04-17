from modules.core.graphs.developer import Developer
from modules.core.models.requirements import Requirements
from modules.core.persistence.shared_pkl_memory import SharedPKLMemory
from modules.core.types.llm_with_temperature import LLM_WITH_TEMPRATURE
from modules.implementations.nodejs.commands.commands import NodeJsCommands
from modules.implementations.nodejs.prompts.prompt_templates import NodeJsPromptTemplates

class NodeJsDeveloper(Developer):
    def __init__(
            self, 
            process_id:str,
            requirements:Requirements,
            team_memory:SharedPKLMemory,
            llm=LLM_WITH_TEMPRATURE,
            max_recursion_allowed=1000
        ):

        # Nodejs Specifics
        prompts = NodeJsPromptTemplates()
        nodejs_commands = NodeJsCommands()

        super().__init__(
            process_id=process_id,
            requirements=requirements,
            prompts=prompts,
            tech_specific_commands=nodejs_commands,
            llm=llm,
            max_recursion_allowed=max_recursion_allowed,
            team_memory=team_memory
        )