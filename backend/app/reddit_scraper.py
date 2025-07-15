# backend/app/reddit_scraper.py

import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def _get_page_content(url: str) -> str:
    browser = await launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=1280,1024",
        ]
    )
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "networkidle2"})
    content = await page.content()
    await browser.close()
    return content

def fetch_user_data(reddit_url: str) -> dict:
    """
    Uses Pyppeteer to load the Reddit profile page (so dynamic JS content is rendered),
    then falls back to BeautifulSoup to extract up to 5 posts & 5 comments.
    """
    html = asyncio.get_event_loop().run_until_complete(_get_page_content(reddit_url))
    soup = BeautifulSoup(html, "html.parser")

    username = reddit_url.rstrip("/").split("/")[-1]
    posts, comments = [], []

    # up to 5 latest submissions
    for post in soup.select("div.Post")[:5]:
        title_el   = post.select_one("h3")
        content_el = post.select_one("p")
        sr_el      = post.select_one("a[data-click-id=subreddit]")
        posts.append({
            "subreddit": sr_el.text if sr_el else "",
            "title":     title_el.text if title_el else "",
            "content":   content_el.text if content_el else ""
        })

    # up to 5 latest comments
    for comment in soup.select("div.Comment")[:5]:
        sr_el   = comment.select_one("a[data-click-id=subreddit]")
        body_el = comment.select_one("div[data-test-id=comment]")
        comments.append({
            "subreddit": sr_el.text if sr_el else "",
            "content":   body_el.text if body_el else ""
        })

    return {
        "username": username,
        "posts":    posts,
        "comments": comments,
    }
