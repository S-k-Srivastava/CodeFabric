import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from modules.prompts import decide_packages_prompts as DecidePackagesPrompts
from modules.prompts import create_project_plan_prompts as CreateProjectPlanPrompts
from enum import Enum
from typing import List, Dict
from collections import defaultdict, deque
from dotenv import load_dotenv

from modules.types.output_formatters import PackagesFormatter,FileInfosFormatter
load_dotenv()
import os

from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from modules.graph.sql_checkpointer import MySQLCheckpointer

from modules.utils.command_runner import CommandRunner

from modules.types.models import FileInfo, Requirements, ResultState

from modules.data.commands import ProjectInitializationCommands,PackageInstallationCommands

logger = logging.getLogger(__name__)

agent_name = "developer_agent"
output_folder = "./outputs"

model_name = "gpt-4o"
reasoning_model_name = "o4-mini"

class DeveloperState(TypedDict):
    process_id: str
    cwd: str
    requirements : Requirements
    files : list[FileInfo]
    result_states : dict[str,ResultState]
    current_index: int

class NodeIDs(Enum):
    INITIALIZE_PROJECT = "initialize-project"
    RECOMMEND_PACKAGES = "recommend-packages"
    INSTALL_PACKAGES = "install-packages"
    CREATE_PROJECT_PLAN = "create-project-plan"
    SORT_TOPOLOGICALLY = "sort-topologically"
    GENERATE_FILE_CODE = "generate-file-code"

