# LangGraph Developer Agent 🦸‍♂️

Welcome to the LangGraph Developer Agent, your coding sidekick that spins up any project faster than you can say "commit to GitHub!" 🚀 Feed it your project idea, and it’ll generate code like a wizard casting spells 🧙‍♂️. Powered by LangGraph, it’s automation with a sprinkle of magic ✨.

This README covers setup and usage to unleash this agent’s power on GitHub. Let’s dive in! 😎

---

## Features 🌟

- **Project Generator**: Builds any project from your requirements (web apps, CLIs, or your wildest ideas!).
- **Tech Flexibility**: Supports multiple tech stacks via the `Technologies` enum.
- **Smart Workflow**: LangGraph orchestrates the process like a pro conductor 🎶.
- **Logging**: Tracks progress, so you’re never lost in the code jungle 🌴.

---

## Prerequisites 🛠️

- Python 3.8+ 🐍  
- Git 📜  
- Project-specific tools (e.g., Node.js for Node projects)  
- `requirements.txt` or `uv` file for dependencies  
- A dash of coding enthusiasm 😄  

---

## Installation 📦

Choose your flavor: `venv` or `uv`.

### Option 1: Using `venv` 🐍

```bash
# Clone the repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Set up and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

Ready to rock! 🎉

### Option 2: Using `uv` ⚡

```bash
# Sync dependencies
uv sync

# Activate the environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

You’re good to go! 💥

---

## Usage 🚀

Create a Python script (e.g., `run_agent.py`) to define your project. Here’s a sample for a Node.js task app, but customize it for any project:

```python
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

# Run agent
final_state = dev_agent.run()

from modules.graph.developer_agent import DeveloperState
final_state = DeveloperState(**final_state)
```

Run it using either:

```bash
python run_agent.py
```

or, if using `uv`:

```bash
uv run run_agent.py
```

Your project files will appear in a new directory (e.g., `TaskManager`). Check logs for details. 🎉

---

## Troubleshooting 🐞

* Dependency issues? Verify `requirements.txt`, run `uv sync`, and check your Python version (3.8+).
* Script not running? Ensure your virtual environment is activated and dependencies are installed.
* Still stuck? Check logs or channel your inner Sherlock 🕵️‍♂️.

---

## Contributing 🤝

Want to level up this agent? Fork, tweak, and submit a pull request. We love community vibes! 🌈

---

## License 📜

MIT License. Use, share, remix—just don’t build a rogue AI without a shoutout 😉.

---

Happy coding, and may your commits be clean and your coffee strong! ☕
