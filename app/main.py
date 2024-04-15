from typing import Union
from fastapi import FastAPI, HTTPException, Query, Depends
from dotenv import load_dotenv
from pineconeRepository import PineconeRepository
from dependencies import get_embeddings_model,get_pinecone_repository, get_preprocessing_service
from pydantic import BaseModel
from schemas import SearchQueryParams, SimilarityQueryParams

#Load environment variables
load_dotenv(dotenv_path="../.env")
#Start the server
app = FastAPI()

@app.get("/similar/{influencer_id}")
def getSimilarInfluencers(influencer_id:str,queryParams:SimilarityQueryParams=Depends() ,pineconeRepository:PineconeRepository=Depends(get_pinecone_repository)):
    results = pineconeRepository.get_similar(influencer_id,num_results=queryParams.max_results)
    if(len(results)==0):
        raise HTTPException(404,f"Object with id {influencer_id} not found")
    return [{'id':result["id"], 'score':result["score"]} for result in results if result["score"] >= queryParams.threshold]

@app.get("/search")
def semanticSearchInfluencers(queryParams: SearchQueryParams = Depends(), model = Depends(get_embeddings_model), pineconeRepository=Depends(get_pinecone_repository), preprocessingService=Depends(get_preprocessing_service)):
    query_embedding = model.encode(queryParams.query)
    query = preprocessingService.preprocess_query(queryParams.query)
    results = pineconeRepository.search_embeddings(query_embedding.tolist(), queryParams.max_results)
    return [{'id':result["id"], 'score':result["score"]} for result in results if result["score"] >= queryParams.threshold]