# 💼 Resume Parser App (Flask + OpenAI + Bootstrap)

## 🧠 Objective  
The Resume Parser App allows recruiters and job seekers to evaluate resumes using AI. Upload a PDF resume and specify a target profession (e.g., "Backend Developer") — the app will parse the resume and assess the candidate using OpenAI GPT-3.5.  
It provides a detailed breakdown of:  
- Contact information  
- Work experience  
- Skills (technical + soft)  
- An AI-powered evaluation (score, recommendation, proceed/no decision)  
> Built with Flask, OpenAI, Bootstrap 5, and modern UI/UX design.

## 📸 Sneak Peek  
![App Screenshot](screenshots/1.png)  
![App Screenshot](screenshots/2.png)

## 📸 Deployment  
- Click on the following URL: **[App](https://resume-parser-tw8t.onrender.com)**

## 🚀 Features  
- Upload PDF resumes for analysis  
- Specify a target profession for role-based evaluation  
- AI-powered extraction of:  
  - Full Name, Email, GitHub, LinkedIn  
  - Employment History  
  - Technical and Soft Skills  
- Candidate Evaluation:  
  - Score out of 10  
  - Short recommendation  
  - Proceed or not  
- Light/Dark Mode Toggle with colorful 🌞 / 🌙 icons  
- Clean, structured JSON-like output  
- Responsive Bootstrap 5 UI with icons and transitions

## ⚙️ Tech Stack  
| Technology   | Use                           |
|--------------|------------------------------|
| Python 3.x    | Core backend logic           |
| Flask        | Lightweight web framework    |
| OpenAI GPT-3.5 | Resume parsing + evaluation |
| PyPDF        | PDF text extraction          |
| Bootstrap 5   | Responsive frontend styling |
| YAML         | API key configuration        |
| Jinja2       | HTML templating with Flask   |

## 📦 Installation & Setup  
Clone the Repository:  
    git clone https://github.com/your-username/resume-parser-ai.git  
    cd resume-parser-ai  

Set Up Virtual Environment:  
    python -m venv venv  
    # For macOS/Linux  
    source venv/bin/activate  
    # For Windows  
    venv\Scripts\activate  

Install Dependencies:  
    pip install -r requirements.txt  

Add Your OpenAI API Key – create a file named **config.yaml** in the root directory with:  
    OPENAI_API_KEY: "your-openai-api-key-here"  

You can get your API key from <https://platform.openai.com/account/api-keys>

Run the Flask App:  
    python app.py  

Open in your browser:  
Visit <http://localhost:8000>

## 🧪 How It Works  
1. Upload a PDF resume  
2. Enter a target profession (e.g., “Data Scientist”)  
3. AI extracts structured resume data  
4. AI evaluates if the candidate fits the role  
5. You receive:  
   - Parsed fields with icons  
   - Score out of 10  
   - Recommendation  
   - Proceed decision

## 📁 Project Structure  
resume-parser-ai/
├── app.py # Main Flask application
├── resumeparser.py # OpenAI resume parsing & evaluation logic
├── templates/
│ └── index.html # Bootstrap UI template with light/dark theme
├── static/
│ └── logo.png # App logo
├── screenshots/
│ └── 1.png # Screenshot for README
├── config.yaml # Your OpenAI API Key (you create this)
├── requirements.txt # Required Python packages
└── README.md # This file 📄


## 🙌 Contributing  
Contributions are welcome! To contribute:  
- Fork the project  
- Create a new branch:  
      git checkout -b feature/your-feature  
- Commit your changes  
- Open a Pull Request 🚀  

Ideas to improve:  
- Add .docx resume support  
- Add “Download as JSON” option  
- Evaluate multiple roles  
- Email feedback to the user

## 📄 License  
This project is licensed under the **MIT License**.  
You are free to use, distribute, and modify this project for personal or commercial use.

## 🙏 Credits  
- [OpenAI GPT-3.5](https://platform.openai.com/)  
- [Bootstrap 5](https://getbootstrap.com/)  
- [Flask](https://flask.palletsprojects.com/)  
- [PyPDF](https://pypi.org/project/pypdf/)  
- [Bootstrap Icons](https://icons.getbootstrap.com/)

