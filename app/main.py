from contextlib import asynccontextmanager
import os
import secrets
from typing import Union
from fastapi import Cookie, FastAPI, HTTPException, Query, Depends, Response
from dotenv import load_dotenv
import redis
from app.Controllers.searchRouter import searchRouter
from app.Services.sessionManager import SessionManager
from app.Services.openAIService import OpenAIService
from app.Dependencies.authorization import get_api_key
from app.Services.pineconeRepository import PineconeRepository
from app.Dependencies.dependencies import get_embeddings_model, get_openai_service,get_pinecone_repository, get_preprocessing_service, get_session_manager
from pydantic import BaseModel
from app.Schemas.schemas import SearchBody, SearchQueryParams, SearchSessionConfig, SimilarityQueryParams
import json



#Load environment variables
load_dotenv(dotenv_path=".env")
#Start the server
app = FastAPI()
app.include_router(searchRouter)





