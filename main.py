from modules.logging.logger import setup_logger
from modules.graph.developer_agent import DeveloperAgent
from modules.types.enums import Technologies
from modules.types.models import Requirements

# Inputs
process_id = "rag-on-pdfs"
project_description = """
Build a Python project that performs Retrieval-Augmented Generation (RAG) on PDFs.

### 🧠 Project Requirements:
- Read **all PDF documents** from a `data/` folder automatically.
- Use a **local vector database** like **ChromaDB**
- Extract text from each PDF and **embed** it using a local embedding model (e.g., `sentence-transformers`).
- Store vectorized data into the local vector DB. use Hugging face embeddings.
- Provide a **Streamlit chat interface** that:
  - Accepts user questions.
  - Retrieves relevant document chunks from the vector store.
  - Use open ai for llm
- use langchain packages for llm

Keep all the imports from root.
Generate a example .env
Add a app.py to root
"""

setup_logger(process_id)

dev_agent = DeveloperAgent(
    process_id=process_id,
    requirements=Requirements(
        project_name="rag-on-pdfs",
        project_description=project_description,
        packages=[],
        technology=Technologies.PYTHON.value,
    )
)

dev_agent.run()
