# Reddit Persona Generator

Generate a detailed UX-style persona from any public Reddit profile, complete with text summary, citations, and a dynamically generated avatar.

---

## 🔧 Features

- **FastAPI backend** scrapes recent posts & comments via Selenium, uses OpenAI GPT-4 to infer persona details  
- **Flask frontend** displays a clean Bootstrap-powered persona card  
- **Custom avatar** generated on-the-fly by DALL·E 3 based on inferred traits  
- **Export options**: print/PDF fallback or “Download” button to save the card as PNG  

---

## 🚀 Getting Started

### 1. Clone the repo  
~~~bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
~~~

### 2. Create and populate your `.env` files  

**backend/.env**
~~~ini
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_user_agent
OPENAI_API_KEY=sk-…
~~~

**frontend/.env** (if needed)
~~~ini
BACKEND_URL=http://127.0.0.1:8000
~~~

### 3. Install dependencies  

**Backend**
~~~bash
cd backend
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
~~~

**Frontend**
~~~bash
cd ../frontend
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
~~~

### 4. Run locally  

**Start the backend**
~~~bash
cd backend
uvicorn app.main:app --reload
~~~

**Start the frontend**
~~~bash
cd frontend
python app.py
~~~

Open your browser at **http://127.0.0.1:5000** (Flask) or **http://127.0.0.1:8501** (Streamlit), depending on which you use.

---

## 📂 Project Structure
~~~text
/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── reddit_scraper.py
│   │   ├── persona_generator.py
│   │   ├── utils.py
│   │   ├── models/reddit_user.py
│   │   ├── templates/        # Jinja2 HTML for print/PDF fallback
│   │   └── static/
│   │       ├── img/          # default_avatar.png
│   │       └── output/       # generated .txt and .png files
│   └── requirements.txt
│
├── frontend/
│   ├── app.py                # Flask or Streamlit
│   ├── templates/            # form.html & persona.html
│   ├── static/img/           # default_avatar.png
│   └── requirements.txt
│
├── .gitignore
└── README.md
~~~

---

## ⚙️ Environment Variables

`REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` – for PRAW/Selenium  
`OPENAI_API_KEY` – for GPT-4 and DALL·E image generation  
`BACKEND_URL` (frontend) – points to your FastAPI server  

---

## 📦 Deployment

Push to GitHub, then create two services on Render (or your host):

| Service | Runtime | Start Command |
|---------|---------|---------------|
| **Backend** | Python 3 | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Frontend** | Python 3 | `python app.py` |

Add your `.env` variables in each service’s dashboard.

---

## 📝 Usage

1. Enter a Reddit user URL (`https://reddit.com/user/username`).  
2. Click **Generate Persona**.  
3. View the text summary with citations, a styled persona card, and download or print as needed.  

---

## 🛠️ Troubleshooting

- **Quota errors** → check your OpenAI billing dashboard.  
- **Chromedriver issues** → ensure `webdriver-manager` can install or set `CHROME_PATH`.  
- **Missing templates** → confirm `backend/app/templates` and `frontend/templates` exist.  

---

## ⚖️ License

MIT © Sanchit Panda
