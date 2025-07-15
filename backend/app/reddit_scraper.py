# reddit_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def fetch_user_data(reddit_url: str) -> dict:
    # 1) configure your ChromeOptions as before
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # any other options…

    # 2) wrap the driver binary in a Service
    service = Service(ChromeDriverManager().install())

    # 3) pass service=… instead of executable_path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(reddit_url)
        time.sleep(2)  # give the JS some time to load

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # … your existing logic to extract posts/comments …
        username = reddit_url.rstrip("/").split("/")[-1]
        posts = []
        for post in soup.select("div.Post"):
            title = post.select_one("h3")
            content = post.select_one("p")
            posts.append({
                "subreddit": post.select_one("a[data-click-id=subreddit]").text,
                "title":    title.text if title else "",
                "content":  content.text if content else ""
            })

        comments = []
        for comment in soup.select("div.Comment"):
            subreddit = comment.select_one("a[data-click-id=subreddit]")
            body      = comment.select_one("div[data-test-id=comment]")
            comments.append({
                "subreddit": subreddit.text if subreddit else "",
                "content":   body.text if body else ""
            })

        return {
            "username": username,
            "posts":    posts,
            "comments": comments,
        }

    finally:
        driver.quit()
