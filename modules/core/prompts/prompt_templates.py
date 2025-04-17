import importlib
from typing import Tuple,Type
from modules.core.enums.prompt_types import PromptTypes,BasePromptTypes

class PromptTemplates:
    def __init__(self,module_path:str,prompt_enum:Type[BasePromptTypes]=PromptTypes):
        """
        module_path: path to the module containing the prompt templates
        prompt_enum: enum containing the prompt types (note : The file names of the prompt templates should be the same as the enum values)

        Example:
        module_path = "modules.implementations.nodejs.prompts"
        prompt_enum = PromptTypes
        
        So each file in module_path should have the name = value of each enum, like generate_file.py
        Each file will have 2 variables -> system_prompt and user_prompt.
        
        This can be extended for different technologies and prompt types
        See implented examples in modules/implementations/nodejs/prompts
        """
        self.PROMPT_TEMPLATES = {}
        self.module_path = module_path
        self.prompt_enum = prompt_enum
        self._initialize_prompt_templates()
        
    def _initialize_prompt_templates(self):
        """
        Dynamically imports the prompt templates and stores them in the PROMPT_TEMPLATES dictionary
        """
        for prompt_type in self.prompt_enum:
            prompt_module = importlib.import_module(f"{self.module_path}.{prompt_type.value}")
            self.PROMPT_TEMPLATES[prompt_type.value] = (prompt_module.system_prompt,prompt_module.user_prompt)

    def get_prompt(self,prompt_type) -> Tuple[str,str]:
        """
        Checks if the prompt type exists and returns the prompt
        """
        if not isinstance(prompt_type, self.prompt_enum):
            raise ValueError(f"Prompt type {prompt_type.name} doesn't exist.")
        
        if prompt_type.value in self.PROMPT_TEMPLATES:
            return self.PROMPT_TEMPLATES[prompt_type.value]
        else:
            raise ValueError(f"Prompt doesn't exist for {prompt_type.name}.")