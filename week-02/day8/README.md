# 🤖 AI Resume Screening System

An AI-powered resume screening system built with **Python, Groq API, and LLMs**.

The system analyzes a candidate's resume against a job description, extracts relevant skills, compares them, and generates a **similarity score, hiring verdict, reason, and skill comparison table**.

---

## 📌 Project Overview

Recruiters often need to compare many resumes against a Job Description (JD). This project automates the initial screening process using an LLM.

The application performs three major steps:

```text
                ┌──────────────────┐
                │     Resume       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Extract Skills   │
                └────────┬─────────┘
                         │
                         ▼
                  Candidate Skills
                         │
                         │
                         │       ┌──────────────────┐
                         │       │ Job Description  │
                         │       └────────┬─────────┘
                         │                │
                         │                ▼
                         │       ┌──────────────────┐
                         │       │ Extract JD Skills│
                         │       └────────┬─────────┘
                         │                │
                         │                ▼
                         │          Required Skills
                         │                │
                         └───────┬────────┘
                                 ▼
                         ┌───────────────┐
                         │ Skill Matcher │
                         └───────┬───────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Score + Verdict +      │
                    │ Skill Comparison Table │
                    └────────────────────────┘
```

---

## ✨ Features

* 🔐 Secure API key management using `.env`
* 🤖 LLM-powered resume analysis
* 📄 Job Description skill extraction
* 👨‍💻 Candidate skill extraction
* 🔍 Candidate vs JD skill comparison
* 📊 Similarity score between 1 and 100
* ✅ Good Fit / Partial Fit / Poor Fit verdict
* 📝 Short explanation of the result
* 📋 Skill comparison table
* ❌ Identification of missing skills
* 🔢 Python-based score extraction using Regular Expressions

---

## 🛠️ Technologies Used

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Application development         |
| Groq API              | LLM API                         |
| `openai/gpt-oss-120b` | Language model                  |
| python-dotenv         | Environment variable management |
| Regular Expressions   | Extracting the score            |
| `time.sleep()`        | Adding delay between API calls  |

---

## 📂 Project Structure

```text
AI-Resume-Screening/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> Your Python file can have any name. In this example it is called `main.py`.

---

## ⚙️ Prerequisites

Make sure you have:

* Python 3.9+
* A Groq API key
* Internet connection
* `pip`

Check Python:

```bash
python --version
```

Check pip:

```bash
pip --version
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd AI-Resume-Screening
```

---

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install groq python-dotenv
```

Or, if a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The application loads the key using:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
```

The application also checks whether the API key exists:

```python
if not api_key:
    raise ValueError("API key is missing")
```

### ⚠️ Important

Never commit your API key to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# 🔄 How the Application Works

## Step 1 — Resume Skill Extraction

The resume is sent to the LLM.

Example:

```text
Python, FastAPI, MySQL, Docker, REST APIs, Git
```

The system extracts only the candidate's skills.

Function:

```python
def res_extract(RESUME):
```

---

## Step 2 — Job Description Skill Extraction

The Job Description is sent to the LLM.

Example:

```text
Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs
```

Function:

```python
def JD_extract(JD):
```

---

## Step 3 — Skill Comparison

The extracted candidate skills and required JD skills are passed to another LLM call.

Function:

```python
def match_similarity(candidate, jd):
```

The LLM generates:

* Score
* Verdict
* Reason
* Skill comparison table

---

# 📊 Example Output

```text
STEP 1
Python, FastAPI, MySQL, Docker, REST APIs, Git

STEP 2
Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs

STEP 3

Score: 57

Verdict: Partial Fit

Reason: Missing several core backend and cloud skills.

Skill Comparison:

| Skill | Available |
|---|---|
| Python | Yes |
| FastAPI | Yes |
| Django | No |
| PostgreSQL | No |
| Docker | Yes |
| AWS | No |
| REST APIs | Yes |
```

---

# 🔢 Extracting the Score

The LLM returns the score as part of a larger text response.

For example:

```text
Score: 57
Verdict: Partial Fit
Reason: Missing several core backend and cloud skills.
```

Python's `re` module can be used to extract the score.

```python
import re

result = match_similarity(candidate, jd)

score_match = re.search(r"Score:\s*(\d+)", result)

if score_match:
    score = int(score_match.group(1))
    print("Final Score:", score)
else:
    print("Score not found")
