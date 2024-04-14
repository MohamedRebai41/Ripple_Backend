from typing import Union
from fastapi import FastAPI, Query, Depends
from dotenv import load_dotenv
from dependencies import get_embeddings_model,get_pinecone_repository

load_dotenv(dotenv_path="../.env")
#Start the server
app = FastAPI()


@app.get("/search")
def semanticSearchInfluencers(query: str = Query(...,min_length=3,max_length=512), model = Depends(get_embeddings_model), pineconeRepository=Depends(get_pinecone_repository)):
    query_embedding = model.encode(query)
    results = pineconeRepository.search_embeddings(query_embedding.tolist(), 10)
    return [{'id':result["id"], 'score':result["score"]} for result in results["matches"]]