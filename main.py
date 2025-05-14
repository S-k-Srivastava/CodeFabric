from modules.logging.logger import setup_logger
from modules.graph.developer_agent import DeveloperAgent
from modules.types.enums import Technologies
from modules.types.models import Requirements

# Inputs
process_id = "leetcode-agent-any"
project_description = """
Build a python ai agent that takes the leetcode DSA questions, it understands the problem and identify the common
patterns. The explain user how to approach and solve the problem in very pattern identification way.

It then proposes the python solution code for the problem.

I will give the key in the .env.

Make a user freindly streamlit app for the same with chat support. Save the Each Questions as a row in sqlite3 local database.

Use should be able to converse for each question. can change the leetcode question using + icon. can go back to question list and converse again.
"""

setup_logger(process_id)

dev_agent = DeveloperAgent(
    process_id=process_id,
    requirements=Requirements(
        project_name="leetcode-agent-any",
        project_description=project_description,
        packages=[],
        technology=Technologies.PYTHON.value,
    )
)

dev_agent.run()
