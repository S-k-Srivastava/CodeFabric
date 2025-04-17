from modules.core.enums.technologies import Technologies
from modules.core.prompts.prompt_templates import PromptTemplates

class NodeJsPromptTemplates(PromptTemplates):
    def __init__(self):
        super().__init__(f"modules.implementations.{Technologies.NODEJS.value}.prompts")