class DeveloperAgent:
    def __init__(
        self,
        process_id: str,
        requirements: Requirements,
        llm=None,
        reasoning_llm=None,
        allowed_retry_count=3,
    ):  
        # Initialize max allowed retries for any node
        self.allowed_retry_count = allowed_retry_count

        # Initialize Initial State and cwd
        cwd = os.path.join(output_folder, requirements['project_name'])
        os.makedirs(cwd, exist_ok=True)
        self.initial_state = DeveloperState(
            process_id = process_id,
            cwd = cwd,
            requirements = requirements,
            files = [],
            result_states={},
            current_index = -1,
            is_initialized=False
        )

        # Create Command Runner
        self.command_runner = CommandRunner(cwd=cwd)
        logger.info(f"🎉 **DeveloperAgentInitialization**: Command Runner set up successfully! Working directory: `{cwd}` 🚀")

        # Initialize LLM
        self.llm = ChatOpenAI(model=model_name) if llm is None else llm
        self.reasoning_llm = ChatOpenAI(model=reasoning_model_name) if reasoning_llm is None else reasoning_llm
        logger.info(f"✨ **ModelSetup**: Using LLM: {self.llm.__class__.__name__} and Reasoning LLM: {self.reasoning_llm.__class__.__name__} 🧠")

        # Initialize Checkpointer
        self.checkpointer = MySQLCheckpointer(agent_name)
        logger.info("🎉 **Checkpoint**: Checkpoint initialized successfully! 🗃️")

        # Build Graph
        self.graph = self._build_graph()

    def _build_graph(self):
        logger.info("🛠️  **GraphConstruction**: Starting graph build process! 🚀")

        graph_builder = StateGraph(DeveloperState)

        # Adding Nodes
        graph_builder.add_node(NodeIDs.INITIALIZE_PROJECT.value,self.initialize_project)
        graph_builder.add_node(NodeIDs.RECOMMEND_PACKAGES.value,self.recommend_packages)
        graph_builder.add_node(NodeIDs.INSTALL_PACKAGES.value,self.install_packages)
        graph_builder.add_node(NodeIDs.CREATE_PROJECT_PLAN.value,self.create_project_plan)
        graph_builder.add_node(NodeIDs.SORT_TOPOLOGICALLY.value,self.sort_topologically)
        graph_builder.add_node(NodeIDs.GENERATE_FILE_CODE.value,self.generate_file_code)

        # Retry Conditions : If any node fails, create retry condition
        # based on the result_state of that node or step
        # loop_to_node : Node to go back and retry if error
        # next_node : Actual next node if no error
        def make_retry_condition_path(loop_to_node:str,next_node:str,result_id:str):    
            def should_retry(state:DeveloperState):
                if not state['result_states'].get(result_id)['success'] and \
                    state['result_states'].get(result_id)['retries'] < self.allowed_retry_count:

                    logger.error(f"❌ **Error**: Failed with: {state['result_states'][result_id]['error']} 😓")
                    logger.warning(f"🔄 **Retry**: Attempting retry for {result_id} -- {state['result_states'][result_id]['retries']+1}/{self.allowed_retry_count} ⏳")
                    
                    if state['result_states'].get(result_id)['error'] == None:
                        raise Exception("No Error Details Found!")
                    return loop_to_node
                
                return next_node
            
            return should_retry

        # Edges
        graph_builder.add_edge(START,NodeIDs.INITIALIZE_PROJECT.value)
        graph_builder.add_edge(NodeIDs.INITIALIZE_PROJECT.value,NodeIDs.RECOMMEND_PACKAGES.value)
        graph_builder.add_edge(NodeIDs.RECOMMEND_PACKAGES.value,NodeIDs.INSTALL_PACKAGES.value)

        ## Retry Conditional Edge Path
        install_packages_path = make_retry_condition_path(
            loop_to_node=NodeIDs.RECOMMEND_PACKAGES.value,
            next_node=NodeIDs.CREATE_PROJECT_PLAN.value,
            result_id = f"{NodeIDs.RECOMMEND_PACKAGES.value}+{NodeIDs.INSTALL_PACKAGES.value}"
        )
        graph_builder.add_conditional_edges(source=NodeIDs.INSTALL_PACKAGES.value,path=install_packages_path)
        graph_builder.add_edge(NodeIDs.CREATE_PROJECT_PLAN.value,NodeIDs.SORT_TOPOLOGICALLY.value)
        graph_builder.add_edge(NodeIDs.SORT_TOPOLOGICALLY.value,END)
        
        # Compile Graph with Checkpointer
        graph = graph_builder.compile(checkpointer=self.checkpointer)

        logger.info("🎉 **GraphCompletion**: Graph successfully built and compiled! 🏗️")

        return graph
    
    def run(self):
        # Graph Config
        config = {"configurable": {"thread_id": self.initial_state['process_id']}}

        # Check if any previous checkpoint
        if self.graph.get_state(config).values == {}:
            start_state = self.initial_state
        else:
            logger.info("🔄 **Resume**: Resuming from last checkpoint! 📍")
            start_state = None
        
        # Invoke
        self.graph.invoke(start_state,config=config)

    async def arun(self):
        # Graph Config
        config = {"configurable": {"thread_id": self.initial_state['process_id']}}

        # Check if any previous checkpoint
        if self.graph.get_state(config).values == {}:
            start_state = self.initial_state
        else:
            logger.info("🔄 **Resume**: Resuming from last checkpoint! 📍")
            start_state = None
        
        # Async Invoke
        await self.graph.ainvoke(start_state,config=config)
    
    def initialize_project(self,state:DeveloperState) -> DeveloperState:
        # Get Technology
        technology = state['requirements']['technology']

        logger.info(f"🚀 **ProjectInit**: Initializing project with technology: {technology} 🛠️")

        # If No Command Found raise Exception
        if technology not in ProjectInitializationCommands:
            raise Exception(f"No Command Found For: {technology}")
        
        # Run Command
        command = ProjectInitializationCommands[technology]
        logger.info(f"🛠️  **CommandExecution**: Running Initialization command: {command} 🔧")
        command_result = self.command_runner.run_commands([command])[0]

        logger.info(f"✅ **CommandResult**: Command executed successfully! 🎉")

        # If Command Failed then raise Exception
        if not command_result.is_success:
            raise Exception(command_result.error)
        
        return state
    
    def recommend_packages(self,state:DeveloperState) -> DeveloperState:
        # Shared result id for recommend_packages and install_packages
        result_id = f"{NodeIDs.RECOMMEND_PACKAGES.value}+{NodeIDs.INSTALL_PACKAGES.value}"

        logger.info("📦 **PackageRecommendation**: Starting package recommendation process! 🚀")
        
        # Get Previous Result State or Initialize New Result State
        result_state = state['result_states'].get(result_id,None)
        if result_state is None:
            result_state = ResultState(
                messages=[SystemMessage(DecidePackagesPrompts.system_prompt)],
                success=False,
                error=None,
                version=0,
                retries=0,
            )
            state['result_states'][result_id] = result_state

        # Based on Result State, success or failure, preparing next message
        if result_state['error'] != None:
            state['result_states'][result_id]['retries'] += 1
            state['result_states'][result_id]['messages'].append(
                HumanMessage(DecidePackagesPrompts.fix_prompt.format(error=result_state['error']))
            )
        else:
            state['result_states'][result_id]['messages'].append(
                HumanMessage(state['requirements']['project_description'])
            )

        # Invokation
        _packages = self.reasoning_llm.with_structured_output(PackagesFormatter)\
            .invoke(state['result_states'][result_id]['messages'])
        
        # Update State
        state['result_states'][result_id]['messages'].append(AIMessage(str(_packages.model_dump_json())))
        state['requirements']['packages'] = _packages.to_model
        state['result_states'][result_id]['version'] += 1

        return state
    
    def install_packages(self,state:DeveloperState):
        # Shared result id for recommend_packages and install_packages
        result_id = f"{NodeIDs.RECOMMEND_PACKAGES.value}+{NodeIDs.INSTALL_PACKAGES.value}"

        # Install the Packages
        technology = state['requirements']['technology']
        command = PackageInstallationCommands[technology]
        command = command.format(packages=" ".join(state['requirements']['packages']))
        logger.info(f"🛠️  **CommandExecution**: Running installation command: {command} 🔧")
        command_result = self.command_runner.run_commands([command])[0]

        # Update Result State
        if command_result.is_success:
            logger.info(f"✅ **CommandResult**: Command executed successfully! 🎉")
            state['result_states'][result_id]['success'] = True
            state['result_states'][result_id]['error'] = None
        else:
            state['result_states'][result_id]['success'] = False
            state['result_states'][result_id]['error'] = command_result.error

        return state
    
    def create_project_plan(self,state:DeveloperState) -> DeveloperState:
        # result_id
        result_id = NodeIDs.CREATE_PROJECT_PLAN.value

        logger.info("📦 **ProjectPlan**: Starting project plan creation process! 🚀")

        # Get Previous Result State or Initialize New Result State
        result_state = state['result_states'].get(result_id,None)
        if result_state is None:
            result_state = ResultState(
                messages=[SystemMessage(CreateProjectPlanPrompts.system_prompt)],
                success=False,
                error=None,
                version=0,
                retries=0,
            )
            state['result_states'][result_id] = result_state

        # Initialize Converstation with contexts
        context_provider_prompt = (
            f"Tech Stack: {state['requirements']['technology']}\n"
            f"Packages: {' '.join(state['requirements']['packages'])}"
            f"Project Description: {state['requirements']['project_description']}\n"
        )
        state['result_states'][result_id]['messages'].append(HumanMessage(context_provider_prompt))
        _files = self.reasoning_llm.with_structured_output(FileInfosFormatter)\
            .invoke(state['result_states'][result_id]['messages'])
        state['result_states'][result_id]['messages'].append(AIMessage(str(_files.model_dump_json())))

        # Update State
        state['files'] = _files.to_model
        state['result_states'][result_id]['version'] += 1

        logger.info(f"✅ **ProjectPlan**: Plan created successfully, total files: {len(state['files'])} 🎉")

        return state
    
    def sort_topologically(self,state:DeveloperState) -> DeveloperState:

        logger.info("📦 **TopologicalSort**: Starting topological sort process! 🚀")

        # Build graph and in-degree count
        files = state['files']
        path_to_file = {file['path']: file for file in files}
        graph = defaultdict(list)
        in_degree = defaultdict(int)

        # Initialize in-degree for all files
        for file in files:
            in_degree[file['path']] = 0

        # Build graph edges and in-degrees
        for file in files:
            for dep in file.get('dependencies', []):
                if dep in path_to_file:
                    graph[dep].append(file['path'])
                    in_degree[file['path']] += 1

        # Start with files that have no dependencies
        queue = deque([path for path in in_degree if in_degree[path] == 0])
        sorted_paths = []

        while queue:
            current = queue.popleft()
            sorted_paths.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check for cycles
        if len(sorted_paths) != len(files):
            raise ValueError("Cycle detected in dependencies. Cannot reorder safely.")

        # Return reordered file list
        state['files'] = [path_to_file[path] for path in sorted_paths]

        # For Debugging Only
        with open("file_info.json", "w", encoding="utf-8") as f:
            json.dump(state['files'], f, indent=2, ensure_ascii=False)

        logger.info(f"✅ **TopologicalSort**: Files sorted successfully, total files: {len(state['files'])} 🎉")

        return state
    
    def generate_file_code(self,state:DeveloperState) -> DeveloperState:
        return state