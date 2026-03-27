import httpx
import asyncio

from app.utils.logger import logger

MAX_RETRIES = 3
BASE_DELAY = 0.5

async def fetch_posts(subreddit: str, limit: int, retries: int = MAX_RETRIES):

    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url, headers=headers)

            if  res.status_code == 404:
                raise Exception("Subreddit not found")
            
            if  res.status_code in (429, 500, 502, 503, 504):
                raise Exception(f"Retry status: {res.status_code}")

            data = res.json()

            posts = []

            for item in data["data"]["children"]:
                post_data = item["data"]

                has_image = False

                if post_data.get("is_gallery") and post_data.get("media_metadata"):
                   has_image = True

    
                elif post_data.get("url", "").endswith((".jpg", ".png", ".jpeg")):
                     has_image = True

                posts.append({
                    "title": post_data["title"],
                    "selftext": post_data.get("selftext", ""),
                    "has_image": has_image
                })

            return posts
        
    except Exception as e:

        if retries > 0:
            logger.warning(f"Retrying {subreddit}, retries left: {retries}")
            await asyncio.sleep(BASE_DELAY * (2 ** (MAX_RETRIES - retries)))
            return await fetch_posts(subreddit, limit, retries - 1)
        
        raise Exception(f"Failed to fetch {subreddit}: {e}")
