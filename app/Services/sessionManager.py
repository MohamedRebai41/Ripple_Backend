import json
import secrets
import os
from fastapi import HTTPException
import redis

class SessionManager:
    def __init__(self):
        self.client = redis.from_url(os.getenv("REDIS_URL"),decode_responses=True)
        self.expiry_time = 60*60*24
        if(self.client == None):
            raise Exception("Redis client is not created")

        
    def new_session(self,data=""):
        key = secrets.token_urlsafe()
        self.client.set(key,json.dumps(data))
        # self.client.setex(key,self.expiry_time)
        return key
            
    def get_session(self,session_key):
        if(not self.client.exists(session_key)):
            raise HTTPException("Session key does not exist")
        return json.loads(self.client.get(session_key))
    

    def update_session(self,session_key,data):
        if(not self.client.exists(session_key)):
            raise HTTPException("Session key does not exist")
        self.client.set(session_key,json.dumps(data))

    def close_session(self,session_key):
        self.client.delete(session_key)