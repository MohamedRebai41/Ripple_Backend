import json
from fastapi import APIRouter, Depends, HTTPException, Query

from app.Dependencies.dependencies import get_embeddings_model, get_openai_service, get_pinecone_repository, get_preprocessing_service, get_session_manager
from app.Schemas.schemas import SearchBody, SearchSessionConfig, SimilarityQueryParams
from app.Services.openAIService import OpenAIService
from app.Services.pineconeRepository import PineconeRepository
from app.Services.sessionManager import SessionManager


searchRouter=APIRouter(prefix="/search")

@searchRouter.get("/similar/{influencer_id}")
def getSimilarInfluencers(influencer_id:str,queryParams:SimilarityQueryParams=Depends() ,pineconeRepository:PineconeRepository=Depends(get_pinecone_repository)):
    results = pineconeRepository.get_similar(influencer_id,num_results=queryParams.max_results)
    if(len(results)==0):
        raise HTTPException(404,f"Object with id {influencer_id} not found")
    return [{'id':result["id"], 'score':result["score"]} for result in results if result["score"] >= queryParams.threshold]

@searchRouter.post("/interactive/get_session")
def get_token(config: SearchSessionConfig ,sessionManager=Depends(get_session_manager)):
    return sessionManager.new_session(data = {
        "conversation":[],
        "max_results":config.max_results ,
        "threshold":config.threshold,
        "requestNumber": 0,
        "minRequests": config.minRequests,
        "maxRequests": config.maxRequests
    } )

@searchRouter.post("/interactive/search")
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
    session["requestNumber"]+=1
    sessionManager.update_session(session_key,session)

    #Querying the vector database with the embedded query 
    assistant_response = json.loads(raw_assistant_response)
    query = preprocessingService.preprocess_query(assistant_response["enhanced_query"])
    query_embedding = model.encode(query)   
    results = pineconeRepository.search_embeddings(query_embedding.tolist(), session["max_results"])

    if (results[0]["score"] > session["threshold"] and session["requestNumber"] >= session["minRequests"]) or ( session["requestNumber"] >= session["maxRequests"]):
        return {"type":"RESULT", "data":[{'id':result["id"], 'score':result["score"]} for result in results]}
    else:
        return  {"type":"QUESTION", "data": assistant_response["next_question"]}
    
