# 🚀 CodeFabric : AI Code Generation Framework  
Your AI-Powered Developer Team 💻🧠

Welcome to the next-gen dev experience! This repository helps you create automated AI developer teams that can generate entire project codebases from natural language descriptions. Currently, we have a working example with a Node.js agent—but the framework is built for expansion to any tech stack you dream of!

---

## 📦 Getting Started

Want to unleash your AI dev team? Follow these simple steps:

1. **Set up API Keys**  
   - Add your LLM API keys to a `.env` file in the root directory.  
   - Choose your model in `main.py` from `modules/core/llms/llms.py`.  
   - Want to use a different LLM provider? Go ahead—plug it in! 🧩

2. **Set up Virtual Environment**  
   - Use `python3 -m venv .venv` or your favorite method (like Conda).  
   - Then run:  
     ```bash
     pip install -r requirements.txt
     ```
   - Activate the venv

3. **Run Redis with Docker**  
   - Start Redis using Docker:  
     ```bash
     sudo docker run -d --name redis-server -p 6379:6379 redis:7
     ```  
   - Or install Redis using your preferred method (see [Redis Docs](https://redis.io)).

4. **Launch the AI Team!**  
   - Fire it up with:  
     ```bash
     python main.py
     ```  
   - Enter your `Process ID`, `Project Name`, and a detailed `Project Description`.
  
5. Check `.sample_projects/bookstore` for sample NodeJs Project generated using this repoistory.

---

## 🧠 Pro Tips for Better Results

- Use powerful reasoning LLMs for best results:
  - ✅ `gemini-2.0-flash-thinking-exp-01-21`
  - ✅ `gpt-4o` and other new models like o3.
- Remember: even human devs make mistakes. While this system won’t guarantee 100% error-free code, with the right prompts and models, it can reach up to **90%+ accuracy**!  
- Want the best? Use great prompts and iterate like a pro. 🔁

---

## 🔁 Process Resumption

### ❓ What happens if the process crashes or your laptop explodes?

No worries! Just re-run the script with the same `Process ID`, and it will pick up right where it left off. Persistence FTW! 🔒💪

---

## 📂 Example Agent: Node.js Developer

Check out the Node.js agent implementation in:  
`modules/implementations/nodejs`

Explore how it:
- Generates file structures
- Builds source code
- Installs dependencies
- And more!

---

## 🛠️ Create Your Own AI Dev Team

Want to support Python, Go, Rust, React, or something wild like COBOL? Here's how you can build your own team:

1. **Create a folder** under `modules/implementations` for your tech.
2. **Add a `prompts/` folder**, and extend `PromptTemplates` from:  
   `modules/core/prompts/prompt_templates.py`
3. **Add your prompts** using the same filenames as listed in `PromptTypes` enum (`modules/core/enums/prompt_types.py`).
4. **Implement project setup commands** by extending `TechSpecificCommands` in `modules/core/commands/commands.py`.
5. **Create your agents** by extending:
   - `Developer` from `modules/core/graphs/developer.py`
   - `RequirementsGatherer` from `modules/core/graphs/requirements_gatherer.py`
6. **Build your `Team` class** by extending `Team` in `modules/core/team/team.py`.
7. **Start the magic** by initializing your team with a `Process ID` and calling `team.start_working()`.

Want to dig deeper? Check the docstrings and the Node.js agent example. They’re your best friends. 📘

---

## 🤝 Contribute and Collaborate!

This project is at the **early stages**, and you can shape its future! 🌱

Here’s how you can help:

- ⚙️ Created a team for a new tech stack? Submit a **PR**!
- 🔍 Got ideas for new agents like a **Code Review Agent**? Let’s build it!
- 🧠 Improved prompts or workflows? Your input is gold.
- 🧼 Found bugs or messy code? Help us clean it up.
- ❤️ Just want to support the project? Star it, share it, or say hi!

> “Code is never perfect, but collaboration brings us closer to greatness.” – Some wise developer, probably

---

## ✨ Final Notes

Let’s push the boundaries of what AI can do in software development. This isn’t just a tool—it’s a movement.  
And you’re invited. 🎉
