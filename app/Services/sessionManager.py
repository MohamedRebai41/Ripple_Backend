import json
import os
import secrets

import redis
from fastapi import HTTPException


class SessionManager:
    def __init__(self, client):
        try:
            self.client = client
            self.expiry_time = 60*60*24*7
        except:
            raise HTTPException("could not instantiate session manager")


        
    def new_session(self,data=""):
        key = secrets.token_urlsafe()
        self.client.set(key,json.dumps(data))
        self.client.setex(key,self.expiry_time, json.dumps(data))
        return key
            
    def get_session(self,session_key):
        if(not self.client.exists(session_key)):
            raise HTTPException(401,"Session key does not exist")
        return json.loads(self.client.get(session_key))
    

    def update_session(self,session_key,data):
        if(not self.client.exists(session_key)):
            raise HTTPException("Session key does not exist")
        self.client.set(session_key,json.dumps(data))

    def close_session(self,session_key):
        self.client.delete(session_key)