from langchain.chains.retrieval_qa.base import RetrievalQA,BaseRetrievalQA
from langchain.vectorstores import VectorStore
from langchain.chat_models.base import BaseChatModel
from langchain.prompts.prompt import PromptTemplate
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class RagHelper:
    @staticmethod
    def get_suitable_chain(
        llm: BaseChatModel,
        vector_store: VectorStore,
        formatted_prompt: PromptTemplate,
        filters: dict = None,
        num_results: int = 4,
    )->BaseRetrievalQA:
        """
        Returns Retrieval QA chain based on provided parameters.
        """
        if filters:
            retriever = vector_store.as_retriever(search_kwargs={"filter": filters,"k":num_results})
        else:
            retriever = vector_store.as_retriever(search_kwargs={"k":num_results})
        
        return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": formatted_prompt
                }
            )
    
    @staticmethod
    def get_vector_store()->VectorStore:
        """
        Return Chroma Vector Store.
        """
        vc = Chroma(
            embedding_function=HuggingFaceEmbeddings( model_kwargs={"device": "cpu"}),
        )
        return vc
    
    @staticmethod
    def get_formatted_prompt(prompt:PromptTemplate,partial_variables:dict)->PromptTemplate:
        """
        Formatts prompt with partial variables.
        """
        return PromptTemplate(
                template=prompt,
                input_variables=["context", "query"],
                partial_variables=partial_variables
            )