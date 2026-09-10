import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep
import re

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API key is missing")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-120b"  

JD = f"""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME = f"""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def llm_call(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt
    }

    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg,user_msg]
    response = client.chat.completions.create(model = model, messages=messages)
    ans = response.choices[0].message.content
    return ans


def res_extract(RESUME):
    print("--------------------------------------")
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this resume
    {RESUME}
    """
    return llm_call(system_prompt, user_prompt)


def JD_extract(JD):
    print("--------------------------------------")
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the Job description  provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this JD
    {JD}
    """
    return llm_call(system_prompt, user_prompt)


def match_similarity(candidate,jd):
    print("--------------------------------------")
    system_prompt="""
    You are a professional HR assistant.

    Compare the candidate's skills with the required job skills.

    Return the result in exactly this format:

    Score: <number between 1 and 100>
    Verdict: <Good Fit / Partial Fit / Poor Fit>
    Reason: <one short sentence>

    Skill Comparison:
    | Skill | Available |
    |---|---|
    | <skill> | Yes/No |

    Rules:
    1. Only compare skills explicitly present in the candidate resume and job description.
    2. Do not invent any skills.
    3. Similarity Table must contain only matching or closely equivalent skills.
    4. Dissimilarity Table must contain required JD skills that are not present in the candidate's skills.
    5. If a skill has no match, write "Not Found" under Candidate Skill.
    6. Keep the tables concise.
    7. Preserve the exact skill names when possible.
    8. Return nothing outside the specified format.
    """
    user_prompt=f"""
    Compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    return llm_call(system_prompt, user_prompt)

candidate = res_extract(RESUME)
print(candidate)
sleep(2)
jd = JD_extract(JD)
print(jd)
sleep(2)
score = match_similarity(candidate,jd)
print(score)

result = match_similarity(candidate,jd)
score_match = re.search(r"Score:\s*(\d+)", result)

if score_match:
    score = int(score_match.group(1))
    if score > 55: 
        print("Call for interview")
    else:
        print("Prepare more for the interview")
else:
    print("Score not found")