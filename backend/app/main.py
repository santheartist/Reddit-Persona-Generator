# backend/app/main.py

from fastapi import FastAPI, HTTPException
import os
from fastapi.staticfiles import StaticFiles
from .models.reddit_user    import RedditProfileRequest
from .reddit_scraper        import fetch_user_data
from .persona_generator     import generate_persona
from .utils                 import generate_avatar_image

app = FastAPI()
app.mount(
    "/avatars",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static", "img")),
    name="avatars",
)
def save_persona_text(username: str, persona_md: str) -> str:
    out = os.path.join(os.path.dirname(__file__), "static", "output")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, f"{username}_persona.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(persona_md)
    return path

@app.post("/generate-persona/")
async def gen_persona(req: RedditProfileRequest):
    try:
        # 1) Scrape & GPT → markdown, citations, fields
        user_data       = await fetch_user_data(req.reddit_url)
        persona_md, citations, fields = generate_persona(user_data)

        # 2) Save markdown
        txt_path = save_persona_text(fields["name"], persona_md)

        # 3) Generate custom 416×416 avatar
        avatar_filename = f"{fields['name']}_avatar.png"
        avatar_path     = os.path.join(
            os.path.dirname(__file__), "static", "img", avatar_filename
        )
        generated = generate_avatar_image(fields, avatar_path)
        if generated:
            avatar_url = f"http://127.0.0.1:8000/avatars/{avatar_filename}"
        else:
            # fall back to stock
            avatar_url = f"http://127.0.0.1:8000/avatars/default_avatar.png"

        # 4) Return everything
        return {
            "persona":      persona_md,
            "citations":    citations,
            "fields":       fields,
            "avatar_url":  avatar_url,
            "saved_txt_to": txt_path,
            "avatar_file":  avatar_filename,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health():
    return {"status":"ok"}
