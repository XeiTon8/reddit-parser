from fastapi import APIRouter
import asyncio

from app.models.schemas import ParseRequest, ParseResponse, SubredditResult

from app.services.reddit_service import fetch_posts
from app.services.filter_service import filter_posts
from app.utils.logger import logger

router = APIRouter()

semaphore = asyncio.Semaphore(5)

async def try_fetch(subreddit: str, limit: int):
    async with semaphore:
        return await fetch_posts(subreddit, limit)

@router.post("/parse", response_model=ParseResponse)
async def analyze(data: ParseRequest):

    logger.info(f"Request received, data: {data}")

    result = []

    tasks = [
        try_fetch(item.subreddit.replace("r/", ""), data.limit)
        for item in data.items
    ]

    posts_results = await asyncio.gather(*tasks, return_exceptions=True)

    for item, posts in zip(data.items, posts_results):
        sub = item.subreddit.replace("r/", "")
        keywords = item.keywords

        if isinstance(posts, Exception):
            logger.error(f"Error for {sub}: {posts}")
            result.append(
            SubredditResult(subreddit=sub, posts=[])
        )
            continue

        filtered = filter_posts(posts, keywords)
        
        result.append(
        SubredditResult(
            subreddit=sub,
            posts=filtered
        ))

    return ParseResponse(items = result)