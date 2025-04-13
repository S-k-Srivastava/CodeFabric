import importlib
from typing import Tuple
from modules.enums.prompt_types import PromptTypes
from modules.enums.technologies import Technologies

class MyPromptTemplates:
    def __init__(self,technology:Technologies):
        self.PROMPT_TEMPLATES = {}

        module_path = f"modules.prompts.{technology.value}"
        for prompt_type in PromptTypes:
            prompt_module = importlib.import_module(f"{module_path}.{prompt_type.value}")
            self.PROMPT_TEMPLATES[prompt_type.value] = (prompt_module.system_prompt,prompt_module.user_prompt)

    def get_prompt(self,prompt_type:PromptTypes) -> Tuple[str,str]:
        if prompt_type.value in self.PROMPT_TEMPLATES:
            return self.PROMPT_TEMPLATES[prompt_type.value]
        else:
            raise ValueError(f"Prompt doesn't exist for {prompt_type.name}.")