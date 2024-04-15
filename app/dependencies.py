from googletrans import Translator
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from fastapi import Depends
from preprocessingService import PreprocessingService
from pineconeRepository import PineconeRepository

def get_embeddings_model():
    try:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        yield embedding_model
    finally:
        pass

def get_pinecone_client():
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        pcClient = pc.Index("influencers")
        yield pcClient
    finally:
        pcClient = None

def get_pinecone_repository(client=Depends(get_pinecone_client)):
    return PineconeRepository(client)

def get_translator():
    return Translator()

def get_preprocessing_service(translator = Depends(get_translator)):
    return PreprocessingService(translator=translator)