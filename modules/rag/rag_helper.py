from langchain.chains.retrieval_qa.base import RetrievalQA,BaseRetrievalQA
from langchain.vectorstores import VectorStore
from langchain.chat_models.base import BaseChatModel
from langchain.prompts.prompt import PromptTemplate
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class RagHelper:
    @staticmethod
    def get_vector_store()->VectorStore:
        """
        Return Chroma Vector Store.
        """
        vc = Chroma(
            embedding_function=HuggingFaceEmbeddings( model_kwargs={"device": "cpu"}),
        )
        return vc