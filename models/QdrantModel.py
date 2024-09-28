import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from langchain_openai import OpenAIEmbeddings

from models.ChunkModel import Chunk

load_dotenv()
QDRANT_SERVER_URL = os.getenv("QDRANT_SERVER_URL")

class Qdrant:
    def __init__(self, embedding_model : OpenAIEmbeddings):
        self.client = QdrantClient(url=QDRANT_SERVER_URL)
        self.embedding_model = embedding_model

    def create_collection_if_not_exists(self, collection_name):
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.DOT)
            )

    def insert_point(self, collection_name, chunk : Chunk):
        try:
            self.client.upsert(
                collection_name=collection_name,
                wait=True,
                points=[
                    PointStruct(
                        id=chunk.id,
                        vector=self.embedding_model.embed_query(chunk.text),
                        payload={
                            "text": chunk.text,
                            "filename": chunk.file_name
                        }
                    )
                ]
            )
        except Exception as e:
            raise InsertionException(f"InsertionException - Error inserting chunk from {chunk.file_name} into Qdrant: {e}")
        
    
    def query_point(self, collection_name, user_query):

        hits = self.client.query_points(
            collection_name=collection_name,
            query=self.embedding_model.embed_query(user_query),
        ).points

        retrieved_docs = [hit.payload for hit in hits]

        return retrieved_docs


class InsertionException(Exception):
    pass