# Week 1 - Day 1: LLM API Call

This project is a beginner-friendly Python example that sends a prompt to the Groq API and prints the model response in the terminal.

## Project Goal

The goal of Day 1 is to:

- set up a Python project
- install the Groq SDK
- create a `.env` file for the API key
- call a language model from Python
- print the returned chat response

## Requirements

Before starting, make sure these are available:

- Python 3.13
- `uv` package manager
- Git Bash / PowerShell / Command Prompt
- A valid Groq API key

## Dependencies

This project uses:

- `groq`
- `python-dotenv`

The project configuration is already defined in `pyproject.toml`.

## Step-by-Step Guide

### 1. Open the project folder

```powershell
cd D:\Study\Lets-learn-AI\week-01\day1
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

Create a file named `.env` in the project folder and add:

```env
GROQ_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your real Groq API key.

> Keep this file private and do not share it in public repositories.

### 5. Create the script

Create a file named `hello_llm.py` with the following code:

```python
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")

if not key:
    raise ValueError("API key is missing")

client = Groq(api_key=key)

model = "openai/gpt-oss-120b"
role = "user"
prompt = "Do you know Virat Kohli?"

message = {
    "role": role,
    "content": prompt
}

messages = [message]

response = client.chat.completions.create(
    model=model,
    messages=messages
)

print(response)
print("#######################################")
print(response.choices[0].message.content)
```

### 6. Run the application

```powershell
python hello_llm.py
```

### 7. Expected output

The program will print the full response object and then the assistant's answer, for example:

```text
The model will respond to the question about Virat Kohli.
```

## Important Notes

- Correct method:

```python
client.chat.completions.create(...)
```

- Incorrect method that causes an error:

```python
client.chat.completion.create(...)
```

This error occurs because the Groq Python SDK uses `completions`, not `completion`.

## Project Structure

```text
week-01/
└── day1/
    ├── .venv/
    ├── src/
    ├── .env
    ├── .python-version
    ├── hello_llm.py
    ├── pyproject.toml
    ├── uv.lock
    └── README.md
```

## Troubleshooting

### API key missing

If you see:

```text
ValueError: API key is missing
```

Then check:

- the `.env` file exists in the project folder
- the variable name is exactly `GROQ_API_KEY`
- the value is not blank

### Module not found

If a package is missing, run:

```powershell
uv add groq python-dotenv
```

### Wrong Groq method

If the error says:

```text
AttributeError: 'Chat' object has no attribute 'completion'
```

Use:

```python
client.chat.completions.create(model=model, messages=messages)
```

## Summary

This Day 1 project teaches the basic flow of integrating an LLM into Python:

1. install dependencies
2. configure the API key
3. create the prompt
4. call the Groq model
5. print the output

This is the foundation for building more advanced AI applications later.
