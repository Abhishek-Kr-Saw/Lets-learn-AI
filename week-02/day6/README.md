# LLM Issue Classification using Groq

A simple Python project that uses a Large Language Model (LLM) through the **Groq API** to automatically classify customer support issues into predefined categories.

The project demonstrates a basic **LLM classification workflow**, including prompt engineering, environment variables, API integration, and structured output constraints.

---

## 🚀 Features

* Uses the **Groq API** to communicate with an LLM.
* Uses `openai/gpt-oss-120b` as the language model.
* Classifies customer issues into predefined categories.
* Uses prompt engineering to control the model's response.
* Keeps the API key secure using a `.env` file.
* Returns a simple one-word classification.

---

## 🧠 How It Works

The application follows this basic flow:

```text
User Issue
    │
    ▼
Prompt Engineering
    │
    ▼
Groq API
    │
    ▼
GPT-OSS-120B Model
    │
    ▼
Issue Classification
    │
    ├── billing
    ├── technical
    ├── return
    └── other
```

For example:

```text
Input:
"My laptop is not working."

Output:
technical
```

Another example:

```text
Input:
"I want a refund for my laptop."

Output:
return
```

---

## 📂 Project Structure

```text
project/
│
├── prompt_eng.py
├── .env
├── .gitignore
└── README.md
```

> You can rename `prompt_eng.py` according to the actual filename of your Python script.

---

## 🛠️ Technologies Used

* **Python**
* **Groq API**
* **Groq Python SDK**
* **python-dotenv**
* **GPT-OSS-120B**

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd <project-directory>
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

Install the required packages:

```bash
pip install python-dotenv groq
```

---

## 🔑 Environment Variables

The application requires a Groq API key.

Create a file named:

```text
.env
```

Add your API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The application loads the key using:

```python
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GROQ_API_KEY")
```

### ⚠️ Important

Never commit your `.env` file to GitHub.

Add this to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
```

---

## ▶️ Running the Project

After activating the virtual environment, run:

```bash
python main.py
```

Example output:

```text
------------------------------------
technical
------------------------------------
```

---

## 🧩 Classification Categories

The LLM is instructed to classify each issue into one of the following categories:

| Category    | Description                                 | Example                        |
| ----------- | ------------------------------------------- | ------------------------------ |
| `billing`   | Payment, invoice, or billing-related issues | "I was charged twice."         |
| `technical` | Product or technical problems               | "My laptop is not turning on." |
| `return`    | Refund, replacement, or returning a product | "I want to return my laptop."  |
| `other`     | Issues unrelated to the above categories    | "What are your store timings?" |

---

## 📝 Prompt Engineering

The project uses a structured prompt containing several components:

### Role

```text
You are a support assistant at a mobile/laptop company.
```

This gives the model a specific role.

### Task

```text
You have to classify the issue into a category.
```

This tells the model what it needs to accomplish.

### Constraints

```text
billing
technical
return
```

These define the expected categories.

### Output Format

```text
Your answer should be in one word only.
```

This prevents the model from returning unnecessary explanations.

### Fallback

```text
If the issue is unrelated to any of the categories,
return other.
```

This provides a category for unsupported issues.

---

## 🔄 Example Classifications

### Example 1

**Input:**

```text
My laptop is not working.
```

**Output:**

```text
technical
```

### Example 2

**Input:**

```text
I was charged twice for my order.
```

**Output:**

```text
billing
```

### Example 3

**Input:**

```text
I want to return the laptop I purchased.
```

**Output:**

```text
return
```

### Example 4

**Input:**

```text
What is your company's holiday schedule?
```

**Output:**

```text
other
```

---

## 🔍 Code Flow

The application first initializes the Groq client:

```python
client = Groq(api_key=key)
```

Then the model is selected:

```python
model = "openai/gpt-oss-120b"
```

The user's prompt is passed to the LLM:

```python
response = client.chat.completions.create(
    model=model,
    messages=messages
)
```

Finally, the generated response is extracted:

```python
ans = response.choices[0].message.content
```

---

## 🎯 Learning Objectives

This project helps understand:

* What an LLM API is
* How to call an LLM from Python
* How to use the Groq SDK
* How environment variables work
* How `.env` files protect API keys
* Basic prompt engineering
* Role prompting
* Classification using LLMs
* Output constraints
* Fallback categories

---

## 🔮 Future Improvements

This project can be extended by:

* Taking issues dynamically from the user.
* Processing multiple customer complaints.
* Adding more categories.
* Returning structured JSON output.
* Building a web interface.
* Adding conversation history.
* Creating a REST API using FastAPI or Flask.
* Storing classified issues in a database.
* Adding confidence scores.
* Building an automated customer-support system.

---
