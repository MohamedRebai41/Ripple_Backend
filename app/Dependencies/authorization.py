


import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader



api_key_header = APIKeyHeader(name="access_token", auto_error=False)
async def get_api_key(
    api_key: str = Security(api_key_header)
):
    API_KEY = os.getenv("API_KEY")
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")