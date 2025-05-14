from typing import List
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import chromadb
from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions
from torch import nn
import os

VECTOR_DB_PATH = "./../vector_db"

# Pydantic model for structured output
class RankedContext(BaseModel):
    document: str
    rank: int
    score: float

class RankingBasedRetriever:
    def __init__(self, collection_name:str, persist_directory=VECTOR_DB_PATH):
        self.embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-base")
        self.reranker = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-base")
        self.reranker.eval()

        # Initialize persistent Chroma client
        self.persist_directory = persist_directory
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("BAAI/bge-small-en-v1.5")
        )

        # Sigmoid function for normalization
        self.sigmoid = nn.Sigmoid()

    def from_documents(self, docs: List[str]):
        ids = [str(i) for i in range(len(docs))]
        self.collection.add(documents=docs, ids=ids)

    def query_and_rerank(self, query: str, top_k: int = 5) -> List[RankedContext]:
        initial = self.collection.query(query_texts=[query], n_results=top_k)
        candidates = initial["documents"][0]

        # Create query-doc pairs
        pairs = [(query, doc) for doc in candidates]
        inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            # Get raw logits scores
            scores = self.reranker(**inputs).logits.squeeze(-1)

        # Normalize scores to range [0, 1] using sigmoid
        normalized_scores = self.sigmoid(scores)

        # Sort documents by normalized score in descending order
        sorted_pairs = sorted(zip(candidates, normalized_scores.tolist()), key=lambda x: x[1], reverse=True)

        # Return Pydantic model instances
        return [
            RankedContext(document=doc, rank=i+1, score=score)
            for i, (doc, score) in enumerate(sorted_pairs)
        ]

    def save_local(self):
        """
        Save the ChromaDB collection to the specified persist directory.
        The collection is automatically persisted by the PersistentClient.
        """
        # Ensure the persist directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        # ChromaDB's PersistentClient automatically handles persistence
        print(f"Collection saved to {self.persist_directory}")

    def load_local(self):
        """
        Load the ChromaDB collection from the specified persist directory.
        """
        try:
            # Reinitialize the persistent client and collection
            self.chroma_client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.chroma_client.get_collection(
                name=self.collection.name,
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("BAAI/bge-small-en-v1.5")
            )
            print(f"Collection loaded from {self.persist_directory}")
        except Exception as e:
            raise ValueError(f"Failed to load collection from {self.persist_directory}: {str(e)}")