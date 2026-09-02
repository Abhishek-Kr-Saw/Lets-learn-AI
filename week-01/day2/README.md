# Week 1 - Day 2: System Prompt and Temperature

This project demonstrates how to send a system prompt to a Groq-hosted LLM and adjust the `temperature` parameter to control the creativity of the response.

## Project Goal

In this exercise, we:

- set up a Python project
- install Groq and dotenv dependencies
- create a `.env` file with the API key
- send both a system message and a user message to the LLM
- tune the model with `temperature=2`
- print the final response in the terminal

## Requirements

Make sure you have:

- Python 3.13
- `uv` installed
- PowerShell or Command Prompt
- A valid Groq API key

## Dependencies

This project uses:

- `groq`
- `python-dotenv`

These are already configured in `pyproject.toml`.

## Step-by-Step Guide

### 1. Open the project folder

```powershell
cd D:\Study\Lets-learn-AI\week-01\day2
```

### 2. Create a virtual environment

```powershell
uv venv --python 3.13
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
uv add groq python-dotenv
```

### 4. Create a `.env` file

In the root of the project, create a file named `.env`:

```env
GROQ_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your real Groq API key.

> Keep your API key private and do not push it to GitHub.

### 5. Create the Python script

Create a file named `sys_temp.py` with the following code:

```python
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")

if not key:
    raise ValueError("API key is missing")

client = Groq(api_key=key)

model = "openai/gpt-oss-20b"

role = "user"
prompt = "Suggest me two MERN stack project with some details which shortlist my resume in any product based company."

message_system = {
    "role": "system",
    "content": "You are a manager of a product based company."
}

message = {
    "role": role,
    "content": prompt
}

messages = [message_system, message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)

print("------------------------------------------------")
print(response.choices[0].message.content)
print("------------------------------------------------")
```

### 6. Run the script

```powershell
python sys_temp.py
```

## What This Code Does

### System message

```python
message_system = {
    "role": "system",
    "content": "You are a manager of a product based company."
}
```

This tells the model to behave like a hiring manager or product-company reviewer.

### User message

```python
message = {
    "role": "user",
    "content": "Suggest me two MERN stack project with some details which shortlist my resume in any product based company."
}
```

This is the actual user request we want the model to answer.

### Temperature

```python
temperature=2
```

- Temperature controls randomness.
- A value closer to 2 creates more creative and varied answers.
- A value near 0 gives more deterministic responses.

## Example Behavior

The model may suggest project ideas such as:

- an e-commerce dashboard
- a project management SaaS app
- a job portal or social media analytics tool

These projects should be framed to impress a product-based company recruiter or hiring manager.

## Project Structure

```text
week-01/
└── day2/
    ├── .venv/
    ├── .env
    ├── .python-version
    ├── pyproject.toml
    ├── README.md
    ├── sys_temp.py
    ├── uv.lock
    └── src/
```

## Troubleshooting

### 1. API key missing

If you see:

```text
ValueError: API key is missing
```

Check:

- `.env` exists in the project folder
- the variable name is exactly `GROQ_API_KEY`
- the value is not blank

### 2. Module not found

If Python says a package is missing, run:

```powershell
uv add groq python-dotenv
```

### 3. Wrong method name

Use:

```python
client.chat.completions.create(...)
```

not:

```python
client.chat.completion.create(...)
```

## Summary

Day 2 focuses on a more realistic LLM interaction by using:

1. a `system` prompt
2. a `user` prompt
3. model temperature control
4. project suggestions for resume improvement

This teaches how prompt design and system instructions can change the quality and tone of AI responses.
