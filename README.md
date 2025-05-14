LangGraph Developer Agent 🦸‍♂️
Welcome to the LangGraph Developer Agent, your coding sidekick that whips up any project faster than you can say "deploy!" 🚀 Feed it your project idea, and it’ll spin up code like a wizard casting spells 🧙‍♂️. Built with LangGraph, it’s automation with a dash of magic ✨.
This README covers setup, usage, and how to unleash this agent’s power. Let’s dive in! 😎
Features 🌟

Project Generator: Creates any project from your requirements (e.g., web apps, CLIs, you name it!).
Tech Flexibility: Supports multiple tech stacks via the Technologies enum.
Smart Workflow: LangGraph orchestrates everything like a pro conductor 🎶.
Logging: Tracks the process, so you’re never lost in the code jungle 🌴.
Graph Visualization: Shows the workflow with a cool Mermaid diagram 📊.

Prerequisites 🛠️

Python 3.8+ 🐍
Git 📜
Project-specific tools (e.g., Node.js for Node projects)
requirements.txt or uv file for dependencies
A pinch of coding enthusiasm 😄

Installation 📦
Pick your flavor: venv or uv.
Option 1: Using venv 🐍

Clone the repo:git clone <your-repo-url>
cd <your-repo-folder>


Set up and activate a virtual environment:python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Ready to rock! 🎉

Option 2: Using uv ⚡
If you have uv, sync dependencies:
uv sync

Activate the environment:
source .venv/bin/activate  # Windows: .venv\Scripts\activate

You’re good to go! 💥
Usage 🚀
Create a Python script (e.g., run_agent.py) to define your project. Here’s a sample for a Node.js task app, but tweak it for any project:
from modules.logging.logger import setup_logger
from modules.graph.developer_agent import DeveloperAgent
from modules.types.enums import Technologies
from modules.types.models import Requirements

# Unique process ID
process_id = "1"

# Project requirements
project_description = """
Create a Node.js backend for task management with APIs to:
1. Create a task
2. Update a task
3. Delete a task
4. Fetch all tasks
"""
requirements = Requirements(
    project_name="TaskManager",
    project_description=project_description,
    packages=[],
    technology=Technologies.NodeJS.value,
)

# Set up logging
setup_logger(process_id)

# Initialize agent
dev_agent = DeveloperAgent(process_id=process_id, requirements=requirements)

# Optional: Visualize workflow
from IPython.display import Image, display
display(Image(dev_agent.graph.get_graph().draw_mermaid_png()))

# Run agent
final_state = dev_agent.run()
from modules.graph.developer_agent import DeveloperState
final_state = DeveloperState(**final_state)

Run it using either:
python run_agent.py

or, if using uv:
uv run run_agent.py

Your project files will appear in a new directory (e.g., TaskManager). Check logs for details and admire the Mermaid diagram if you included visualization. 🎉
Troubleshooting 🐞

Graph issues? Ensure all nodes in dev_agent.graph are connected. Try draw_method=MermaidDrawMethod.API if visualization fails.
Dependency woes? Verify requirements.txt or uv sync and Python 3.8+.
Still stuck? Channel your inner Sherlock 🕵️‍♂️ and check the logs.

Contributing 🤝
Want to make this agent cooler? Fork, tweak, and send a PR. We love community vibes! 🌈
License 📜
MIT License. Use, share, remix—just don’t build a rogue AI without inviting us 😉.
Happy coding, and may your bugs be few and your coffee strong! ☕
