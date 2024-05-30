from pydantic import BaseModel, Field
from fastapi import Query
class SearchQueryParams(BaseModel):
    max_results: int = Query(default=10,gt=0)
    threshold : float = Query(default=0,ge=0,le=1)


class SimilarityQueryParams(BaseModel):
    max_results: int = Query(default=10,gt=0)
    threshold : float = Query(default=0,ge=0,le=1)


class SearchSessionConfig(BaseModel):
    max_results: int = Query(10,gt=1)
    threshold : float = Query(0.5,ge=0,le=0.7)
    minRequests: int = Query(2,ge=0,le=20)
    maxRequests: int = Query(5,ge=0,le=20)
    


class RenameTopicBody(BaseModel):
    name: str = Field(...,min_length=1)

class SearchBody(BaseModel):
    input: str = Field(...,min_length=1)