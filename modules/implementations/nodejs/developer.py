from modules.agent_blueprints.graphs.developer import Developer
from modules.enums.technologies import Technologies
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.prompts.my_prompt_templates import MyPromptTemplates
from modules.types.common.models.requirements import Requirements
from modules.utils.commands import NodeJsCommands
from modules.llms.llms import google_with_temperature

class NodeJsDeveloper(Developer):
    def __init__(
            self, 
            id:str,
            requirements:Requirements,
            team_memory:SharedPKLMemory,
            llm_with_temperature=google_with_temperature,
            max_recursion_allowed=1000
        ):

        # Nodejs Specifics
        technology=Technologies.NODEJS
        prompts = MyPromptTemplates(technology)
        nodejs_commands = NodeJsCommands()

        super().__init__(
            id=id,
            requirements=requirements,
            prompts=prompts,
            tech_specific_commands=nodejs_commands,
            llm_with_temperature=llm_with_temperature,
            max_recursion_allowed=max_recursion_allowed,
            team_memory=team_memory
        )