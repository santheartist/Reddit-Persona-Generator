import os
from jinja2 import Environment, FileSystemLoader
from pyppeteer import launch

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def _render_persona_html(fields: dict, html_path: str):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    tpl = env.get_template("persona.html")
    html = tpl.render(**fields)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

async def generate_persona_image_html(fields: dict, output_path: str):
    # 1) Write HTML
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_path = os.path.splitext(output_path)[0] + ".html"
    _render_persona_html(fields, html_path)

    # 2) Launch your local Chrome
    chrome = os.getenv("CHROME_PATH") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome):
        raise FileNotFoundError(f"Chrome not found at {chrome}")
    browser = await launch(executablePath=chrome, args=["--no-sandbox","--disable-setuid-sandbox"])

    # 3) Snapshot
    page = await browser.newPage()
    await page.setViewport({"width":2048,"height":1024})
    await page.goto(f"file://{os.path.abspath(html_path)}")
    await page.screenshot({"path": output_path})
    await browser.close()

    # 4) Cleanup
    os.remove(html_path)
    return output_path
