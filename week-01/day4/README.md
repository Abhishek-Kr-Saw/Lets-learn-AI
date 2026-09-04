# 🤖 Structured Output with Groq + Pydantic

A beginner-friendly Python project that demonstrates how to extract structured information from a customer support ticket using an **LLM (Large Language Model)**, **Groq API**, and **Pydantic**.

The main idea is simple:

> Give an AI a normal piece of text → ask it to extract specific information → receive JSON → validate that JSON using Pydantic.

---

## 📌 What Will You Learn?

By completing this project, you will understand:

* What environment variables are
* How to use a `.env` file
* How to connect Python with the Groq API
* How to send messages to an LLM
* What `system` and `user` messages mean
* How to define a data structure using Pydantic
* What JSON Schema is
* How to request JSON output from an LLM
* How to validate an LLM response using Pydantic
* How unstructured text can be converted into structured data

---

# 🧠 The Basic Idea

Imagine a customer sends this message:

```text
Hi I am Abhishek from Delhi, I bought iphone from your store
and it is not working. My email is abc@gmail.com.
I am 25 years old.
```

This is **unstructured text**.

We want to extract only the information our application needs:

```json
{
  "name": "Abhishek",
  "email": "abc@gmail.com",
  "issue": "iPhone is not working"
}
```

The complete process looks like this:

```text
Customer Ticket
      ↓
   Groq LLM
      ↓
Extract Information
      ↓
   JSON Output
      ↓
Pydantic Validation
      ↓
Structured Ticket Object
```

---

# 🏗️ Project Structure

A simple project structure can look like this:

```text
day4/
│
├── json_pydantic.py
├── .env
└── README.md
```

### Files

| File               | Purpose                 |
| ------------------ | ----------------------- |
| `json_pydantic.py` | Main Python program     |
| `.env`             | Stores the Groq API key |
| `README.md`        | Project documentation   |

---

# ⚙️ Step 1 — Check Python Installation

First, make sure Python is installed.

Open your terminal and run:

```bash
python --version
```

You should see something similar to:

```text
Python 3.x.x
```

If Python is not installed, install it from the official Python website.

---

# 📦 Step 2 — Install Required Packages

Our program uses three external packages:

```text
python-dotenv
groq
pydantic
```

Install them using:

```bash
pip install python-dotenv groq pydantic
```

If `pip` doesn't work, use:

```bash
python -m pip install python-dotenv groq pydantic
```

---

# 🔑 Step 3 — Create a `.env` File

Create a file named:

```text
.env
```

inside the project directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

For example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

> ⚠️ Never share your API key publicly.

Do **not** upload your `.env` file to GitHub.

Add this to your `.gitignore`:

```gitignore
.env
```

---

# 🔐 Step 4 — Load the API Key

In Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GROQ_API_KEY")
```

Let's understand what happens.

### `load_dotenv()`

This loads variables from your `.env` file.

```text
.env
 │
 │ GROQ_API_KEY
 ↓
load_dotenv()
 ↓
Environment Variables
```

Then:

```python
os.getenv("GROQ_API_KEY")
```

retrieves the API key.

---

# 🛡️ Step 5 — Check the API Key

It's a good practice to check whether the API key exists.

```python
if not key:
    raise ValueError("API key is missing")
```

The flow is:

```text
API Key Found?
     │
 ┌───┴────┐
 │        │
YES       NO
 │        │
 ↓        ↓
Continue  Error
```

---

# 🤝 Step 6 — Create the Groq Client

Import Groq:

```python
from groq import Groq
```

Then create the client:

```python
client = Groq(api_key=key)
```

The client allows our Python program to communicate with the Groq API.

Think of it as:

```text
Python Application
       ↓
  Groq Client
       ↓
   Groq API
       ↓
      LLM
```

---

# 🧠 Step 7 — Select the Model

We specify the model we want to use:

```python
model = "openai/gpt-oss-120b"
```

Later, we pass this model to the API:

```python
response = client.chat.completions.create(
    model=model,
    ...
)
```

---

# 📋 Step 8 — Create a Pydantic Model

Now we need to tell our application what information we expect from the AI.

Import Pydantic:

```python
from pydantic import BaseModel
```

Create a model:

```python
class Ticket(BaseModel):
    name: str
    email: str
    issue: str
