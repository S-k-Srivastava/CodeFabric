from enum import Enum
import logging
import os
from typing import TypedDict

from langchain_openai import ChatOpenAI

from modules.graph.sql_checkpointer import MySQLCheckpointer
from modules.types.models import FileInfoDebugAndFix
from modules.utils.command_runner import CommandRunner

logger = logging.getLogger(__name__)

agent_name = "debug_and_fix_agent"
output_folder = "./outputs"

model_name = "gpt-4o"
# model_name="gpt-4.1-2025-04-14"
reasoning_model_name = "o4-mini"

class NodeIDs(Enum):
    DETECT_ERROR_FILES = "detect-error-files"
    RETRIEVE_FILES = "retrieve-files"
    FIX_FILES = "fix-files"
    GIT_COMMIT = "git-commit"

class DebugAndFixState(TypedDict):
    process_id: str
    errors: dict[str,any]
    related_files: dict[str,list[FileInfoDebugAndFix]]
    files: list[FileInfoDebugAndFix]

class DebugAndFixAgent:
    def __init__(
            self,
            process_id: str,
            folder_name:str, # project name
            llm=None,
            reasoning_llm=None,
            allowed_retry_count=3,
            recursion_limit=150
        ):
         # Initialize max allowed retries for any node
        self.allowed_retry_count = allowed_retry_count
        self.recursion_limit = recursion_limit

         # Initialize LLM
        self.llm = ChatOpenAI(model=model_name) if llm is None else llm
        self.reasoning_llm = ChatOpenAI(model=reasoning_model_name) if reasoning_llm is None else reasoning_llm
        logger.info(f"✨ **ModelSetup**: Using LLM: {self.llm.__class__.__name__} and Reasoning LLM: {self.reasoning_llm.__class__.__name__} 🧠")

        # Initialize Initial State and cwd
        cwd = os.path.join(output_folder, folder_name)
        if not os.path.exists(cwd):
            raise Exception(f"🚨 **DebugAndFixAgentInitialization**: Folder {cwd} does not exist! 🚨")
        self.initial_state = DebugAndFixState(
            process_id = process_id,
            errors = {},
            related_files = {},
            files = []
        )

        # Create Command Runner
        self.command_runner = CommandRunner(cwd=cwd)
        logger.info(f"🎉 **DebugAndFixAgentInitialization**: Command Runner set up successfully! Working directory: `{cwd}` 🚀")

        # Initialize Checkpointer
        self.checkpointer = MySQLCheckpointer(agent_name)
        logger.info("🎉 **Checkpoint**: Checkpoint initialized successfully! 🗃️")

        # Build Graph
        self.graph = self._build_graph()

    def _build_graph(self):
        logger.info("🛠️  **GraphConstruction**: Starting graph build process! 🚀")

    def _init_project_data(self, state:DebugAndFixState):
        logger.info("🛠️  **InitProjectData**: Reading project files! 🚀")
        
