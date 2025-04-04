import logging
import os
from pathlib import Path
import re
from typing import Callable
from modules.agents.states.developer_state import DeveloperState
from modules.prompts.my_prompt_templates import MyPromptTemplates
from modules.enums.prompt_types import PromptTypes
from modules.enums.technologies import Technologies
from modules.llms.default_llm import default_llm_with_temperature
from modules.rag.rag_helper import RagHelper
from modules.types.current_file import CurrentFile
from modules.types.project_structure import ProjectStructure
from modules.types.requirements import Requirements
from uuid import uuid4
from langchain.output_parsers import PydanticOutputParser
from modules.utils.command_runner import run_commands
from modules.utils.file_helper import FileHelper
from modules.utils.commands import TechSpecificCommands
from langchain.docstore.document import Document
from langgraph.graph import StateGraph, START, END
from langchain.vectorstores import VectorStore
from langchain.chat_models.base import BaseChatModel

BASE_DIR = Path(__file__).parent.parent.parent.parent / "projects/"

logger = logging.getLogger(__name__)

LLM_WITH_TEMPRATURE = Callable[[float], BaseChatModel]

class Developer:
    def __init__(
            self, 
            project_name:str,
            project_description:str,
            prompts:MyPromptTemplates,
            tech_specific_commands:TechSpecificCommands,
            vector_store:VectorStore,
            llm_with_temperature:LLM_WITH_TEMPRATURE = default_llm_with_temperature,
            num_rag_results_allowed:int=6,
            max_recursion_allowed:int=120,
        ):
        # User Inputs
        self.project_name = project_name
        self.project_description = project_description
        self.prompts = prompts
        self.tech_specific_commands = tech_specific_commands
        self.vector_store = vector_store
        self.llm_with_temperature = llm_with_temperature
        self.num_rag_results_allowed = num_rag_results_allowed
        self.max_recursion_allowed = max_recursion_allowed

        # Path
        self.cwd = os.path.join(BASE_DIR, project_name)
        os.makedirs(self.cwd, exist_ok=True)

        # Initital State
        id = str(uuid4())
        self.initital_state = DeveloperState(
            id=id,
            requirements=Requirements(project_name=project_name,description=project_description,packages=[]),
            files=[],
            current_file=CurrentFile(index=-1,code=None),
        )

        # Graph
        self.graph =  self._build_graph()

        logger.info("🚀 Process started! ID: %s", id)

    def _build_graph(self):

        logger.info("🚀 Building Graph...")

        graph_builder = StateGraph(DeveloperState)

        graph_builder.add_node('sanitize_project_description',self.sanitize_project_description)
        graph_builder.add_node('create_base_project',self.create_base_project)
        graph_builder.add_node('create_project_structure',self.create_project_structure)
        graph_builder.add_node('sort_files_by_dependency',self.sort_files_by_dependency)
        graph_builder.add_node('pick_a_file',self.pick_a_file)
        graph_builder.add_node('generate_code',self.generate_code)
        graph_builder.add_node('sanitize_code',self.sanitize_code)
        graph_builder.add_node('write_code_to_file',self.write_code_to_file)
        graph_builder.add_node('install_packages',self.install_packages)

        # END
        def should_generate_next(state: DeveloperState):
            if state['current_file'].index == -1:
                return END
            else:
                return 'generate_code'

        # Edges
        graph_builder.add_edge(START,'sanitize_project_description')
        graph_builder.add_edge('sanitize_project_description','create_base_project')
        graph_builder.add_edge('create_base_project','install_packages')
        graph_builder.add_edge('install_packages','create_project_structure')
        graph_builder.add_edge('create_project_structure','sort_files_by_dependency')
        graph_builder.add_edge('sort_files_by_dependency','pick_a_file')
        graph_builder.add_conditional_edges(
            source='pick_a_file',
            path=should_generate_next,
            path_map={
                END:END,
                'generate_code':'generate_code'
            })
        graph_builder.add_edge('generate_code','sanitize_code')
        graph_builder.add_edge('sanitize_code','write_code_to_file')
        graph_builder.add_edge('write_code_to_file','pick_a_file')

        graph = graph_builder.compile()

        return graph
    
    async def arun(self):
        return await self.graph.ainvoke(self.initital_state,{"recursion_limit": self.max_recursion_allowed})
    
    def create_project_structure(self,state:DeveloperState):

        prompt_template = self.prompts.get_prompt(PromptTypes.GENERATE_PROJECT_STRUCTURE)
        project_structure_parser = PydanticOutputParser(pydantic_object=ProjectStructure)
        prompt = prompt_template.format(
            project_description=state['requirements'].description,
            format=project_structure_parser.get_format_instructions()
        )
    
        response = self.llm_with_temperature(0.3).invoke(prompt).content
        
        file_list = project_structure_parser.parse(response).files

        state['files'] = file_list

        state['current_file'] = CurrentFile(index=0,code=None)

        logger.info(f"📄 Total files to be generated: {len(file_list)}")

        return state
    
    def sanitize_project_description(self,state:DeveloperState):

        logger.info("🧼 Sanitizing Project Description...")

        prompt_template = self.prompts.get_prompt(PromptTypes.SANITIZE_PROJECT_DESCRIPTION)
        requirements_parser = PydanticOutputParser(pydantic_object=Requirements)
        prompt = prompt_template.format(
            project_description=state['requirements'].description,
            project_name=state['requirements'].project_name,
            format=requirements_parser.get_format_instructions()
        )
        response = self.llm_with_temperature(0).invoke(prompt).content
        requirements = requirements_parser.parse(response)

        state['requirements'] = requirements

        return state 

    def create_base_project(self,state:DeveloperState):

        logger.info("🚀 Initializing Base Project... (Running template setup)")

        _ = run_commands([self.tech_specific_commands.project_setup_command()],cwd=self.cwd)[0]

        return state
    
    def install_packages(self,state:DeveloperState):

        packages = state['requirements'].packages

        logger.info(f"📦 Installing Packages: {packages}...")

        _ = run_commands([self.tech_specific_commands.package_install_command(packages)],cwd=self.cwd)[0]

        return state
    
    def sort_files_by_dependency(self,state:DeveloperState):

        logger.info("📦 Sorting files based on dependencies...")

        return state
    
    def pick_a_file(self,state:DeveloperState):

        logger.info("📂 Picking up the file for generation...")

        picked_file_index = FileHelper.get_next_unprocessed_file_index(state['files'])
        state['current_file'] = CurrentFile(index=picked_file_index,code=None)

        return state
    
    def generate_code(self,state:DeveloperState):        
        current_file = state['files'][state['current_file'].index]
        dependencies_path = current_file.dependencies

        logger.info(f"🛠️  Generating code for {current_file.name}...")

        prompt_template = self.prompts.get_prompt(PromptTypes.GENERATE_FILE)
        prompt = RagHelper.get_formatted_prompt(
            prompt=prompt_template,                        
            partial_variables={
                'packages': state['requirements'].packages,
                'file':current_file.name,
                'documentation':current_file.documentation,
                'path':current_file.path,
                'project_description':state['requirements'].description
            }
        )

        chain = RagHelper.get_suitable_chain(
            llm=self.llm_with_temperature(0.3),
            vector_store=self.vector_store,
            formatted_prompt=prompt,
            num_results=self.num_rag_results_allowed
        )

        query = f"Generate the Code for {current_file.name}, You can use these files : {dependencies_path}"
        code = chain.invoke(query)['result']

        state['current_file'].code = code
        state['files'][state['current_file'].index].is_generated = True

        logger.info("📖 Adding to contexts...")

        code_info = (
            f"File Name : {current_file.name}\n\n"
            f"File Path : {current_file.path}\n\n"
            f"About File : {current_file.documentation}\n\n"
            f"Code : {code}\n\n\n"
        )
        self.vector_store.add_documents(
            documents=[
                Document(page_content=code_info,metadata={'name':current_file.name,'content_type':'code'})
            ]
        )
        return state
    
    def sanitize_code(self,state:DeveloperState):

        logger.info("🧼 Sanitizing Code...")

        def clean_code_block(code: str) -> str:
            return re.sub(r"^```[a-zA-Z]*\n?|```$", "", code, flags=re.MULTILINE).strip()

        state['current_file'].code = clean_code_block(state['current_file'].code)
        return state
    
    def write_code_to_file(self,state:DeveloperState):
        current_file = state['files'][state['current_file'].index]

        file_path = os.path.join(self.cwd,current_file.path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(state['current_file'].code)
        
        # Reset the current file
        state['current_file'] = CurrentFile(index=-1,code=None)

        logger.info(f"✅ Successfully wrote code to: {current_file.path}")

        return state
    
