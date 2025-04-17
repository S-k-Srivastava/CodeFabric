from modules.core.types.llm_with_temperature import LLM_WITH_TEMPRATURE

class Team:
    def __init__(self,process_id:str,llm:LLM_WITH_TEMPRATURE):
        """
        Create a custom team of required agents by extending this class
        """
        self.process_id = process_id
        self.llm = llm

    def start_working(self):
        pass