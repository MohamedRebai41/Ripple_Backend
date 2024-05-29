from fastapi import HTTPException
from pinecone import Index
class PineconeRepository:
    def __init__(self, client: Index):
        self.client = client

    def clear_namespace(self, namespace):
        self.client.delete(delete_all=True, namespace=namespace)

    def search_embeddings(self, query_embedding, num_results, namespace="miniLM"):
        return self.client.query(vector=query_embedding, top_k=num_results, namespace=namespace)["matches"][1:]
    

    def get_similar(self, influencer_id:str, num_results:int, namespace="miniLM"):
        return self.client.query(id=influencer_id,top_k=num_results,namespace=namespace)["matches"][1:]
    

