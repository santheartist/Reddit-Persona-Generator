import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(
    __name__,
    static_folder="static",        # where your /static/img/default_avatar.png lives
    template_folder="templates",   # where form.html & persona.html will live
)

BACKEND_URL = "http://127.0.0.1:8000/generate-persona/"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        reddit_url = request.form.get("reddit_url", "").strip()
        if not reddit_url:
            return render_template("form.html", error="Please enter a Reddit URL.")

        resp = requests.post(
            BACKEND_URL,
            json={"reddit_url": reddit_url}
        )
        if resp.status_code != 200:
            return render_template(
                "form.html",
                error=f"Backend error: {resp.text}"
            )

        result = resp.json()
        # pull out the structured fields your backend now returns
        fields = result.get("fields", {
            "name": "", "age":"", "occupation":"",
            "status":"", "location":"", "tier":"",
            "archetype":"", "traits":[],
            "behaviours":[], "motivations":[],
            "frustrations":[], "goals":[]
        })

        fields     = result["fields"]
        avatar_url = result.get("avatar_url", url_for("static", filename="img/default_avatar.png"))
        return render_template("persona.html",
                                fields=fields,
                                avatar_url=avatar_url)
 
    # GET → show the simple entry form
    return render_template("form.html", error=None)


if __name__ == "__main__":
    app.run(debug=True)
