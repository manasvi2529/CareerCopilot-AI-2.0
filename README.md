# CareerCopilot AI 2.0

An AI-powered career assistant built with Python, Streamlit, and the OpenRouter API. It helps users review resumes and prepare for career opportunities across computer engineering and technology roles.

## Live Demo: https://careercopilot-ai-20-mm5mswyqqn7cnmav7tdbzn.streamlit.app

## Features

- Extract text from PDF resumes
- ATS-style resume score breakdown
- Career path and roadmap generation
- Skill-gap analysis
- AI-assisted resume rewriting
- Course recommendations
- Job-role matching
- Resume-versus-job-description comparison
- Interview preparation
- Resume ranking
- AI career chatbot

## Tech stack

- Python
- Streamlit
- OpenRouter API

## Getting started

### 1. Requirements

Use Python 3.10 or newer.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Configure AI features

Enter your OpenRouter API key in the app's sidebar. You can obtain a key at https://openrouter.ai/keys.

## Project files

```text
CareerCopilot-AI-2.0/
├── app.py
├── resume_parser.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Security and privacy

- Never commit API keys, `.env` files, or private credentials.
- The app accepts an OpenRouter API key through its password-style sidebar field.
- When AI features are used, resume text may be sent to OpenRouter for processing. Do not upload information you are not comfortable sharing with that provider.

## Notes

The ATS score is an application-generated estimate and should not be treated as a guarantee of how any employer's applicant tracking system will score a resume.
