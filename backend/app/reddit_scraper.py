# backend/app/reddit_scraper.py

import os
import asyncio
from asyncpraw import Reddit

reddit = Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


async def fetch_user_data(reddit_url: str) -> dict:
    username = reddit_url.rstrip("/").split("/")[-1]
    user = await reddit.redditor(username)

    posts = []
    async for submission in user.submissions.new(limit=10):
        posts.append({
            "title": submission.title,
            "content": submission.selftext,
            "subreddit": str(submission.subreddit),
        })

    comments = []
    async for comment in user.comments.new(limit=10):
        comments.append({
            "content": comment.body,
            "subreddit": str(comment.subreddit),
        })

    return {"username": username, "posts": posts, "comments": comments}