```

The regular expression:

```python
r"Score:\s*(\d+)"
```

looks for:

```text
Score:
```

followed by optional whitespace and a number.

For:

```text
Score: 57
```

it extracts:

```text
57
```

and converts it into an integer:

```python
57
```

---

# 🧩 Core Function Architecture

The application uses a reusable LLM function:

```python
def llm_call(system_prompt, user_prompt):
```

This function handles communication with the Groq API.

The other functions use it for their individual tasks:

```text
                 llm_call()
                    ▲
          ┌─────────┼─────────┐
          │         │         │
          │         │         │
    res_extract  JD_extract  match_similarity
          │         │         │
       Resume       JD       Comparison
```

This avoids repeating the Groq API implementation multiple times.

---

# 🧠 Prompt Engineering

The system uses different prompts for different tasks.

### Resume extraction

```text
Extract the skills from the candidate's resume.
Only return the skills.
Do not invent any skills.
```

### JD extraction

```text
Extract the skills from the Job Description.
Only return the skills.
Do not invent any skills.
```

### Skill matching

```text
Compare the candidate's skills with the required job skills.
Return a score, verdict, reason, and skill comparison table.
```

This demonstrates a **multi-step LLM workflow** instead of using one large prompt for the entire application.

---

# ▶️ Running the Application

Activate the virtual environment first:

```bash
venv\Scripts\activate
```

Then run:

```bash
python main.py
```

You should see output similar to:

```text
STEP 1
Python, FastAPI, MySQL, Docker, REST APIs, Git

STEP 2
Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs

STEP 3
Score: 57
Verdict: Partial Fit
Reason: Missing several core backend and cloud skills.
```

---

# ⚠️ Current Limitations

This is currently a learning/prototype version.

### 1. LLM-generated score

The score is currently generated by the LLM, so it may not always be deterministic.

### 2. Plain-text parsing

The score is extracted using Regex:

```python
re.search(...)
```

A structured JSON response would be more reliable.

### 3. Manual resume input

Currently, the resume is stored directly inside Python:

```python
RESUME = """..."""
```

There is no PDF/DOCX upload yet.

### 4. Skill matching depends on the LLM

The comparison is currently performed by the LLM rather than a deterministic matching algorithm.

### 5. No database

Candidate results are not currently stored in PostgreSQL or another database.

---

# 🚀 Future Improvements

The project can be expanded into a complete AI recruitment assistant.

### Phase 1

* [x] Resume skill extraction
* [x] JD skill extraction
* [x] Skill comparison
* [x] Similarity score
* [x] Hiring verdict
* [x] Missing skill detection
* [x] Score extraction

### Phase 2

* [ ] Structured JSON output
* [ ] Skill normalization
* [ ] Deterministic scoring system
* [ ] Experience matching
* [ ] Required vs optional skills
* [ ] Better handling of `AND` / `OR` requirements

### Phase 3

* [ ] PDF resume upload
* [ ] DOCX resume upload
* [ ] Automatic text extraction
* [ ] Candidate information extraction
* [ ] Multiple resume processing

### Phase 4

* [ ] Embeddings
* [ ] Semantic similarity
* [ ] Vector database
* [ ] Better skill matching

### Phase 5

* [ ] FastAPI backend
* [ ] Web frontend
* [ ] PostgreSQL database
* [ ] Recruiter dashboard
* [ ] Candidate ranking
* [ ] Interview question generation

### Phase 6

* [ ] Dockerize application
* [ ] Deploy to AWS
* [ ] Authentication
* [ ] Production logging
* [ ] Monitoring

---

# 📈 Planned Architecture

The long-term architecture could look like:

```text
                         ┌───────────────┐
                         │   Recruiter   │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    Frontend   │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         └───────┬───────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
               ▼                 ▼                 ▼
          Resume Parser      PostgreSQL        LLM API
               │                                   │
               ▼                                   ▼
        Candidate Data                      Skill Analysis
                                                   │
                                                   ▼
                                          Skill Comparison
                                                   │
                                                   ▼
                                           Final Score
                                                   │
                                                   ▼
                                            Candidate Rank
```

---

# 🎯 Learning Objectives

This project helps demonstrate practical concepts in:

* Python
* Environment variables
* API integration
* LLM APIs
* Prompt engineering
* Function abstraction
* Multi-step AI workflows
* Regular expressions
* Text extraction
* Resume analysis
* Job description analysis
* AI-assisted decision making

---

# ⚠️ Disclaimer

This project is intended for **educational and experimental purposes**.

AI-generated resume evaluations should not be treated as the sole basis for real-world hiring decisions. Human review should always be included in recruitment workflows.

---

## 👨‍💻 Author

**Abhishek Kumar Saw**

Built as part of hands-on learning in **Python, LLMs, Prompt Engineering, and AI Application Development**.