```

This defines the expected structure.

Think of it as:

```text
Ticket
│
├── name  → string
├── email → string
└── issue → string
```

For example, this is valid:

```json
{
  "name": "Abhishek",
  "email": "abc@gmail.com",
  "issue": "iPhone is not working"
}
```

---

# 📐 Step 9 — Generate a JSON Schema

We can convert our Pydantic model into a JSON Schema:

```python
schema = Ticket.model_json_schema()
```

Conceptually, Pydantic generates something like:

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "issue": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "email",
    "issue"
  ]
}
```

The schema tells us:

> "A Ticket should be an object containing `name`, `email`, and `issue`, and all three should be strings."

---

# 🤖 Step 10 — Tell the AI to Return JSON

We define:

```python
response_format = {
    "type": "json_object"
}
```

This tells the API that we want a JSON response.

Instead of getting:

```text
Sure! Here is the information you requested...
```

we want something like:

```json
{
  "name": "Abhishek",
  "email": "abc@gmail.com",
  "issue": "iPhone is not working"
}
```

---

# 📝 Step 11 — Create the System Prompt

We create instructions for the AI:

```python
system_prompt = f"""
    Extract personal info from this ticket and return in json format
    {schema}
"""
```

The system prompt tells the AI **what it should do**.

The schema gives the AI an idea of the expected structure.

Conceptually:

```text
System
  ↓
Extract information
  ↓
Use this structure
  ↓
name
email
issue
```

---

# 👤 Step 12 — Create the Customer Ticket

Now we have our input:

```python
text = """
Hi I am Abhishek from Delhi, I bought iphone from your store
and is not working, My email is abc@gmail.com.
I am 25 years old.
"""
```

Notice that the text contains information we don't necessarily need.

```text
Name       → Abhishek
Location   → Delhi
Product    → iPhone
Issue      → iPhone is not working
Email      → abc@gmail.com
Age        → 25
```

But our Pydantic model only requires:

```text
name
email
issue
```

The LLM's job is to extract those fields.

---

# 💬 Step 13 — Create the User Prompt

```python
prompt = f"""
    This is customer ticket.
    Please extract the personal info from this:
    {text}
"""
```

This gives the AI the actual customer ticket.

---

# 📨 Step 14 — Create the Messages

We create a system message:

```python
message_system = {
    "role": "system",
    "content": system_prompt
}
```

And a user message:

```python
message = {
    "role": "user",
    "content": prompt
}
```

Then combine them:

```python
messages = [message_system, message]
```

So the LLM receives:

```text
┌──────────────────────────────┐
│ SYSTEM                       │
│                              │
│ Extract information and      │
│ return it as JSON.           │
└──────────────┬───────────────┘
               │
               ↓
┌──────────────────────────────┐
│ USER                         │
│                              │
│ Here is the customer ticket.│
│ Extract the information.     │
└──────────────────────────────┘
```

---

# 🚀 Step 15 — Send the Request

Now we finally communicate with the LLM:

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)
```

This is the most important step.

Our application sends:

```text
Model
+
System Instructions
+
Customer Ticket
+
JSON Response Requirement
```

to Groq.

The LLM processes the ticket and returns a response.

---

# 📥 Step 16 — Get the LLM Response

The response contains several pieces of information.

The actual generated content is:

```python
response.choices[0].message.content
```

We can store it:

```python
content = response.choices[0].message.content
```

For example:

```json
{
  "name": "Abhishek",
  "email": "abc@gmail.com",
  "issue": "iPhone is not working"
}
```

---

# ✅ Step 17 — Validate Using Pydantic

Now comes the important part.

We can use Pydantic to validate the JSON:

```python
ticket = Ticket.model_validate_json(content)
```

This means:

> Take the JSON returned by the LLM and check whether it matches my `Ticket` model.

The flow:

```text
LLM Response
     ↓
    JSON
     ↓
Pydantic
     ↓
Does it match Ticket?
     │
 ┌───┴────┐
YES       NO
 ↓         ↓
Object    Validation Error
```

---

# 🎯 Step 18 — Access the Data

After validation:

```python
print(ticket.name)
print(ticket.email)
print(ticket.issue)
```

Output:

```text
Abhishek
abc@gmail.com
iPhone is not working
```

You now have a proper Python object instead of just raw text.

---

# 🔄 Complete Code

Here is the complete version:

```python
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


