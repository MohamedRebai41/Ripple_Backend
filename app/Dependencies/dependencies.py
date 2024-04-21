from googletrans import Translator
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from fastapi import Depends
from sessionManager import SessionManager
from openAIService import OpenAIService
from preprocessingService import PreprocessingService
from pineconeRepository import PineconeRepository

def get_embeddings_model():
    try:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        yield embedding_model
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


def get_translator():
    return Translator()

def get_preprocessing_service(translator = Depends(get_translator)):
    return PreprocessingService(translator=translator)

#sessions
def get_session_manager():
    return SessionManager()
