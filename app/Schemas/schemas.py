from pydantic import BaseModel, Field
from fastapi import Query
class SearchQueryParams(BaseModel):
    max_results: int = Query(default=10,gt=0)
    threshold : float = Query(default=0,ge=0,le=1)


class SimilarityQueryParams(BaseModel):
    max_results: int = Query(default=10,gt=0)
    threshold : float = Query(default=0,ge=0,le=1)


class SearchSessionConfig(BaseModel):
    max_results: int = Query(...,gt=1)
    threshold : float = Query(...,ge=0,le=0.7)
    

class SearchBody(BaseModel):
    input: str = Field(...,min_length=1)