# Load environment variables
load_dotenv()


# Get API key
key = os.getenv("GROQ_API_KEY")

if not key:
    raise ValueError("API key is missing")


# Create Groq client
client = Groq(api_key=key)


# Select model
model = "openai/gpt-oss-120b"


# -----------------------------
# Pydantic Schema
# -----------------------------

class Ticket(BaseModel):
    name: str
    email: str
    issue: str


# Generate JSON schema
schema = Ticket.model_json_schema()


# Tell the model to return JSON
response_format = {
    "type": "json_object"
}


# -----------------------------
# System Prompt
# -----------------------------

system_prompt = f"""
Extract personal information from this customer ticket
and return it in JSON format.

Expected structure:
{schema}
"""


message_system = {
    "role": "system",
    "content": system_prompt
}


# -----------------------------
# Customer Ticket
# -----------------------------

text = """
Hi I am Abhishek from Delhi, I bought iphone from your store
and it is not working. My email is abc@gmail.com.
I am 25 years old.
"""


# -----------------------------
# User Prompt
# -----------------------------

prompt = f"""
This is a customer ticket.
Please extract the required information from this:

{text}
"""


message = {
    "role": "user",
    "content": prompt
}


# Combine messages
messages = [
    message_system,
    message
]


# -----------------------------
# Call Groq API
# -----------------------------

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)


# Get model output
content = response.choices[0].message.content

print("Raw JSON:")
print(content)


# -----------------------------
# Pydantic Validation
# -----------------------------

ticket = Ticket.model_validate_json(content)


print("\nValidated Ticket:")
print(ticket)

print("\nIndividual Fields:")
print("Name:", ticket.name)
print("Email:", ticket.email)
print("Issue:", ticket.issue)
```

---

# 🧩 Understanding the Roles

One of the most important concepts in this project is the `role`.

You have:

```python
{
    "role": "system",
    "content": "..."
}
```

and:

```python
{
    "role": "user",
    "content": "..."
}
```

### System

The system message gives instructions to the model.

```text
SYSTEM
↓
"What should you do?"
```

### User

The user message provides the actual request/data.

```text
USER
↓
"Here is the customer ticket."
```

So:

```text
System → Instructions
User   → Input / Request
AI     → Response
```

---

# 🧠 Pydantic vs JSON Schema vs JSON

These three concepts can be confusing at first.

### Pydantic Model

Python definition:

```python
class Ticket(BaseModel):
    name: str
    email: str
    issue: str
```

### JSON Schema

A machine-readable description of the expected structure:

```json
{
  "name": "string",
  "email": "string",
  "issue": "string"
}
```

### JSON

The actual data:

```json
{
  "name": "Abhishek",
  "email": "abc@gmail.com",
  "issue": "iPhone is not working"
}
```

Think:

```text
Pydantic Model
      ↓
Defines structure
      ↓
JSON Schema
      ↓
Describes structure
      ↓
LLM
      ↓
Generates data
      ↓
JSON
      ↓
Pydantic
      ↓
Validates data
```

---

# ⚠️ Important Note

In this project, the Pydantic schema is included in the prompt:

```python
system_prompt = f"""
    ...
    {schema}
"""
```

and the API is instructed to return a JSON object:

```python
response_format = {
    "type": "json_object"
}
```

Therefore, Pydantic is being used to **describe and validate** the structure.

It is not, by itself, forcing the LLM to produce the exact Pydantic structure.

That's an important distinction when learning structured outputs.

---

# 🏁 Final Mental Model

If you're new to AI/LLM development, remember this simple pattern:

```text
                  INPUT
                    │
                    ↓
        "Hi, my name is Abhishek..."
                    │
                    ↓
              ┌───────────┐
              │    LLM    │
              └─────┬─────┘
                    │
                    ↓
             JSON Response
                    │
                    ↓
              ┌───────────┐
              │ Pydantic  │
              └─────┬─────┘
                    │
                    ↓
           Validated Python Object
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
        name      email      issue
```

### In one sentence:

> **Groq's LLM extracts information from unstructured text, JSON provides a structured format, and Pydantic validates that the returned data matches the structure your Python application expects.**

---

## ▶️ Run the Project

Once everything is configured:

```bash
python json_pydantic.py
```

If everything is working correctly, you should see the extracted ticket information in JSON and the validated Pydantic object.
