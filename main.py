import asyncio
from modules.implementations.nodejs.team.team import NodeJsTeam
from modules.logging.logger import setup_logger
from modules.core.llms.llms import openai_with_temperature

process_id = "x_y_z"
setup_logger(process_id)
team = NodeJsTeam(process_id,llm=openai_with_temperature)
asyncio.run(team.start_working())