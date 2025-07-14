# backend/app/utils.py

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from PIL import Image

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_avatar_image(fields: dict, output_path: str) -> str:
    """
    Uses DALL·E to generate a 1024×1024 portrait based on persona fields,
    then resizes it to 416×416 and saves to output_path.
    """
    prompt = (
        f"Create a clean, photorealistic portrait headshot of a person with these traits:\n"
        f"- Age: {fields.get('age','unknown')}\n"
        f"- Occupation: {fields.get('occupation','unknown')}\n"
        f"- Location: {fields.get('location','unknown')}\n"
        f"- Personality descriptors: {', '.join(fields.get('traits',[]))}\n"
        "Neutral background, soft lighting, facing forward."
    )
    try:
        resp = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",    # ← correct size
            n=1
        )
        url      = resp.data[0].url
        img_data = requests.get(url).content

        im = Image.open(BytesIO(img_data)).convert("RGBA")
        im = im.resize((416, 416), Image.LANCZOS)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        im.save(output_path)
        return output_path

    except Exception as e:
        # if anything goes wrong, just let the caller know
        # and we can fall back on default_avatar.png
        print("Avatar generation failed:", e)
        return None
