# backend/app/reddit_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

def fetch_user_data(reddit_url: str) -> dict:
    # configure headless Chromium
    options = webdriver.ChromeOptions()
    # point at the system‐installed Chromium
    # on Render (Debian) this lives at /usr/bin/chromium
    chrome_path = os.getenv("CHROME_PATH", "/usr/bin/chromium")
    options.binary_location = chrome_path

    # headless & no‐sandbox flags required in many container environments
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1024")

    # webdriver‐manager will pull down a matching chromedriver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(reddit_url)
        time.sleep(2)  # wait for JS to render

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        username = reddit_url.rstrip("/").split("/")[-1]
        posts, comments = [], []

        for post in soup.select("div.Post"):
            title   = post.select_one("h3")
            content = post.select_one("p")
            sr      = post.select_one("a[data-click-id=subreddit]")
            posts.append({
                "subreddit": sr.text if sr else "",
                "title":     title.text if title else "",
                "content":   content.text if content else ""
            })

        for comment in soup.select("div.Comment"):
            sr   = comment.select_one("a[data-click-id=subreddit]")
            body = comment.select_one("div[data-test-id=comment]")
            comments.append({
                "subreddit": sr.text if sr else "",
                "content":   body.text if body else ""
            })

        return {
            "username": username,
            "posts":    posts,
            "comments": comments,
        }
    finally:
        driver.quit()
