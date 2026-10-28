"""
CareerCopilot AI 2.0  —  Computer Engineering Edition
Supports: Data Analytics · Data Science · Web Dev · Full Stack ·
          Backend · Frontend · DevOps · ML Engineering · Mobile Dev ·
          Cybersecurity · Cloud Engineering · UI/UX
Built with: Python · Streamlit · OpenRouter API
"""

import streamlit as st
from resume_parser import extract_resume_text
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerCopilot AI 2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS  — clean dark tech theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #07101e;
    background-image:
        linear-gradient(rgba(99,179,237,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,179,237,0.025) 1px, transparent 1px);
    background-size: 44px 44px;
}

[data-testid="stSidebar"] {
    background: #040d1a !important;
    border-right: 1px solid rgba(99,179,237,0.12) !important;
}

.cc-card {
    background: rgba(8,20,38,0.97);
    border: 1px solid rgba(99,179,237,0.14);
    border-radius: 14px;
    padding: 22px 24px;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
}
.cc-card::before {
    content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background: linear-gradient(90deg,var(--accent,#3b82f6),var(--accent2,#8b5cf6),transparent);
}
.cc-plain {
    background: rgba(8,20,38,0.97);
    border: 1px solid rgba(99,179,237,0.1);
    border-radius: 14px;
    padding: 20px 22px;
    margin: 8px 0;
}
.metric-box {
    background: rgba(8,20,38,0.97);
    border: 1px solid rgba(99,179,237,0.18);
    border-radius: 12px;
    padding: 18px 14px;
    text-align: center;
}
.pill {
    display:inline-block;
    background:rgba(59,130,246,0.1);
    border:1px solid rgba(59,130,246,0.3);
    border-radius:20px;padding:4px 13px;margin:3px;
    font-size:0.79rem;color:#93c5fd;font-family:'DM Mono',monospace;
}
.pill-miss {
    background:rgba(245,158,11,0.1);
    border:1px solid rgba(245,158,11,0.3);color:#fcd34d;
}
.sec-title {
    font-family:'Syne',sans-serif;font-size:1.0rem;font-weight:800;
    color:#e2e8f0;letter-spacing:.05em;text-transform:uppercase;
    margin:20px 0 12px;padding-left:10px;
    border-left:3px solid #3b82f6;
}
.chat-user {
    background:linear-gradient(135deg,#1d4ed8,#7c3aed);
    border-radius:16px 16px 4px 16px;
    padding:12px 18px;margin:8px 0 8px 15%;
    color:#f0f9ff;font-size:0.9rem;line-height:1.55;
}
.chat-ai {
    background:rgba(8,20,38,0.97);
    border:1px solid rgba(99,179,237,0.18);
    border-radius:16px 16px 16px 4px;
    padding:12px 18px;margin:8px 15% 8px 0;
    color:#cbd5e1;font-size:0.9rem;line-height:1.55;
}
.rank-row {
    display:flex;align-items:center;gap:14px;
    background:rgba(8,20,38,0.95);
    border:1px solid rgba(99,179,237,0.1);
    border-radius:12px;padding:14px 18px;margin:7px 0;
}
.stProgress > div > div {
    background:linear-gradient(90deg,#3b82f6,#8b5cf6) !important;
    border-radius:999px !important;
}
.stTabs [data-baseweb="tab-list"] {
    background:rgba(8,20,38,0.8);border-radius:10px;padding:4px;gap:4px;
}
.stTabs [data-baseweb="tab"] { border-radius:8px;color:#64748b;font-size:.87rem; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background:rgba(59,130,246,0.18);color:#60a5fa;
}
.stButton > button {
    background:linear-gradient(135deg,#1d4ed8,#7c3aed) !important;
    border:none !important;border-radius:9px !important;
    color:#f0f9ff !important;font-weight:600 !important;
    font-size:.87rem !important;padding:.5rem 1.4rem !important;
    transition:all .2s !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 6px 22px rgba(59,130,246,0.35) !important;
}
.stTextArea textarea, .stTextInput input {
    background:rgba(4,13,26,0.9) !important;color:#e2e8f0 !important;
    border:1px solid rgba(99,179,237,0.18) !important;border-radius:9px !important;
}
.stSelectbox > div > div {
    background:rgba(4,13,26,0.9) !important;
    border:1px solid rgba(99,179,237,0.18) !important;
    border-radius:9px !important;color:#e2e8f0 !important;
}
.streamlit-expanderHeader {
    background:rgba(8,20,38,0.8) !important;border-radius:10px !important;color:#94a3b8 !important;
}
.stDownloadButton > button {
    background:rgba(59,130,246,0.1) !important;
    border:1px solid rgba(59,130,246,0.35) !important;
    color:#60a5fa !important;border-radius:9px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ██  MASTER SKILL + ROLE DATABASE  (all CS/CE fields)
# ─────────────────────────────────────────────────────────────

ALL_SKILLS = [
    # ── Data / Analytics ──────────────────────────────
    "Python","SQL","R","Excel","Power BI","Tableau","Looker",
    "Pandas","NumPy","Matplotlib","Seaborn","Plotly",
    "Statistics","Machine Learning","Deep Learning","Scikit-learn",
    "TensorFlow","PyTorch","Keras","XGBoost","LightGBM",
    "Regression","Classification","Clustering","A/B Testing",
    "Hypothesis Testing","Forecasting","NLP","Computer Vision",
    "ETL","Data Warehousing","Data Cleaning","Data Modeling","EDA",
    "BigQuery","Snowflake","Redshift","dbt","Airflow","Spark","Hadoop",
    "DAX","Power Query","Google Data Studio","Metabase","SSRS",
    "MySQL","PostgreSQL","SQLite","MongoDB","Oracle","SSMS",
    "KPI Reporting","Dashboard Design","Data Storytelling","Business Intelligence",
    # ── Web / Frontend ────────────────────────────────
    "HTML","CSS","JavaScript","TypeScript","React","Next.js",
    "Vue.js","Angular","Svelte","Tailwind","Bootstrap","SASS",
    "Redux","GraphQL","Webpack","Vite","Storybook",
    # ── Backend ───────────────────────────────────────
    "Node.js","Express","Django","Flask","FastAPI","Spring Boot",
    "Ruby on Rails","Laravel","REST API","JWT","OAuth","Redis",
    "Celery","RabbitMQ","Kafka","gRPC","WebSockets",
    # ── Database ──────────────────────────────────────
    "Firebase","Supabase","DynamoDB","Cassandra","Elasticsearch",
    # ── DevOps / Cloud ────────────────────────────────
    "Docker","Kubernetes","CI/CD","Linux","Bash","Terraform",
    "AWS","Azure","GCP","Ansible","Jenkins","GitHub Actions",
    "Nginx","Prometheus","Grafana","ELK Stack",
    # ── Mobile ────────────────────────────────────────
    "React Native","Flutter","Swift","Kotlin","Android","iOS",
    "Expo","Xcode","Android Studio",
    # ── General Engineering ───────────────────────────
    "Java","C++","C#","C","Go","Rust","PHP","Scala","Dart",
    "Git","GitHub","GitLab","JIRA","Agile","Scrum",
    "System Design","Microservices","OOP","Design Patterns",
    # ── Cybersecurity ─────────────────────────────────
    "Penetration Testing","Ethical Hacking","Network Security",
    "OWASP","Burp Suite","Nmap","Wireshark","Metasploit",
    "SIEM","SOC","Cryptography","Incident Response",
    # ── Cloud / ML Ops ────────────────────────────────
    "MLflow","Kubeflow","Vertex AI","SageMaker","MLOps",
    "Feature Engineering","Model Deployment","Data Pipelines",
    # ── UI/UX ─────────────────────────────────────────
    "Figma","Adobe XD","Sketch","InVision","Zeplin",
    "UI/UX","Wireframing","Prototyping","User Research",
]

# ── Role ➜ required skills mapping (one per field) ──────────
ROLE_SKILLS = {
    # ── Analytics & Data ──────────────────────────────────
    "Data Analyst": [
        "SQL","Excel","Python","Power BI","Tableau",
        "Pandas","Statistics","EDA","Data Cleaning",
        "Dashboard Design","KPI Reporting",
    ],
    "Business Analyst": [
        "SQL","Excel","Power BI","Tableau","Business Intelligence",
        "Statistics","JIRA","Data Storytelling","KPI Reporting",
        "Google Data Studio","Data Modeling",
    ],
    "BI Developer": [
        "Power BI","DAX","Power Query","SQL","Tableau",
        "Data Warehousing","ETL","SSRS","Data Modeling",
        "Looker","Snowflake",
    ],
    "Data Scientist": [
        "Python","Machine Learning","Deep Learning","Scikit-learn",
        "TensorFlow","Pandas","NumPy","SQL","Statistics",
        "A/B Testing","Forecasting","NLP",
    ],
    "Data Engineer": [
        "Python","SQL","ETL","Spark","Airflow",
        "dbt","BigQuery","Snowflake","AWS","Data Warehousing",
        "Data Pipelines","Kafka",
    ],
    "ML Engineer": [
        "Python","Machine Learning","TensorFlow","PyTorch","MLOps",
        "Docker","AWS","Kubernetes","Feature Engineering",
        "Model Deployment","Scikit-learn","MLflow",
    ],
    "MIS Analyst": [
        "Excel","SQL","Power BI","KPI Reporting","DAX",
        "Data Cleaning","Google Data Studio","SSRS","Data Modeling",
        "Business Intelligence",
    ],
    # ── Web & Software ────────────────────────────────────
    "Frontend Developer": [
        "HTML","CSS","JavaScript","TypeScript","React",
        "Next.js","Tailwind","Bootstrap","Redux","Git",
    ],
    "Backend Developer": [
        "Node.js","Express","Python","Django","REST API",
        "PostgreSQL","MongoDB","Redis","JWT","Docker","Git",
    ],
    "Full Stack Developer": [
        "HTML","CSS","JavaScript","React","Node.js",
        "Express","MongoDB","REST API","TypeScript","Git",
        "Docker","PostgreSQL",
    ],
    "Software Engineer": [
        "Python","Java","C++","Data Structures","Algorithms",
        "OOP","Design Patterns","Git","System Design",
        "REST API","SQL","Docker",
    ],
    # ── Infrastructure & Security ─────────────────────────
    "DevOps Engineer": [
        "Docker","Kubernetes","CI/CD","Linux","AWS",
        "Terraform","Ansible","Jenkins","GitHub Actions",
        "Prometheus","Grafana","Bash",
    ],
    "Cloud Engineer": [
        "AWS","Azure","GCP","Docker","Kubernetes",
        "Terraform","CI/CD","Linux","Networking",
        "Security","IAM","Serverless",
    ],
    "Cybersecurity Analyst": [
        "Network Security","OWASP","Penetration Testing",
        "Burp Suite","Nmap","SIEM","SOC","Cryptography",
        "Linux","Incident Response","Python","Wireshark",
    ],
    # ── Mobile & Design ───────────────────────────────────
    "Mobile Developer": [
        "React Native","Flutter","Swift","Kotlin",
        "Android","iOS","JavaScript","TypeScript","Git","Firebase",
    ],
    "UI/UX Designer": [
        "Figma","Adobe XD","UI/UX","Wireframing","Prototyping",
        "User Research","HTML","CSS","Sketch","Zeplin",
    ],
}

# ── Field groupings for domain detection ────────────────────
FIELD_GROUPS = {
    "Data & Analytics": ["Data Analyst","Business Analyst","BI Developer","MIS Analyst"],
    "Data Science & AI": ["Data Scientist","ML Engineer","Data Engineer"],
    "Web Development": ["Frontend Developer","Backend Developer","Full Stack Developer"],
    "Software Engineering": ["Software Engineer"],
    "Infrastructure": ["DevOps Engineer","Cloud Engineer","Cybersecurity Analyst"],
    "Mobile & Design": ["Mobile Developer","UI/UX Designer"],
}

# ── ATS sections to check ────────────────────────────────────
ATS_SECTIONS = {
    "Professional Summary": ["summary","profile","objective","about"],
    "Skills":               ["skills","technical skills","tools","competencies","technologies"],
    "Projects":             ["projects","project","portfolio","work samples"],
    "Experience":           ["experience","work experience","internship","employment"],
    "Education":            ["education","degree","university","college","b.tech","mba","b.sc","bca","mca","bsc"],
    "Certifications":       ["certification","certifications","certificate","credential"],
    "LinkedIn":             ["linkedin.com"],
    "GitHub / Portfolio":   ["github.com","kaggle.com","portfolio","behance","dribbble"],
}

# ── Courses per role ─────────────────────────────────────────
COURSES = {
    "Data Analyst":         [("Google Data Analytics","Coursera","Best overall"),("SQL Bootcamp","Udemy","Hands-on SQL"),("Power BI Full Course","Udemy","Top-rated BI"),("Python for DA","DataCamp","DA-specific Python"),("Tableau A–Z","Udemy","Practical Tableau")],
    "Data Scientist":       [("ML Specialization – Andrew Ng","Coursera","Gold standard"),("Applied DS with Python","Coursera","U Michigan"),("Kaggle ML Courses","Kaggle","Free & hands-on"),("Deep Learning Spec","Coursera","Neural networks"),("Fast.ai","Fast.ai","Top-down DL")],
    "ML Engineer":          [("MLOps Specialization","Coursera","Production ML"),("Docker for ML","Udemy","Containerise models"),("AWS ML Specialty","Udemy","Cloud ML"),("Feature Engineering","Kaggle","Free course"),("Kubeflow Pipelines","Udemy","ML orchestration")],
    "Data Engineer":        [("DE Zoomcamp","DataTalks.Club","Free project-based"),("Apache Spark","Udemy","PySpark"),("dbt Fundamentals","dbt Learn","Free official"),("Airflow Fundamentals","Astronomer","Free"),("AWS Data Analytics","Udemy","Cloud DE cert")],
    "BI Developer":         [("PL-300 Power BI","Microsoft Learn","Official cert"),("DAX Deep Dive","SQLBI","Best DAX resource"),("Data Warehousing","Udemy","DWH concepts"),("Tableau Desktop Spec","Tableau","Official cert"),("ETL with Python","DataCamp","Pipelines")],
    "Frontend Developer":   [("The Web Dev Bootcamp","Udemy","HTML/CSS/JS"),("React – Complete Guide","Udemy","Top React course"),("Next.js Full Stack","Udemy","SSR & APIs"),("TypeScript Handbook","Microsoft","Free official"),("CSS for JS Devs","Josh Comeau","Modern CSS")],
    "Backend Developer":    [("Node.js Complete Guide","Udemy","Node + Express"),("Django REST Framework","Udemy","Python backend"),("PostgreSQL Bootcamp","Udemy","Databases"),("Docker Mastery","Udemy","Containerisation"),("System Design Primer","GitHub","Free, essential")],
    "Full Stack Developer": [("Full Stack Open","Helsinki Uni","Free, project-based"),("MERN Stack F2B","Udemy","Mongo/Express/React/Node"),("Next.js Full Stack","Udemy","Production apps"),("The Odin Project","The Odin Project","Free curriculum"),("GraphQL with React","Udemy","Modern APIs")],
    "Software Engineer":    [("DSA – Abdul Bari","Udemy","Best DSA course"),("System Design Interview","Udemy","Essential"),("Clean Code","O'Reilly Book","Must read"),("Design Patterns","Refactoring.Guru","Free"),("LeetCode 75","LeetCode","Interview prep")],
    "DevOps Engineer":      [("DevOps Beginner–Advanced","Udemy","Full roadmap"),("Docker Mastery","Udemy","Industry standard"),("Kubernetes for Beginners","Udemy","K8s basics"),("AWS Solutions Architect","Udemy","Most popular cert"),("Terraform on AWS","Udemy","IaC")],
    "Cloud Engineer":       [("AWS Cloud Practitioner","Udemy","Start here"),("Azure Fundamentals AZ-900","Microsoft","Free learning path"),("GCP Associate CE","Coursera","Google Cloud"),("Terraform Associate","HashiCorp","IaC cert"),("Cloud Networking","Udemy","Networking for cloud")],
    "Cybersecurity Analyst":[("Google Cybersecurity Cert","Coursera","Best starter"),("CompTIA Security+","Udemy","Industry cert"),("Ethical Hacking","Udemy","Penetration testing"),("TryHackMe","TryHackMe","Hands-on labs"),("OWASP Top 10","OWASP","Free, essential")],
    "Mobile Developer":     [("Flutter Complete Guide","Udemy","Best Flutter"),("React Native Practical","Udemy","Cross-platform"),("iOS & Swift Bootcamp","Udemy","Apple dev"),("Android Kotlin Dev","Udemy","Android"),("Firebase for Mobile","Firebase Docs","Backend for mobile")],
    "UI/UX Designer":       [("Google UX Design","Coursera","Most recognised"),("Figma UI Design","Udemy","Tool mastery"),("UX Research","Interaction Design Fdn","Deep UX"),("Design Systems","Udemy","Scale your design"),("UI Fundamentals","Scrimba","Free, practical")],
    "Business Analyst":     [("Business Analytics Spec","Coursera","Wharton-backed"),("SQL for BAs","DataCamp","BA-focused"),("Advanced Excel","Udemy","Power user Excel"),("Power BI for Business","Microsoft","Free official"),("Agile BA","Udemy","Agile workflows")],
    "MIS Analyst":          [("Advanced Excel & Dash","Udemy","Excel power user"),("SQL for MIS","Udemy","Reporting SQL"),("Power BI for MIS","Microsoft Learn","Free"),("SSRS Services","Udemy","Enterprise reporting"),("KPI Dashboard Design","LinkedIn Learning","Visual best practices")],
}

# ── Interview question bank (universal CS + field-specific) ──
INTERVIEW_QS = {
    "Data & Analytics — SQL": [
        "What is the difference between WHERE and HAVING?",
        "Explain RANK(), DENSE_RANK(), and ROW_NUMBER() with an example.",
        "How do you find the second highest salary in a table?",
        "What are CTEs and when would you use one over a subquery?",
        "Explain the difference between UNION and UNION ALL.",
        "How do you handle NULL values in SQL aggregations?",
        "Write a query to find duplicate records in a table.",
        "What are window functions? Give a real-world use case.",
    ],
    "Data & Analytics — Python / Pandas": [
        "What is the difference between .loc and .iloc in Pandas?",
        "How do you handle missing values in a DataFrame?",
        "How do you merge two DataFrames? What merge types exist?",
        "How would you detect and remove outliers in Python?",
        "Explain list comprehension with a data cleaning example.",
        "What is the difference between apply() and map()?",
        "How do you pivot a DataFrame in Pandas?",
    ],
    "Data & Analytics — Statistics": [
        "Explain p-value in plain English.",
        "What is the difference between Type I and Type II errors?",
        "How would you design an A/B test for a new feature?",
        "What is the Central Limit Theorem and why does it matter?",
        "When would you use a t-test vs. ANOVA?",
        "Explain correlation vs. causation with an example.",
        "What is overfitting and how do you prevent it?",
    ],
    "Web Dev — JavaScript / React": [
        "What is the difference between var, let, and const?",
        "Explain the event loop in JavaScript.",
        "What are React hooks? Explain useState and useEffect.",
        "What is the virtual DOM and how does React use it?",
        "What is closure in JavaScript? Give an example.",
        "Explain async/await vs Promises.",
        "What is the difference between controlled and uncontrolled components in React?",
        "How does CSS specificity work?",
    ],
    "Web Dev — Backend / APIs": [
        "What is REST? What are its core principles?",
        "Explain the difference between SQL and NoSQL databases.",
        "What is JWT? How does token-based authentication work?",
        "What is the difference between PUT and PATCH?",
        "How do you handle rate limiting in an API?",
        "Explain database indexing and when you would use it.",
        "What is middleware in Express/Django?",
        "How do you prevent SQL injection?",
    ],
    "DevOps & Cloud": [
        "What is Docker and how does it differ from a VM?",
        "Explain Kubernetes — what problems does it solve?",
        "What is CI/CD? Describe a pipeline you would set up.",
        "What is Infrastructure as Code? Name a tool for it.",
        "Explain the difference between horizontal and vertical scaling.",
        "What is a Load Balancer and how does it work?",
        "What are the core AWS services every cloud engineer should know?",
    ],
    "Software Engineering — DSA": [
        "What is the time complexity of binary search?",
        "Explain the difference between a stack and a queue.",
        "What is dynamic programming? Give an example.",
        "How does a hash map work internally?",
        "Explain BFS vs DFS and when to use each.",
        "What is the difference between a tree and a graph?",
        "What is memoisation?",
    ],
    "Software Engineering — System Design": [
        "How would you design a URL shortener like bit.ly?",
        "Design a notification system for millions of users.",
        "How would you design Twitter's feed?",
        "Explain CAP theorem.",
        "How does a CDN work?",
        "How would you design a rate limiter?",
        "What is eventual consistency?",
    ],
    "HR & Behavioural (All Fields)": [
        "Tell me about yourself and your journey into tech.",
        "Describe a challenging project and how you handled it.",
        "How do you keep up with the latest tech trends?",
        "Tell me about a time you disagreed with a teammate.",
        "How do you prioritise tasks under deadlines?",
        "Where do you see yourself in 3 years?",
        "Why do you want this specific role?",
        "Describe a time you learned something outside your comfort zone.",
    ],
}

# ── Portfolio project ideas per field ────────────────────────
PROJECTS = {
    "Data Analyst":         [("Sales Dashboard","Power BI/Tableau dashboard with KPIs","Power BI · SQL · Excel"),("Customer Segmentation","RFM analysis and clustering","Python · Pandas · K-Means"),("HR Attrition EDA","Explore factors behind employee turnover","Python · Seaborn"),("Superstore Analysis","Deep dive on Kaggle Superstore dataset","Python · Tableau")],
    "Data Scientist":       [("House Price Predictor","Regression model on Kaggle dataset","Python · Scikit-learn"),("Sentiment Analyser","NLP on product reviews","Python · NLTK"),("Credit Risk Model","Loan default classification","Python · XGBoost"),("Time Series Forecast","Sales forecasting with Prophet","Python · Prophet")],
    "ML Engineer":          [("End-to-End ML Pipeline","Train → containerise → deploy a model","Python · Docker · AWS"),("Real-time Prediction API","FastAPI serving an ML model","FastAPI · Scikit-learn"),("MLflow Experiment Tracker","Track experiments with MLflow","MLflow · Python")],
    "Frontend Developer":   [("Portfolio Website","Personal site with animations","React · Tailwind"),("E-commerce UI","Product listing, cart, checkout","React · TypeScript · Redux"),("Weather App","Live weather with API integration","React · JavaScript · REST API")],
    "Backend Developer":    [("REST API with Auth","Full CRUD API with JWT","Node.js · Express · MongoDB"),("Task Manager API","Todo app backend with tests","Django · PostgreSQL"),("Real-time Chat","WebSocket-based chat server","Node.js · Socket.io")],
    "Full Stack Developer": [("Social Media Clone","Full app: auth, feed, posts","React · Node.js · MongoDB"),("E-commerce Platform","Cart, payments, admin dashboard","Next.js · Express · PostgreSQL"),("Blog CMS","Content management system","Next.js · Prisma · PostgreSQL")],
    "DevOps Engineer":      [("CI/CD Pipeline","GitHub Actions → Docker → AWS","GitHub Actions · Docker · AWS"),("K8s Deployment","Deploy a microservice on Kubernetes","Kubernetes · Helm · AWS EKS"),("Monitoring Stack","Prometheus + Grafana dashboards","Prometheus · Grafana · Linux")],
    "Mobile Developer":     [("Expense Tracker App","Track expenses with charts","Flutter · Firebase"),("Food Delivery App UI","Screens and navigation","React Native · Expo"),("Chat App","Real-time messages","Flutter · Firebase · Dart")],
    "Cybersecurity Analyst":[("Vulnerability Scanner","Script to scan open ports","Python · Nmap"),("SIEM Log Analyser","Parse and alert on system logs","Python · ELK Stack"),("CTF Writeups","Document TryHackMe/HackTheBox solutions","Linux · Networking")],
    "UI/UX Designer":       [("Banking App Redesign","UX audit and hi-fi prototype","Figma"),("Design System","Component library with tokens","Figma · Storybook"),("E-commerce UX Study","User research + wireframes","Figma · Maze")],
    "Software Engineer":    [("LeetCode 100 Solutions","Solve and document 100 problems","Python/Java"),("Chat Application","Scalable chat with design patterns","Java · WebSockets"),("CLI Productivity Tool","Terminal tool with file ops","Python · Click")],
    "Cloud Engineer":       [("Serverless API","Lambda + API Gateway + DynamoDB","AWS · Terraform"),("Multi-region Setup","HA infrastructure across regions","AWS · Terraform"),("Cost Optimiser Script","Identify unused AWS resources","Python · Boto3 · AWS")],
}

# ─────────────────────────────────────────────────────────────
# OPENROUTER API HELPERS
# ─────────────────────────────────────────────────────────────
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-4o-mini"

def call_openrouter_messages(messages: list, max_tokens: int = 2000) -> str:
    key = st.session_state.get("api_key", "")
    if not key:
        return "⚠️ Please enter your OpenRouter API key in the sidebar to use AI features."

    request = Request(
        OPENROUTER_URL,
        data=json.dumps({
            "model": OPENROUTER_MODEL,
            "max_tokens": max_tokens,
            "messages": messages,
        }).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Shivay-98/Study-Notion",
            "X-Title": "CareerCopilot AI 2.0",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"]
    except HTTPError as e:
        details = e.read().decode("utf-8", errors="replace")
        return f"⚠️ OpenRouter API Error ({e.code}): {details}"
    except (URLError, KeyError, IndexError, json.JSONDecodeError) as e:
        return f"⚠️ OpenRouter API Error: {e}"

def call_openrouter(prompt: str, system: str = "", max_tokens: int = 2000) -> str:
    messages = [{"role": "user", "content": prompt}]
    if system:
        messages.insert(0, {"role": "system", "content": system})
    return call_openrouter_messages(messages, max_tokens)

# ─────────────────────────────────────────────────────────────
# CORE ANALYSIS FUNCTIONS
# ─────────────────────────────────────────────────────────────
def extract_found_skills(text: str) -> list:
    low = text.lower()
    return [s for s in ALL_SKILLS if s.lower() in low]

def compute_ats_breakdown(text: str, skills: list) -> dict:
    low = text.lower()
    bd = {}
    bd["Skills Breadth"]  = (min(len(skills) * 2, 28), 28)
    wc = len(text.split())
    bd["Content Depth"]   = (20 if wc>=600 else 14 if wc>=400 else 8 if wc>=200 else 3, 20)
    bd["Projects"]        = (15 if any(k in low for k in ["project","portfolio","github.com","kaggle"]) else 0, 15)
    bd["Experience"]      = (12 if any(k in low for k in ["experience","internship","employment","work"]) else 0, 12)
    bd["Education"]       = (8  if any(k in low for k in ["education","degree","university","b.tech","bca","mca","mba","b.sc","bsc"]) else 0, 8)
    bd["Online Presence"] = (min((4 if "linkedin.com" in low else 0)+(4 if any(k in low for k in ["github.com","kaggle.com","portfolio","behance","dribbble"]) else 0), 8), 8)
    bd["Summary"]         = (5  if any(k in low for k in ["summary","profile","objective","about"]) else 0, 5)
    bd["Certifications"]  = (4  if any(k in low for k in ["certification","certificate","credential"]) else 0, 4)
    bd["__total__"]       = min(sum(v[0] for k,v in bd.items() if k!="__total__"), 100)
    return bd

def detect_best_role(skills: list) -> tuple:
    low = [s.lower() for s in skills]
    scores = {role: round(sum(1 for s in req if s.lower() in low) / len(req) * 100)
              for role, req in ROLE_SKILLS.items()}
    return max(scores, key=scores.get), scores

def detect_field(best_role: str) -> str:
    for field, roles in FIELD_GROUPS.items():
        if best_role in roles:
            return field
    return "Software Engineering"

def skill_match(skills: list, role: str) -> tuple:
    req = ROLE_SKILLS.get(role, [])
    if not req:
        return 0.0, []
    low = [s.lower() for s in skills]
    return (
        round(sum(1 for s in req if s.lower() in low) / len(req) * 100, 1),
        [s for s in req if s.lower() not in low],
    )

def strength_label(score: int) -> tuple:
    if score >= 85: return "Elite",     "#10b981", "🏆"
    if score >= 70: return "Strong",    "#3b82f6", "💪"
    if score >= 55: return "Good",      "#8b5cf6", "✅"
    if score >= 40: return "Fair",      "#f59e0b", "⚠️"
    return              "Needs Work",  "#ef4444", "❌"

def score_color(s):
    return "#10b981" if s>=75 else "#3b82f6" if s>=50 else "#f59e0b" if s>=30 else "#ef4444"

def pbar(pct, color="#3b82f6"):
    return f"""<div style='background:#0a1628;border-radius:999px;height:9px;margin:5px 0;'>
      <div style='width:{pct}%;height:100%;background:linear-gradient(90deg,{color},{color}88);border-radius:999px;'></div>
    </div>"""

def no_resume():
    st.markdown("""<div style='text-align:center;padding:70px 20px;'>
        <div style='font-size:3.5rem;'>📄</div>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;color:#e2e8f0;margin-top:14px;'>Upload your resume to unlock this feature</div>
        <div style='color:#475569;margin-top:8px;'>Use the sidebar → upload a PDF resume</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 6px;'>
      <div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;
            background:linear-gradient(135deg,#3b82f6,#8b5cf6,#ec4899);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        🚀 CareerCopilot
      </div>
      <div style='color:#1e3a5f;font-size:0.72rem;letter-spacing:.1em;margin-top:2px;'>
        AI 2.0 · ALL CS FIELDS
      </div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='color:#334155;font-size:0.75rem;font-weight:700;letter-spacing:.06em;margin-bottom:5px;'>OPENROUTER API KEY</div>", unsafe_allow_html=True)
    api_key = st.text_input("", type="password", key="api_key",
                             placeholder="sk-or-v1-...", label_visibility="collapsed")
    if api_key:
        st.markdown("<div style='color:#10b981;font-size:0.78rem;'>✓ API key set — AI features unlocked</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#334155;font-size:0.76rem;'>Get key: openrouter.ai/keys</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='color:#334155;font-size:0.75rem;font-weight:700;letter-spacing:.06em;margin-bottom:5px;'>YOUR RESUME (PDF)</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.markdown(f"<div style='color:#3b82f6;font-size:0.78rem;'>✓ {uploaded_file.name}</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='color:#334155;font-size:0.75rem;font-weight:700;letter-spacing:.06em;margin-bottom:7px;'>NAVIGATE</div>", unsafe_allow_html=True)
    pages = [
        "🏠  Dashboard",
        "📊  ATS Breakdown",
        "🎯  Career Path & Roadmap",
        "🧠  Skill Gap Analysis",
        "✍️  Resume Rewriter",
        "📚  Course Recommendations",
        "💼  Job Role Engine",
        "🆚  Resume vs Job Description",
        "🎤  Interview Prep",
        "🏆  Resume Ranking",
        "🤖  AI Career Chatbot",
    ]
    nav = st.radio("", pages, label_visibility="collapsed")

    st.divider()
    st.markdown("<div style='color:#1e3a5f;font-size:0.7rem;text-align:center;'>Powered by OpenRouter</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PARSE & CACHE RESUME
# ─────────────────────────────────────────────────────────────
if uploaded_file:
    cache_key = uploaded_file.name + str(uploaded_file.size)
    if st.session_state.get("_ck") != cache_key:
        with st.spinner("Reading resume…"):
            rt = extract_resume_text(uploaded_file)
        if not rt.strip():
            st.error("Could not extract text. Please upload a text-based (not scanned) PDF.")
            st.stop()
        fs      = extract_found_skills(rt)
        bd      = compute_ats_breakdown(rt, fs)
        ats     = bd["__total__"]
        br, rs  = detect_best_role(fs)
        field   = detect_field(br)
        sp, ms  = skill_match(fs, br)
        st.session_state.update({"_ck":cache_key,"rt":rt,"fs":fs,"bd":bd,
                                  "ats":ats,"br":br,"rs":rs,"field":field,"sp":sp,"ms":ms})
    rt    = st.session_state.rt
    fs    = st.session_state.fs
    bd    = st.session_state.bd
    ats   = st.session_state.ats
    br    = st.session_state.br
    rs    = st.session_state.rs
    field = st.session_state.field
    sp    = st.session_state.sp
    ms    = st.session_state.ms
else:
    rt=fs=bd=ats=br=rs=field=sp=ms=None

# ═════════════════════════════════════════════════════════════
#  🏠  DASHBOARD
# ═════════════════════════════════════════════════════════════
if "Dashboard" in nav:
    st.markdown("""<div style='margin-bottom:4px;'>
      <span style='font-family:Syne,sans-serif;font-size:2.1rem;font-weight:800;
        background:linear-gradient(135deg,#3b82f6,#8b5cf6,#ec4899);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        CareerCopilot AI 2.0</span></div>
      <div style='color:#334155;font-size:0.9rem;margin-bottom:26px;'>
        All Computer Engineering Fields · Powered by OpenRouter</div>
    """, unsafe_allow_html=True)

    if not rt:
        # landing state
        st.markdown("""<div style='text-align:center;padding:50px 20px 30px;'>
            <div style='font-size:4rem;'>📄</div>
            <div style='font-family:Syne,sans-serif;font-size:1.6rem;color:#e2e8f0;margin-top:14px;'>
              Upload your resume to get started</div>
            <div style='color:#475569;margin-top:8px;'>
              Supports: Data Analytics · Data Science · Web Dev · Full Stack · Backend ·
              Frontend · DevOps · Cloud · Cybersecurity · Mobile · UI/UX · Software Engineering
            </div></div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-title'>What CareerCopilot Does</div>", unsafe_allow_html=True)
        features = [
            ("📊","ATS Score Breakdown","Category-level score with visual breakdown"),
            ("🎯","Career Path & Roadmap","6-month plan tailored to your field"),
            ("🧠","Skill Gap Analysis","See exactly what skills you're missing"),
            ("✍️","Resume Rewriter","AI rewrites your bullets & full resume"),
            ("📚","Course Recommendations","Field-specific courses to fill skill gaps"),
            ("💼","Job Role Engine","Rank all roles, find real jobs in your city"),
            ("🆚","Resume vs JD","Match score & tailoring tips for any job posting"),
            ("🎤","Interview Prep","Question bank + AI generator + answer coach"),
            ("🏆","Resume Ranking","Rank multiple resumes for placements / drives"),
            ("🤖","AI Career Chatbot","Multi-turn advisor with your resume as context"),
        ]
        cols = st.columns(2)
        for i,(ico,title,desc) in enumerate(features):
            cols[i%2].markdown(f"""
            <div class='cc-plain' style='padding:14px 18px;margin:6px 0;'>
              <span style='font-size:1.2rem;'>{ico}</span>
              <span style='color:#e2e8f0;font-weight:600;margin-left:8px;'>{title}</span>
              <div style='color:#475569;font-size:0.82rem;margin-top:3px;'>{desc}</div>
            </div>""", unsafe_allow_html=True)
    else:
        label, col, icon = strength_label(ats)
        c1,c2,c3,c4 = st.columns(4)
        for widget,val,sub,clr in [
            (c1, f"{icon} {ats}", "ATS Score /100", col),
            (c2, br,              "Best Role Match", "#a78bfa"),
            (c3, str(len(fs)),    "Skills Detected", "#3b82f6"),
            (c4, f"{sp}%",        "Role Skill Match", score_color(sp)),
        ]:
            widget.markdown(f"""<div class='metric-box'>
              <div style='font-family:Syne,sans-serif;font-size:1.45rem;font-weight:800;color:{clr};'>{val}</div>
              <div style='color:#334155;font-size:0.78rem;margin-top:4px;'>{sub}</div>
            </div>""", unsafe_allow_html=True)

        # field badge
        st.markdown(f"<div style='margin:12px 0 6px;'><span style='background:rgba(99,179,237,0.1);border:1px solid rgba(99,179,237,0.25);border-radius:20px;padding:5px 16px;color:#93c5fd;font-size:0.82rem;font-family:DM Mono,monospace;'>📂 Detected Field: {field}</span></div>", unsafe_allow_html=True)

        # Strength meter
        st.markdown(f"""<div class='cc-card'>
          <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;'>
            <div style='font-family:Syne,sans-serif;font-size:1.55rem;font-weight:800;color:{col};'>{icon} {label}</div>
            <div style='color:{col};font-weight:700;'>{ats}/100</div>
          </div>
          <div style='background:#0a1628;border-radius:999px;height:18px;overflow:hidden;'>
            <div style='width:{ats}%;height:100%;
                  background:linear-gradient(90deg,{col},{col}88);
                  border-radius:999px;'></div>
          </div>
          <div style='display:flex;justify-content:space-between;margin-top:6px;
                      color:#1e3a5f;font-size:0.7rem;font-family:DM Mono,monospace;'>
            <span>0 Needs Work</span><span>40 Fair</span><span>55 Good</span><span>70 Strong</span><span>85 Elite 100</span>
          </div>
        </div>""", unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            st.markdown("<div class='sec-title'>Detected Skills</div>", unsafe_allow_html=True)
            pills = " ".join(f"<span class='pill'>{s}</span>" for s in fs) or "<span style='color:#334155'>None found — check your PDF format</span>"
            st.markdown(f"<div class='cc-plain'>{pills}</div>", unsafe_allow_html=True)
        with cb:
            st.markdown("<div class='sec-title'>Quick Wins</div>", unsafe_allow_html=True)
            low = rt.lower()
            wins = []
            if "github.com" not in low: wins.append("Add GitHub profile URL")
            if "linkedin.com" not in low: wins.append("Add LinkedIn profile URL")
            if not any(k in low for k in ["summary","profile","objective"]): wins.append("Add Professional Summary (3–4 lines)")
            if not any(k in low for k in ["project","portfolio"]): wins.append("Add 2+ projects with outcomes & stack")
            if len(rt.split()) < 400: wins.append("Resume is short — expand project details")
            if ms: wins.append(f"Learn: {', '.join(ms[:3])}")
            rows = "".join(f"<div style='padding:7px 0;border-bottom:1px solid #0a1628;color:#94a3b8;font-size:0.86rem;'>⚡ {w}</div>" for w in wins[:5])
            st.markdown(f"<div class='cc-plain'>{rows or '<span style=color:#10b981>✅ Looking strong!</span>'}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  📊  ATS BREAKDOWN
# ═════════════════════════════════════════════════════════════
elif "ATS Breakdown" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>📊 ATS Score Breakdown</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        label, col, icon = strength_label(ats)
        left, right = st.columns([1,2])
        with left:
            deg = round(ats*3.6)
            st.markdown(f"""<div class='cc-card' style='text-align:center;'>
              <div style='width:136px;height:136px;border-radius:50%;margin:0 auto 12px;
                    background:conic-gradient({col} {deg}deg,#0a1628 0deg);
                    display:flex;align-items:center;justify-content:center;'>
                <div style='width:96px;height:96px;border-radius:50%;background:#07101e;
                      display:flex;align-items:center;justify-content:center;
                      font-family:Syne,sans-serif;font-size:1.9rem;font-weight:800;color:{col};'>{ats}</div>
              </div>
              <div style='font-size:1.2rem;font-weight:700;color:{col};'>{icon} {label}</div>
              <div style='color:#1e3a5f;font-size:0.8rem;margin-top:3px;'>out of 100</div>
            </div>""", unsafe_allow_html=True)
        with right:
            st.markdown("<div class='sec-title'>Category Breakdown</div>", unsafe_allow_html=True)
            for cat,(earned,total) in bd.items():
                if cat=="__total__": continue
                pct = round((earned/total)*100)
                c   = score_color(pct)
                st.markdown(f"""<div style='margin-bottom:10px;'>
                  <div style='display:flex;justify-content:space-between;color:#94a3b8;font-size:0.8rem;margin-bottom:2px;'>
                    <span>{cat}</span>
                    <span style='color:{c};font-weight:700;font-family:DM Mono,monospace;'>{earned}/{total}</span>
                  </div>{pbar(pct,c)}</div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sec-title'>Section Checklist</div>", unsafe_allow_html=True)
        low = rt.lower()
        cols = st.columns(4)
        for i,(sec,kws) in enumerate(ATS_SECTIONS.items()):
            found = any(k in low for k in kws)
            bg  = "rgba(16,185,129,0.08)" if found else "rgba(239,68,68,0.08)"
            bdr = "#10b981" if found else "#ef4444"
            cols[i%4].markdown(f"""<div style='background:{bg};border:1px solid {bdr};border-radius:10px;
                  padding:10px;margin:4px 0;text-align:center;'>
              <div style='font-size:1.15rem;'>{"✅" if found else "❌"}</div>
              <div style='color:#cbd5e1;font-size:0.76rem;margin-top:3px;'>{sec}</div>
            </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sec-title'>AI ATS Analysis</div>", unsafe_allow_html=True)
        if st.button("🤖 Run AI ATS Deep Analysis"):
            with st.spinner("Analysing with OpenRouter…"):
                result = call_openrouter(
                    f"""Analyse this {field} resume for ATS compatibility. Provide:
1. Top 5 ATS strengths for a {br} role
2. Top 5 critical ATS weaknesses to fix immediately
3. 5 missing keywords that ATS systems in {field} look for
4. Formatting issues that could cause ATS rejection
5. One-sentence verdict + predicted score after fixes

Resume:
{rt[:3500]}""",
                    f"You are a senior ATS expert specialising in {field} recruitment. Be specific and actionable.")
            st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  🎯  CAREER PATH & ROADMAP
# ═════════════════════════════════════════════════════════════
elif "Career Path" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>🎯 Career Path & Roadmap</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        st.markdown(f"""<div class='cc-card' style='margin-bottom:18px;'>
          <div style='color:#475569;font-size:0.75rem;letter-spacing:.08em;'>BEST MATCH ROLE</div>
          <div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#60a5fa;margin-top:4px;'>🏆 {br}</div>
          <div style='color:#334155;font-size:0.82rem;margin-top:3px;'>Field: {field}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-title'>All Role Matches</div>", unsafe_allow_html=True)

        # group by field for readability
        for grp_name, grp_roles in FIELD_GROUPS.items():
            grp_data = [(r,rs[r]) for r in grp_roles if r in rs]
            if not grp_data: continue
            st.markdown(f"<div style='color:#334155;font-size:0.75rem;font-family:DM Mono,monospace;letter-spacing:.08em;margin:12px 0 6px;'>{grp_name.upper()}</div>", unsafe_allow_html=True)
            for role, sc in sorted(grp_data, key=lambda x: x[1], reverse=True):
                c = score_color(sc)
                st.markdown(f"""<div style='display:flex;align-items:center;gap:12px;margin:5px 0;'>
                  <div style='width:155px;color:#cbd5e1;font-size:0.85rem;'>{role}</div>
                  <div style='flex:1;'>{pbar(sc,c)}</div>
                  <div style='width:42px;text-align:right;color:{c};font-weight:700;font-family:DM Mono,monospace;'>{sc}%</div>
                </div>""", unsafe_allow_html=True)

        st.divider()
        tab1, tab2, tab3 = st.tabs(["🗺️ Career Roadmap", "💰 Salary Insights", "📁 Project Ideas"])

        with tab1:
            target = st.text_input("Customise target role", value=br)
            if st.button("Generate My 6-Month Roadmap"):
                with st.spinner("Building your personalised roadmap…"):
                    result = call_openrouter(
                        f"""Create a detailed 6-month career roadmap for someone in {field} targeting: {target}

Current skills: {', '.join(fs[:10])}
Missing skills: {', '.join(ms[:6])}
Experience level: Fresher / Early Career

Format as 6 monthly milestones:
Month N — [Title]
• Skill to master
• Specific resource (course name + platform)
• Project to build and showcase
• Measurable checkpoint at month end

Be concrete, practical, and specific to the Indian tech job market 2024–25.""",
                        f"You are a senior {field} career coach specialising in Indian placement outcomes.")
                st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

        with tab2:
            if st.button("Show Salary Insights"):
                with st.spinner("Fetching salary data…"):
                    result = call_openrouter(
                        f"""Salary insights for {br} in India (2024–25):

1. Fresher (0–1 yr): CTC range in LPA + top hiring cities
2. Junior (1–3 yr): CTC range
3. Mid-level (3–5 yr): CTC range
4. Senior (5+ yr): CTC range
5. Top 10 companies hiring for {br} in India with typical CTC
6. Skills that command a 30%+ salary premium for this role
7. MNC vs Startup vs Product company salary comparison
8. Remote work salary trends for {field}""")
                st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

        with tab3:
            proj_role = st.selectbox("Projects for:", list(PROJECTS.keys()),
                                     index=list(PROJECTS.keys()).index(br) if br in PROJECTS else 0)
            for name, desc, stack in PROJECTS.get(proj_role,[]):
                st.markdown(f"""<div class='cc-plain'>
                  <div style='color:#60a5fa;font-weight:700;'>{name}</div>
                  <div style='color:#94a3b8;font-size:0.86rem;margin-top:3px;'>{desc}</div>
                  <div style='margin-top:8px;'>{"".join(f"<span class='pill' style='font-size:0.74rem;'>{t.strip()}</span>" for t in stack.split("·"))}</div>
                </div>""", unsafe_allow_html=True)
            if st.button("🤖 Generate Custom Project Ideas"):
                with st.spinner("Thinking…"):
                    result = call_openrouter(
                        f"""Suggest 5 unique {proj_role} project ideas.
Skills: {', '.join(fs[:8])}

Each project:
- Catchy name
- Problem it solves
- Dataset or API to use (free, publicly available)
- Exact tech stack
- Key insight/deliverable to showcase
- How to make it stand out from similar projects""",
                        "You are a tech career mentor focused on portfolio building.")
                st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  🧠  SKILL GAP
# ═════════════════════════════════════════════════════════════
elif "Skill Gap" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>🧠 Skill Gap Analysis</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        # allow user to change target role
        t_role = st.selectbox("Analyse gap for role:", list(ROLE_SKILLS.keys()),
                               index=list(ROLE_SKILLS.keys()).index(br) if br in ROLE_SKILLS else 0)
        t_sp, t_ms = skill_match(fs, t_role)
        c = score_color(t_sp)
        st.markdown(f"""<div class='cc-card'>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
            <span style='color:#e2e8f0;font-weight:600;'>Skill Match — {t_role}</span>
            <span style='color:{c};font-family:DM Mono,monospace;font-weight:700;font-size:1.1rem;'>{t_sp}%</span>
          </div>{pbar(t_sp,c)}</div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='sec-title'>Skills You Have ✅</div>", unsafe_allow_html=True)
            role_low = [s.lower() for s in ROLE_SKILLS.get(t_role,[])]
            matched  = [s for s in fs if s.lower() in role_low]
            other    = [s for s in fs if s.lower() not in role_low]
            pm = " ".join(f"<span class='pill'>✅ {s}</span>" for s in matched)
            po = " ".join(f"<span class='pill' style='opacity:.5;font-size:.74rem;'>{s}</span>" for s in other)
            extra = f"<div style='color:#1e3a5f;font-size:.74rem;margin:9px 0 3px;'>Other detected skills:</div>{po}" if other else ""
            st.markdown(f"<div class='cc-plain'>{pm or '<span style=color:#334155>None yet</span>'}{extra}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='sec-title'>Skills to Learn 📌</div>", unsafe_allow_html=True)
            pm2 = " ".join(f"<span class='pill pill-miss'>📌 {s}</span>" for s in t_ms)
            st.markdown(f"<div class='cc-plain'>{pm2 or '<span style=color:#10b981>🎉 You have all core skills!</span>'}</div>", unsafe_allow_html=True)

        st.divider()
        if st.button("🤖 Build My Skill Learning Plan"):
            with st.spinner("Planning…"):
                result = call_openrouter(
                    f"""I'm targeting {t_role} in {field}.
I know: {', '.join(fs[:10])}
I need to learn: {', '.join(t_ms[:6])}

Create a prioritised learning plan:
1. Which skill to learn first (and why — job market demand)
2. Time to proficiency for each missing skill
3. Best free resource for each (specific platform + course)
4. One mini-project per skill to practise it
5. How to list each skill on a resume once learned

Focus on practical, Indian job-market-relevant advice for 2024–25.""",
                    f"You are a {field} career coach.")
            st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  ✍️  RESUME REWRITER
# ═════════════════════════════════════════════════════════════
elif "Rewriter" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>✍️ Resume Rewriter</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        tab1, tab2 = st.tabs(["✏️ Bullet Rewriter", "📄 Full Resume Rewrite"])

        with tab1:
            st.markdown("<div style='color:#475569;margin-bottom:10px;'>Paste weak bullets → get ATS-optimised, impact-driven rewrites for your specific field.</div>", unsafe_allow_html=True)
            bullets_in = st.text_area("Your current bullets (one per line)", height=180,
                placeholder="Built a website\nWorked on database queries\nHelped team with testing\nCreated reports in Excel")
            t_role2 = st.text_input("Target role", value=br or "")
            if st.button("🔄 Rewrite Bullets") and bullets_in.strip():
                with st.spinner("Rewriting with OpenRouter…"):
                    result = call_openrouter(
                        f"""Rewrite these resume bullets for a {t_role2} role in {field}.

RULES:
- Strong action verb at the start of every bullet
- Add quantification (%, numbers, users, performance, time saved) wherever possible
- Include ATS keywords relevant to {t_role2} and {field}
- Max 20 words per bullet
- Show business/technical impact, not just task

Original bullets:
{bullets_in}

Return ONLY the rewritten bullets, one per line. No explanations, no numbering.""",
                        f"You are a professional resume writer specialised in {field} roles.")
                st.markdown("<div class='sec-title'>✨ Rewritten Bullets</div>", unsafe_allow_html=True)
                for line in result.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"<div class='cc-plain' style='padding:10px 16px;margin:4px 0;color:#e2e8f0;'>• {line.strip()}</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div style='color:#475569;margin-bottom:10px;'>Get a fully rewritten, ATS-ready resume from your uploaded PDF — tailored to your target role and field.</div>", unsafe_allow_html=True)
            t_role3 = st.text_input("Target Role for Rewrite", value=br or "")
            yoe     = st.selectbox("Experience Level", ["Fresher (0–1 yr)","Junior (1–3 yr)","Mid-level (3–5 yr)","Senior (5+ yr)"])
            if st.button("🚀 Generate Full Rewritten Resume"):
                with st.spinner("OpenRouter is rewriting your resume… (~30 sec)"):
                    result = call_openrouter(
                        f"""Rewrite this resume for a {t_role3} position in {field}. Level: {yoe}.

REQUIREMENTS:
- Clear sections: Summary | Skills | Experience | Projects | Education | Certifications
- ATS keywords for {t_role3} and {field} throughout
- Strong action verbs for every bullet point
- Quantify all achievements (%, numbers, scale, impact)
- 3–4 line Professional Summary tailored to {t_role3}
- Do NOT invent experience — only rewrite what exists
- Plain text, ready to paste into a Word document

ORIGINAL RESUME:
{rt[:4000]}""",
                        f"You are a top-tier professional resume writer specialised in {field} hiring.",
                        max_tokens=3000)
                st.text_area("📄 Rewritten Resume — copy this", result, height=520)
                st.download_button("📥 Download Rewritten Resume", result,
                                   f"Rewritten_{t_role3.replace(' ','_')}_Resume.txt")

# ═════════════════════════════════════════════════════════════
#  📚  COURSES
# ═════════════════════════════════════════════════════════════
elif "Course" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>📚 Course Recommendations</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        sel_role = st.selectbox("Show courses for:", list(COURSES.keys()),
                                 index=list(COURSES.keys()).index(br) if br in COURSES else 0)
        st.markdown(f"<div class='sec-title'>Top Courses for {sel_role}</div>", unsafe_allow_html=True)
        for i,(name,platform,note) in enumerate(COURSES[sel_role],1):
            st.markdown(f"""<div class='cc-plain' style='display:flex;align-items:flex-start;justify-content:space-between;gap:12px;'>
              <div>
                <div style='color:#334155;font-size:0.7rem;font-family:DM Mono,monospace;'>COURSE {i:02d}</div>
                <div style='color:#e2e8f0;font-weight:600;margin-top:3px;'>{name}</div>
                <div style='color:#334155;font-size:0.8rem;margin-top:2px;'>📍 {platform} · {note}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sec-title'>AI Personalised Learning Plan</div>", unsafe_allow_html=True)
        if st.button("🤖 Build My 3-Month Learning Plan"):
            with st.spinner("Building…"):
                result = call_openrouter(
                    f"""3-month personalised learning plan for:
Role: {sel_role} | Field: {field}
Current skills: {', '.join(fs[:10])}
Missing: {', '.join(ms[:8])}

Each month:
Month N — Theme
• Primary skill/topic to focus on
• Specific free course (platform + name)
• Daily 30-min routine
• Project to build
• What to add to resume/portfolio at month end

Also recommend: 2 certifications worth getting for {sel_role} in India.""",
                    f"You are a {field} educator focused on Indian placement outcomes.")
            st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  💼  JOB ROLE ENGINE
# ═════════════════════════════════════════════════════════════
elif "Job Role" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>💼 Job Role Recommendation Engine</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        st.markdown(f"<div class='cc-card' style='margin-bottom:16px;'><div style='color:#475569;font-size:.74rem;letter-spacing:.08em;'>PRIMARY RECOMMENDATION</div><div style='font-family:Syne,sans-serif;font-size:1.45rem;font-weight:800;color:#60a5fa;margin-top:4px;'>🏆 {br}</div><div style='color:#1e3a5f;font-size:.8rem;'>{field}</div></div>", unsafe_allow_html=True)

        # Show all roles grouped by field
        for grp_name, grp_roles in FIELD_GROUPS.items():
            grp_data = [(r,rs[r]) for r in grp_roles if r in rs]
            if not grp_data: continue
            st.markdown(f"<div style='color:#334155;font-size:.73rem;font-family:DM Mono,monospace;letter-spacing:.08em;margin:14px 0 5px;'>{grp_name.upper()}</div>", unsafe_allow_html=True)
            for role, sc in sorted(grp_data, key=lambda x: x[1], reverse=True):
                c = score_color(sc)
                _, r_ms = skill_match(fs, role)
                st.markdown(f"""<div class='rank-row'>
                  <div style='width:50px;height:50px;border-radius:50%;background:{c}18;border:2px solid {c};
                        display:flex;align-items:center;justify-content:center;
                        font-family:DM Mono,monospace;font-weight:700;color:{c};font-size:.9rem;'>{sc}%</div>
                  <div style='flex:1;'>
                    <div style='color:#e2e8f0;font-weight:600;'>{role}</div>
                    <div style='color:#1e3a5f;font-size:.76rem;margin-top:2px;'>Missing: {", ".join(r_ms[:4]) if r_ms else "✅ All core skills"}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sec-title'>Find Real Jobs</div>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: j_role = st.selectbox("Role", list(ROLE_SKILLS.keys()), index=list(ROLE_SKILLS.keys()).index(br) if br in ROLE_SKILLS else 0)
        with c2: j_loc  = st.selectbox("Location", ["India","Bangalore","Mumbai","Delhi NCR","Hyderabad","Pune","Chennai","Kolkata","Remote India","USA","UK","UAE","Canada"])
        with c3: j_exp  = st.selectbox("Experience", ["Fresher (0–1 yr)","Junior (1–3 yr)","Mid (3–5 yr)","Senior (5+ yr)"])
        if st.button("🔍 Find Jobs & Companies"):
            with st.spinner("Searching…"):
                result = call_openrouter(
                    f"""10 specific job opportunities for {j_role} in {j_loc} at {j_exp} level.

For each:
1. Specific job title
2. 3 companies actively hiring (India-relevant)
3. Required tools/stack
4. Estimated CTC (LPA for India / USD for international)
5. Where to apply (LinkedIn / Naukri / specific company career page)
6. One tip to stand out

Candidate skills: {', '.join(fs[:10])}
Field: {field}""",
                    f"You are a {field} recruiter with deep India market knowledge.")
            st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  🆚  RESUME vs JD
# ═════════════════════════════════════════════════════════════
elif "Job Description" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>🆚 Resume vs Job Description</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#475569;margin-bottom:18px;'>Paste any job description to see exactly how well your resume matches — and how to close the gap.</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        jd = st.text_area("Paste Job Description (LinkedIn, Naukri, company site, etc.)", height=250,
            placeholder="Copy-paste the full job description here…")
        if st.button("🔍 Analyse Match") and jd.strip():
            with st.spinner("Comparing resume vs JD…"):
                result = call_openrouter(
                    f"""Compare this {field} resume against the job description.

JOB DESCRIPTION:
{jd[:2500]}

RESUME:
{rt[:2500]}

Provide:
MATCH SCORE: X/100 (be precise and honest)

MATCHED KEYWORDS: All JD requirements found in resume

CRITICAL GAPS: Required skills/experience absent from resume (prioritised by importance)

EXPERIENCE FIT: Required YOE vs actual, domain match

5 TAILORING ACTIONS: Specific edits to make this resume a stronger match
(e.g. "Add 'Docker' to skills section", "Mention REST API experience in Project 2")

COVER LETTER HOOK: One powerful opening sentence for this application

VERDICT: Apply Now / Borderline / Not Yet — with brief explanation""",
                    f"You are an expert {field} recruiter and resume coach.", max_tokens=2500)
            st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  🎤  INTERVIEW PREP
# ═════════════════════════════════════════════════════════════
elif "Interview" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>🎤 Interview Prep</div>", unsafe_allow_html=True)
    if not rt: no_resume()
    else:
        tab1, tab2, tab3 = st.tabs(["❓ Question Bank", "🤖 AI Generator", "💬 Answer Coach"])

        with tab1:
            st.markdown("<div class='sec-title'>Question Bank — All CS Fields</div>", unsafe_allow_html=True)
            q_cat = st.selectbox("Category", list(INTERVIEW_QS.keys()))
            for i, q in enumerate(INTERVIEW_QS[q_cat], 1):
                st.markdown(f"""<div class='cc-plain' style='padding:11px 16px;margin:4px 0;'>
                  <span style='color:#3b82f6;font-family:DM Mono,monospace;font-size:.76rem;'>Q{i:02d}</span>
                  <span style='color:#e2e8f0;margin-left:10px;font-size:.88rem;'>{q}</span>
                </div>""", unsafe_allow_html=True)

        with tab2:
            c1,c2,c3 = st.columns(3)
            with c1: q_role  = st.text_input("Target Role", value=br or "")
            with c2: q_type  = st.selectbox("Question Type", ["Mixed","Technical","HR & Behavioural","System Design","DSA / Coding","Case Study"])
            with c3: q_count = st.slider("Number of Questions", 5, 20, 10)
            if st.button("🎯 Generate Personalised Questions"):
                with st.spinner("Generating…"):
                    result = call_openrouter(
                        f"""Generate {q_count} interview questions for a {q_role} role in {field}.
Type: {q_type}
Candidate skills: {', '.join(fs[:10])}

Each question:
Q[N]. [Question]
Type: [Technical/HR/System Design/DSA/Case Study]
Difficulty: [Easy/Medium/Hard]
Strong Answer Should Cover: [2–3 key points]

Tailor to the candidate's skill level and exact target role.""",
                        f"You are a senior {field} interviewer at a top tech company.", max_tokens=3000)
                st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)
                st.download_button("📥 Download Questions", result,
                                   f"{(q_role or 'interview').replace(' ','_')}_questions.txt")

        with tab3:
            prac_q = st.text_input("Enter a question to practise", placeholder="e.g. Explain the virtual DOM in React")
            prac_a = st.text_area("Your answer", height=150, placeholder="Type your answer here…")
            if st.button("📝 Evaluate My Answer") and prac_q and prac_a:
                with st.spinner("Evaluating…"):
                    result = call_openrouter(
                        f"""Evaluate this {field} interview answer:

Question: {prac_q}
Role: {br}
Answer: {prac_a}

Provide:
SCORE: X/10

STRENGTHS: What they got right

MISSING: What a top candidate would have added

MODEL ANSWER: A concise, complete answer (max 150 words)

ONE TIP: Single most impactful improvement""",
                        f"You are a senior {field} interview coach.")
                st.markdown(f"<div class='cc-card'>{result.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  🏆  RESUME RANKING
# ═════════════════════════════════════════════════════════════
elif "Ranking" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>🏆 Resume Ranking</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#475569;margin-bottom:18px;'>Upload multiple resumes to rank them — for campus placements, college drives, and shortlisting.</div>", unsafe_allow_html=True)

    multi       = st.file_uploader("Upload multiple PDF resumes", type=["pdf"], accept_multiple_files=True)
    rank_role   = st.selectbox("Role to rank for", list(ROLE_SKILLS.keys()),
                                index=list(ROLE_SKILLS.keys()).index(br) if (br and br in ROLE_SKILLS) else 0)

    if st.button("🏆 Rank All Resumes") and multi:
        results_list = []
        prog = st.progress(0)
        for i, f in enumerate(multi):
            txt    = extract_resume_text(f)
            s_list = extract_found_skills(txt)
            b2     = compute_ats_breakdown(txt, s_list)
            a_sc   = b2["__total__"]
            _, r_s  = detect_best_role(s_list)
            r_match = r_s.get(rank_role, 0)
            wc2     = len(txt.split())
            final   = round(a_sc*0.5 + r_match*0.4 + min(wc2/20,10)*0.1)
            results_list.append({
                "name": f.name.replace(".pdf",""),
                "ats": a_sc, "role_match": r_match,
                "skills": len(s_list), "final": min(final,100),
            })
            prog.progress((i+1)/len(multi))

        results_list.sort(key=lambda x: x["final"], reverse=True)
        medals = ["🥇","🥈","🥉"]
        st.markdown(f"<div class='sec-title'>Rankings for: {rank_role}</div>", unsafe_allow_html=True)
        for i, r in enumerate(results_list):
            m = medals[i] if i<3 else f"#{i+1}"
            c = score_color(r["final"])
            st.markdown(f"""<div class='rank-row'>
              <div style='font-size:1.6rem;width:42px;text-align:center;'>{m}</div>
              <div style='flex:1;'>
                <div style='color:#e2e8f0;font-weight:700;'>{r["name"]}</div>
                <div style='color:#1e3a5f;font-size:.76rem;margin-top:2px;'>
                  ATS: {r["ats"]} · Role Match: {r["role_match"]}% · Skills: {r["skills"]}
                </div>
              </div>
              <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:{c};'>{r["final"]}</div>
            </div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
#  🤖  AI CHATBOT
# ═════════════════════════════════════════════════════════════
elif "Chatbot" in nav:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.85rem;font-weight:800;color:#e2e8f0;margin-bottom:6px;'>🤖 AI Career Chatbot</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#475569;margin-bottom:18px;'>Ask anything — resume, coding, career, interviews, salaries, projects. Your personal tech career advisor.</div>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    ctx = ""
    if rt:
        ctx = f"""
CANDIDATE RESUME CONTEXT:
- Detected Field: {field}
- Best Role: {br}
- Skills: {', '.join(fs[:15]) if fs else 'None parsed'}
- ATS Score: {ats}/100
- Role Skill Match: {sp}%
- Missing Core Skills: {', '.join(ms[:6]) if ms else 'None'}"""

    sys_prompt = f"""You are CareerCopilot, an expert tech career advisor for computer engineering students and professionals.

You have deep expertise in ALL these fields:
- Data Analytics & Business Intelligence (SQL, Python, Power BI, Tableau, Excel)
- Data Science & ML (Machine Learning, Deep Learning, TensorFlow, Scikit-learn)
- Web Development (React, Node.js, Next.js, Django, REST APIs)
- Full Stack, Frontend, Backend development
- DevOps & Cloud (Docker, Kubernetes, AWS, Azure, CI/CD)
- Cybersecurity (Penetration Testing, OWASP, Network Security)
- Mobile Development (Flutter, React Native, iOS, Android)
- Software Engineering (DSA, System Design, OOP, Design Patterns)
- UI/UX Design (Figma, User Research, Design Systems)

{ctx}

Be specific, practical, and encouraging. Reference the candidate's actual profile when relevant.
For coding questions, give concise code examples. Keep answers under 300 words unless asked to elaborate.
You speak like a senior engineer and mentor at a top tech company."""

    # Display history
    for msg in st.session_state.chat_history:
        css = "chat-user" if msg["role"]=="user" else "chat-ai"
        ico = "👤" if msg["role"]=="user" else "🚀"
        st.markdown(f"<div class='{css}'>{ico}  {msg['content']}</div>", unsafe_allow_html=True)

    # Suggested starters
    if not st.session_state.chat_history:
        st.markdown("<div style='color:#1e3a5f;font-size:.8rem;margin:14px 0 7px;'>💡 Try asking:</div>", unsafe_allow_html=True)
        suggestions = [
            "What should I improve in my resume?",
            f"How do I become a {br}?" if br else "Which tech field should I choose?",
            "Explain SQL JOIN types with examples",
            "What salary can I expect as a fresher in India?",
            "How do I answer 'Tell me about yourself'?",
            "What are the best free datasets for practice projects?",
        ]
        cols = st.columns(3)
        for i, s in enumerate(suggestions):
            if cols[i%3].button(s, key=f"sug_{i}"):
                st.session_state.chat_history.append({"role":"user","content":s})
                with st.spinner("Thinking…"):
                    reply = call_openrouter(s, sys_prompt)
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

    user_msg = st.chat_input("Ask your career question…")
    if user_msg:
        st.session_state.chat_history.append({"role":"user","content":user_msg})
        with st.spinner("…"):
            msgs = [{"role":"system","content":sys_prompt}]
            msgs.extend({"role":m["role"],"content":m["content"]}
                        for m in st.session_state.chat_history)
            reply = call_openrouter_messages(msgs, max_tokens=1000)
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
