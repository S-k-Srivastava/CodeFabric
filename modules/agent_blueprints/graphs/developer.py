import logging
import os
from pathlib import Path
from typing import Callable
from modules.agent_blueprints.states.developer_state import DeveloperState
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.prompts.my_prompt_templates import MyPromptTemplates
from modules.enums.prompt_types import PromptTypes
from modules.types.common.output_formatters.packages_formatter import PackagesFormatter
from modules.types.common.output_formatters.project_structure_formatter import ProjectStructureFormatter
from modules.types.common.models.requirements import Requirements
from langchain.output_parsers import PydanticOutputParser
from modules.utils.command_runner import run_commands
from modules.utils.file_helper import FileHelper
from modules.utils.commands import TechSpecificCommands,VsCodeCommands
from modules.utils.io_helper import IOHelper
from langgraph.graph import StateGraph, START, END
from langchain.chat_models.base import BaseChatModel
from langchain.schema import HumanMessage,SystemMessage
from modules.enums.stages import Stages

BASE_DIR = Path(__file__).parent.parent.parent.parent / "projects/"

logger = logging.getLogger(__name__)

LLM_WITH_TEMPRATURE = Callable[[float], BaseChatModel]

class Developer:
    def __init__(
            self, 
            id:str,
            requirements:Requirements,
            prompts:MyPromptTemplates,
            tech_specific_commands:TechSpecificCommands,
            llm_with_temperature:LLM_WITH_TEMPRATURE,
            team_memory:SharedPKLMemory,
            max_recursion_allowed:int=120,
        ):

        # Tech Specific Stuff
        self.prompts = prompts
        self.tech_specific_commands = tech_specific_commands

        # Performance Related Stuff
        self.llm_with_temperature = llm_with_temperature
        self.max_recursion_allowed = max_recursion_allowed

        # Current Working Directory
        self.cwd = os.path.join(BASE_DIR, requirements.project_name)
        os.makedirs(self.cwd, exist_ok=True)
        run_commands([VsCodeCommands.open_vscode()],cwd=self.cwd)

        # Initital State - Load from memory if exists
        self.memory = team_memory.get_memory(Stages.PROJECT_DEVELOPMENT)
        if self.memory.get('current_node') is not None:
            logger.info("🧠 Using past memory...")
            self.initial_node = self.memory.get('current_node')
            self.initital_state = self.memory.get('graph_state')
        else:
            logger.info("🧠 Starting a fresh process with new memory...")
            self.initial_node = START
            self.initital_state = DeveloperState(
                id=id,
                requirements=requirements,
                files=[],
                current_file_index=-1,
                cwd=self.cwd
            )

        # Graph
        self.graph =  self._build_graph()

        logger.info("🚀 Process started! ID: %s", id)

    def _build_graph(self):

        logger.info("🚀 Building Graph...")

        graph_builder = StateGraph(DeveloperState)

        graph_builder.add_node('decide_packages',self.decide_packages)
        graph_builder.add_node('create_base_project',self.create_base_project)
        graph_builder.add_node('create_project_structure',self.create_project_structure)
        graph_builder.add_node('sort_files_by_dependency',self.sort_files_by_dependency)
        graph_builder.add_node('pick_a_file',self.pick_a_file)
        graph_builder.add_node('generate_and_write_code',self.generate_and_write_code)
        graph_builder.add_node('install_packages',self.install_packages)

        
        # Decide Start Node
        def decide_start_node(_: DeveloperState):
            if self.initial_node == START:
                return 'create_base_project'
            else:
                return self.initial_node
            
        # END Condition
        def should_generate_next(state: DeveloperState):
            if state['current_file_index'] == -1:
                logger.info("🚀 Process completed! ID: %s", state['id'])
                return END
            else:
                return 'generate_and_write_code'

        # Edges
        graph_builder.add_conditional_edges(
            source=START,
            path=decide_start_node
        )
        graph_builder.add_edge('create_base_project','decide_packages')
        graph_builder.add_edge('decide_packages','install_packages')
        graph_builder.add_edge('install_packages','create_project_structure')
        graph_builder.add_edge('create_project_structure','sort_files_by_dependency')
        graph_builder.add_edge('sort_files_by_dependency','pick_a_file')
        graph_builder.add_conditional_edges(
            source='pick_a_file',
            path=should_generate_next
        )
        graph_builder.add_edge('generate_and_write_code','pick_a_file')

        graph = graph_builder.compile()

        return graph
    
    async def arun(self):
        async for event in self.graph.astream(self.initital_state,config={"recursion_limit": self.max_recursion_allowed}):
            current_node = list(event.keys())[0]
            current_state = event[current_node]
            self.memory.add('graph_state',current_state)
            self.memory.add('current_node',current_node)
            logger.info(f"🧠 Saving memory for current node: {current_node}\n\n")

    def create_base_project(self,state:DeveloperState):

        logger.info("🚀 Initializing Base Project... (Running template setup)")

        cmd_result = run_commands([self.tech_specific_commands.project_setup_command()],cwd=self.cwd)[0]

        if not cmd_result.is_success:
            raise Exception(cmd_result.error)

        logger.info("🚀 Base Project Initialized!")

        return state
    
    def decide_packages(self,state:DeveloperState):

        logger.info("🚀 Deciding packages...")

        system_prompt,user_prompt = self.prompts.get_prompt(PromptTypes.DECIDE_PACKAGES)
        packages_parser = PydanticOutputParser(pydantic_object=PackagesFormatter)
        user_prompt = user_prompt.format(
            project_description=state['requirements'].description,
            project_name=state['requirements'].project_name
        )
        system_prompt = system_prompt.format(
            format=packages_parser.get_format_instructions()
        )

        messages = [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ]
        response = self.llm_with_temperature(0).invoke(messages).content

        packages = packages_parser.parse(response)

        state['requirements'].packages = packages.packages

        return state 
    
    def install_packages(self,state:DeveloperState):

        packages = state['requirements'].packages

        logger.info(f"📦 Installing Packages: {packages}...")

        cmd_result = run_commands([self.tech_specific_commands.package_install_command(packages)],cwd=self.cwd)[0]

        if not cmd_result.is_success:
            raise Exception(cmd_result.error)

        logger.info("📦 Packages Installed!")

        return state
    
    def create_project_structure(self,state:DeveloperState):
        """
        Can be overridden later for creating project structure with any custom logic depending on technology.
        """
        
        logger.info("📂 Creating Project Structure...")

        system_prompt,user_prompt = self.prompts.get_prompt(PromptTypes.GENERATE_PROJECT_STRUCTURE)
        project_structure_parser = PydanticOutputParser(pydantic_object=ProjectStructureFormatter)
        user_prompt = user_prompt.format(
            project_description=state['requirements'].description,
            packages=','.join(state['requirements'].packages)
        )
        system_prompt = system_prompt.format(
            format=project_structure_parser.get_format_instructions()
        )

        messages = [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ]
        response = self.llm_with_temperature(0.6).invoke(messages).content

        file_list = project_structure_parser.parse(response).to_files()

        state['files'] = file_list

        state['current_file_index'] = 0

        logger.info(f"📄 Total files to be generated: {len(file_list)}")

        return state
    
    def sort_files_by_dependency(self,state:DeveloperState):
        """
        Can be overridden later for sorting files with any custom logic depending on technology.
        """

        logger.info("📦 Sorting files based on dependencies...")

        return state
    
    def pick_a_file(self,state:DeveloperState):

        logger.info("📂 Picking up the file for generation...")

        picked_file_index = FileHelper.get_next_unprocessed_file_index(state['files'])

        state['current_file_index'] = picked_file_index

        return state
    
    def generate_and_write_code(self,state:DeveloperState):        
        current_file = state['files'][state['current_file_index']]

        logger.info(f"🛠️  Generating code for {current_file.name}...")

        system_prompt,user_prompt = self.prompts.get_prompt(PromptTypes.GENERATE_FILE)

        context = "No dependencies needed for this file"
        
        if len(current_file.dependencies) > 0:
            for dependency in current_file.dependencies:
                file = next((f for f in state['files'] if f.path == dependency), None)
                if file is not None:
                    context += f"****File Name : {file.name}****\n****File Path : {file.path}****\nContent:\n{file.code}\n\n--------------\n\n"
                else:
                    logger.info(f"📂 File not found: {dependency}")

        user_prompt = user_prompt.format(
            packages= ','.join(state['requirements'].packages),
            file=current_file.name,
            technical_specifications=current_file.technical_specifications,
            path=current_file.path,
            project_description=state['requirements'].description,
            context=context
        )

        messages = [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ]

        streamer = self.llm_with_temperature(0).stream(messages)

        code = IOHelper.stream_code_to_file(streamer, cwd=self.cwd,filepath=current_file.path)

        logger.info(f"📂 Related files for {current_file.path} --> [{','.join(current_file.dependencies)}]")

        state['files'][state['current_file_index']].is_generated = True

        logger.info("📖 Adding to contexts...")

        state['files'][state['current_file_index']].code = code
        
        return state
    
