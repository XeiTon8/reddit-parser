from pydantic import BaseModel
from typing import List

class RequestItem(BaseModel):
    subreddit: str
    keywords: List[str]

class ParseRequest(BaseModel):
    items: List[RequestItem]
    limit: int

class ResponseItem(BaseModel):
    title: str
    has_image: bool

class SubredditResult(BaseModel):
    subreddit: str
    posts: List[ResponseItem]

class ParseResponse(BaseModel):
    items: List[SubredditResult]