from email.policy import HTTP
from bertopic import BERTopic
# from googletrans import Translator
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException

from app.Services.sessionManager import SessionManager
from app.Services.openAIService import OpenAIService
from app.Services.preprocessingService import PreprocessingService
from app.Services.pineconeRepository import PineconeRepository
from app.Dependencies.globalResources import global_resources

def get_embeddings_model():
    try:
        yield global_resources["embedding_model"]
    finally:
        pass


def get_topic_model():
    try:
        return global_resources["topic_model"]
    finally:
        pass



#Pinecone db dependency
def get_pinecone_client():
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        pcClient = pc.Index("influencers")
        yield pcClient
    finally:
        pcClient = None

def get_pinecone_repository(client=Depends(get_pinecone_client)):
    return PineconeRepository(client)


#OpenAI dependency
def get_openai_client():
    return OpenAI()

def get_openai_service(client=Depends(get_openai_client)):
    return OpenAIService(client)


# def get_translator():
#     return Translator()

def get_preprocessing_service():
    return PreprocessingService()




#sessions
def get_redis_pool():
    try:
        return global_resources["redis_pool"]
    except:
        raise HTTPException("Redis pool could no be created")
    finally:
        pass


def get_session_manager(client = Depends(get_redis_pool)):
    return SessionManager(client)
