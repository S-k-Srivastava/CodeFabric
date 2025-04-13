import logging
import os
from pathlib import Path
from typing import Callable
from modules.agents.memory.developer_memory import DeveloperMemory
from modules.agents.states.project_state import ProjectState
from modules.prompts.my_prompt_templates import MyPromptTemplates
from modules.enums.prompt_types import PromptTypes
from modules.llms.llms import deep_infra_with_temperature
from modules.rag.rag_helper import RagHelper
from modules.types.common.output_formatters.packages_formatter import PackagesFormatter
from modules.types.common.output_formatters.project_structure_formatter import ProjectStructureFormatter
from modules.types.common.models.requirements import Requirements
from langchain.output_parsers import PydanticOutputParser
from modules.utils.command_runner import run_commands
from modules.utils.file_helper import FileHelper
from modules.utils.commands import TechSpecificCommands,VsCodeCommands
from modules.utils.io_helper import IOHelper
from langchain.docstore.document import Document
from langgraph.graph import StateGraph, START, END
from langchain.vectorstores import VectorStore
from langchain.chat_models.base import BaseChatModel
from langchain.schema import HumanMessage,SystemMessage

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
            max_recursion_allowed:int=120,
            memory:DeveloperMemory = None,
            persist_memory:bool=False
        ):

        if persist_memory and memory is None:
            raise ValueError("Memory cannot be None if persist_memory is True")

        # User Inputs
        self.persist_memory = persist_memory

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
        self.memory = memory
        if memory is not None and memory.have_past_memory:
            logger.info("🧠 Using past memory...")
            self.initial_node = memory.current_node
            self.initital_state = memory.graph_state
            self.vector_store = memory.vector_store
        else:
            logger.info("🧠 Starting a fresh process with new memory...")
            self.initial_node = START
            self.initital_state = ProjectState(
                id=id,
                requirements=requirements,
                files=[],
                current_file_index=-1,
            )
            self.vector_store = RagHelper.get_vector_store()

        # Graph
        self.graph =  self._build_graph()

        logger.info("🚀 Process started! ID: %s", id)

    def _build_graph(self):

        logger.info("🚀 Building Graph...")

        graph_builder = StateGraph(ProjectState)

        graph_builder.add_node('decide_packages',self.decide_packages)
        graph_builder.add_node('create_base_project',self.create_base_project)
        graph_builder.add_node('create_project_structure',self.create_project_structure)
        graph_builder.add_node('sort_files_by_dependency',self.sort_files_by_dependency)
        graph_builder.add_node('pick_a_file',self.pick_a_file)
        graph_builder.add_node('generate_and_write_code',self.generate_and_write_code)
        graph_builder.add_node('install_packages',self.install_packages)

        
        # Decide Start Node
        def decide_start_node(_: ProjectState):
            if self.initial_node == START:
                return 'create_base_project'
            else:
                return self.initial_node
            
        # END Condition
        def should_generate_next(state: ProjectState):
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
            if self.persist_memory:
                current_node = list(event.keys())[0]
                current_state = event[current_node]
                self.memory.save_memory(
                    state=current_state,
                    current_node=current_node,
                    vector_store=self.vector_store
                )
                logger.info(f"🧠 Saving memory for current node: {current_node}\n\n")

    def create_base_project(self,state:ProjectState):

        logger.info("🚀 Initializing Base Project... (Running template setup)")

        cmd_result = run_commands([self.tech_specific_commands.project_setup_command()],cwd=self.cwd)[0]

        if not cmd_result.is_success:
            raise Exception(cmd_result.error)

        logger.info("🚀 Base Project Initialized!")

        return state
    
    def decide_packages(self,state:ProjectState):

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
    
    def install_packages(self,state:ProjectState):

        packages = state['requirements'].packages

        logger.info(f"📦 Installing Packages: {packages}...")

        cmd_result = run_commands([self.tech_specific_commands.package_install_command(packages)],cwd=self.cwd)[0]

        if not cmd_result.is_success:
            raise Exception(cmd_result.error)

        logger.info("📦 Packages Installed!")

        return state
    
    def create_project_structure(self,state:ProjectState):
        """
        Can be overridden later for creating project structure with any custom logic depending on technology.
        """

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
    
    def sort_files_by_dependency(self,state:ProjectState):
        """
        Can be overridden later for sorting files with any custom logic depending on technology.
        """

        logger.info("📦 Sorting files based on dependencies...")

        return state
    
    def pick_a_file(self,state:ProjectState):

        logger.info("📂 Picking up the file for generation...")

        picked_file_index = FileHelper.get_next_unprocessed_file_index(state['files'])

        state['current_file_index'] = picked_file_index

        return state
    
    def generate_and_write_code(self,state:ProjectState):        
        current_file = state['files'][state['current_file_index']]

        logger.info(f"🛠️  Generating code for {current_file.name}...")

        system_prompt,user_prompt = self.prompts.get_prompt(PromptTypes.GENERATE_FILE)
        
        query = f"{current_file.dependencies}"

        if len(current_file.dependencies) > 0:
            context = self.vector_store.similarity_search(query,k=len(current_file.dependencies))
        else:
            context = []

        user_prompt = user_prompt.format(
            packages= ','.join(state['requirements'].packages),
            file=current_file.name,
            technical_specifications=current_file.technical_specifications,
            path=current_file.path,
            project_description=state['requirements'].description,
            context='\n\n'.join([doc.page_content for doc in context])
        )

        messages = [
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ]

        streamer = self.llm_with_temperature(0).stream(messages)

        code = IOHelper.stream_code_to_file(streamer, cwd=self.cwd,filepath=current_file.path)

        names = [doc.metadata['name'] for doc in context]

        logger.info(f"📂 Related files for {current_file.path} --> [{','.join(names)}]")

        state['files'][state['current_file_index']].is_generated = True

        logger.info("📖 Adding to contexts...")

        code_info = (
            f"File Name : {current_file.name}\n"
            f"File Path : {current_file.path}\n\n"
            f"Code : {code}\n\n"
        )
        self.vector_store.add_documents(
            documents=[
                Document(page_content=code_info,metadata={'name':current_file.name,'content_type':'code'})
            ]
        )
        return state
    
