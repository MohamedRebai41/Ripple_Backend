from contextlib import asynccontextmanager
import secrets
from typing import Union
from fastapi import Cookie, FastAPI, HTTPException, Query, Depends, Response
from dotenv import load_dotenv
import redis
from sessionManager import SessionManager
from openAIService import OpenAIService
from cookies import get_discussion_session
from authorization import get_api_key
from pineconeRepository import PineconeRepository
from dependencies import get_embeddings_model, get_openai_service,get_pinecone_repository, get_preprocessing_service, get_session_manager
from pydantic import BaseModel
from schemas import SearchBody, SearchQueryParams, SearchSessionConfig, SimilarityQueryParams
import json



#Load environment variables
load_dotenv(dotenv_path="../.env")
#Start the server
app = FastAPI()


sessions = {}






@app.post("/search/get_session")
def get_token(config: SearchSessionConfig ,sessionManager=Depends(get_session_manager)):
    return sessionManager.new_session(data = {
        "conversation":[],
        "max_results":config.max_results ,
        "threshold":config.threshold,
        "number": 0
    } )


@app.get("/similar/{influencer_id}")
def getSimilarInfluencers(influencer_id:str,queryParams:SimilarityQueryParams=Depends() ,pineconeRepository:PineconeRepository=Depends(get_pinecone_repository)):
    results = pineconeRepository.get_similar(influencer_id,num_results=queryParams.max_results)
    if(len(results)==0):
        raise HTTPException(404,f"Object with id {influencer_id} not found")
    return [{'id':result["id"], 'score':result["score"]} for result in results if result["score"] >= queryParams.threshold]

@app.post("/search")
def semanticSearchInfluencers(data: SearchBody ,session_key:str=Query(...),
                                model = Depends(get_embeddings_model),
                                pineconeRepository=Depends(get_pinecone_repository), 
                                preprocessingService=Depends(get_preprocessing_service), 
                                openAIService: OpenAIService = Depends(get_openai_service),
                                sessionManager:SessionManager = Depends(get_session_manager)):

    session = sessionManager.get_session(session_key=session_key)
    input = data.input
    if(len(session["conversation"]) == 0):
        new_query = openAIService.get_start_message(input)
    else:
        new_query = openAIService.get_message(role='user',message=input)

    #Updating the conversation
    session["conversation"].append(new_query)
    raw_assistant_response = openAIService.process_query(session["conversation"])
    session["conversation"].append(openAIService.get_message('assistant',raw_assistant_response))
    session["number"]+=1
    sessionManager.update_session(session_key,session)

    #Querying the vector database with the embedded query 
    assistant_response = json.loads(raw_assistant_response)
    query = preprocessingService.preprocess_query(assistant_response["enhanced_query"])
    query_embedding = model.encode(assistant_response["enhanced_query"])   
    results = pineconeRepository.search_embeddings(query_embedding.tolist(), session["max_results"])

    if (results[0]["score"] > session["threshold"] and session["number"] >= 2) or ( session["number"] >= 3):
        return [{'id':result["id"], 'score':result["score"]} for result in results]
    else:
        return  assistant_response["next_question"]
    
@app.post("/new")
def addInfluencer(api_key = Depends(get_api_key)):
    return "influencer added"