from contextlib import asynccontextmanager
import os
from bertopic import BERTopic
from fastapi import FastAPI
from dotenv import load_dotenv
from huggingface_hub import HfFolder
import redis
from app.Controllers.visualiseRouter import visualiseRouter
from app.Controllers.clusterRouter import clusterRouter
from app.Controllers.searchRouter import searchRouter
from sentence_transformers import SentenceTransformer
from app.Dependencies.globalResources import global_resources
import nltk


@asynccontextmanager
async def lifespan(app: FastAPI):
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    nltk.download("stopwords")
    global_resources["embedding_model"] = embedding_model
    HfFolder.save_token(os.getenv("HF_TOKEN"))
    topic_model = BERTopic.load("RebaiMed/Bertopic-Influencers",embedding_model=embedding_model)
    global_resources["topic_model"] = topic_model
    global_resources["redis_pool"] = redis.from_url(os.getenv("REDIS_URL"),decode_responses=True)
    yield
    global_resources.clear()

#Load environment variables
load_dotenv(dotenv_path=".env")
#Start the server
app = FastAPI(lifespan=lifespan)
app.include_router(searchRouter)
app.include_router(clusterRouter)
app.include_router(visualiseRouter)





