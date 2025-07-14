# backend/app/persona_generator.py

import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_persona(user_data):
    """
    Returns:
      - persona_md: markdown summary (for .txt save)
      - citations:   list[str]
      - fields:      dict with exactly these keys:
          name, age, occupation, status, location, tier,
          archetype, traits (4), behaviour[], motivations[],
          frustrations[], goals[], citations[]
    """
    username = user_data["username"]
    snippets = []

    # include up to 5 posts & 5 comments
    for p in user_data.get("posts", [])[:5]:
        snippets.append(f"Post in r/{p['subreddit']}: {p['title']} {p['content']}")
    for c in user_data.get("comments", [])[:5]:
        snippets.append(f"Comment in r/{c['subreddit']}: {c['content']}")
    
    # optionally include profile "about" if you scraped it
    bio = user_data.get("about", "")
    if bio:
        snippets.insert(0, f"Profile bio: {bio}")

    snippet_str = "\n".join(snippets)

    # cleaned-up prompt (no leading '-' on any line)
    prompt = (
        "You are a UX researcher. Given the Reddit profile data below (including bio, karma, cake-day) "
        "and up to 5 posts/comments, infer a realistic user persona. For each field:\n"
        "  • If the user states it explicitly, capture it exactly.\n"
        "  • Otherwise, make an educated guess (e.g. “late-20s”, “Single”, “Mid-level Enthusiast”),\n"
        "    based on their activity and tone.\n"
        "Output only strict JSON (no code fences) with exactly these keys:\n"
        "  age (string),\n"
        "  occupation (string),\n"
        "  status (string),\n"
        "  location (string),\n"
        "  tier (string),\n"
        "  archetype (string),\n"
        "  traits (array of 4 short descriptors),\n"
        "  behaviour (array of bullet strings),\n"
        "  motivations (array of bullet strings),\n"
        "  frustrations (array of bullet strings),\n"
        "  goals (array of bullet strings),\n"
        "  citations (array of strings).\n\n"
        f"Profile:\n"
        f"  Username:    {username}\n"
        f"  Bio:         {bio}\n"
        f"  Karma:       {user_data.get('karma','')}\n"
        f"  CakeDay:     {user_data.get('cake_day','')}\n\n"
        f"Recent Activity Snippets:\n{snippet_str}\n"
    )

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"Output strict JSON only."},
            {"role":"user",  "content":prompt}
        ],
        temperature=0.3,
        max_tokens=450,
    )
    raw = resp.choices[0].message.content.strip()

    # extract the JSON blob
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(f"Could not find JSON in LLM output:\n{raw}")
    data = json.loads(m.group(0))

    # force the name to be the Reddit username
    data["name"] = username

    # build a simple markdown summary for your text file
    persona_md = (
        f"- **Name (Reddit Username):** {username}\n\n"
        f"- **Behaviour:**\n"
        + "\n".join(f"  • {b}" for b in data["behaviour"]) + "\n\n"
        f"- **Motivations:**\n"
        + "\n".join(f"  • {m}" for m in data["motivations"]) + "\n\n"
        f"- **Frustrations:**\n"
        + "\n".join(f"  • {f}" for f in data["frustrations"]) + "\n\n"
        "**Citations:**\n"
        + "\n".join(f"- {c}" for c in data["citations"])
    )
    return persona_md, data.get("citations", []), data
