from pydantic import BaseModel
from fastapi import Query
class SearchQueryParams(BaseModel):
    query: str = Query(...,min_length=3,max_length=4096)
    max_results: int = Query(default=10,gt=0)
    threshold : float = Query(default=0,ge=0,le=1)


class SimilarityQueryParams(BaseModel):
    max_results: int = Query(default=10,gt=0)
    threshold : float = Query(default=0,ge=0,le=1)