# backend/app/reddit_scraper.py

import os
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

def fetch_user_data(reddit_url: str) -> dict:
    username = reddit_url.rstrip("/").split("/")[-1]
    user = reddit.redditor(username)

    posts = [{
       "subreddit": str(sub.subreddit),
       "title":      sub.title,
       "content":    sub.selftext or ""
    } for sub in user.submissions.new(limit=10)]

    comments = [{
       "subreddit": str(c.comment.subreddit),
       "content":   c.body
    } for c in user.comments.new(limit=10)]

    return {
        "username": username,
        "posts":    posts,
        "comments": comments
    }
