from pydantic import BaseModel


class RedditProfileRequest(BaseModel):
    reddit_url: str
