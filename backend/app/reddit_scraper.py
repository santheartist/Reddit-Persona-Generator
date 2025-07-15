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
        ],
    )
    page = await browser.newPage()
    await page.goto(url, {"waitUntil": "networkidle2"})
    content = await page.content()
    await browser.close()
    return content

def fetch_user_data(reddit_url: str) -> dict:
    """
    Uses a fresh asyncio event loop to drive Pyppeteer, then
    falls back to BeautifulSoup for scraping the rendered HTML.
    """
    # 1) Spin up a brand-new event loop for Pyppeteer
    loop = asyncio.new_event_loop()
    try:
        html = loop.run_until_complete(_get_page_content(reddit_url))
    finally:
        loop.close()

    # 2) Parse with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    username = reddit_url.rstrip("/").split("/")[-1]

    posts, comments = [], []
    for post in soup.select("div.Post")[:5]:
        title_el   = post.select_one("h3")
        content_el = post.select_one("p")
        sr_el      = post.select_one("a[data-click-id=subreddit]")
        posts.append({
            "subreddit": sr_el.text if sr_el else "",
            "title":     title_el.text if title_el else "",
            "content":   content_el.text if content_el else ""
        })

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
