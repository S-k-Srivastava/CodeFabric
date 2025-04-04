from modules.agents.graphs.developer import Developer
from modules.enums.technologies import Technologies
from modules.prompts.my_prompt_templates import MyPromptTemplates
from modules.rag.rag_helper import RagHelper
from modules.utils.commands import NodeJsCommands
from modules.llms.default_llm import default_llm_with_temperature

class NodeJsBackendDeveloper(Developer):
    def __init__(self, project_name:str, project_description:str):

        technology=Technologies.NODEJS_BACKEND
        prompts = MyPromptTemplates(technology)
        nodejs_commands = NodeJsCommands()
        vector_store = RagHelper.get_vector_store()

        super().__init__(
            project_name=project_name,
            project_description=project_description,
            prompts=prompts,
            tech_specific_commands=nodejs_commands,
            vector_store=vector_store,
            llm_with_temperature=default_llm_with_temperature,
            max_recursion_allowed=1000,
            num_rag_results_allowed=8
        )