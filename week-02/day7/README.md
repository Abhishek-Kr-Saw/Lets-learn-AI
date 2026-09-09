# 🛒 Shopping Assistant Agent

A simple **LLM-powered shopping assistant** built with Python and the **Groq API**.

The project demonstrates how to build a basic **ReAct-style AI agent** that can:

* Understand a user's request
* Decide which tool to use
* Call one tool at a time
* Receive the tool's result as an observation
* Perform calculations
* Continue reasoning based on the observation
* Return a final answer

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Technologies Used](#-technologies-used)
4. [Project Structure](#-project-structure)
5. [Prerequisites](#-prerequisites)
6. [Installation](#-installation)
7. [Environment Variables](#-environment-variables)
8. [How the Agent Works](#-how-the-agent-works)
9. [Available Tools](#-available-tools)
10. [Running the Application](#-running-the-application)
11. [Example](#-example)
12. [Understanding the Agent Loop](#-understanding-the-agent-loop)
13. [Important Implementation Details](#-important-implementation-details)
14. [Troubleshooting](#-troubleshooting)
15. [Limitations](#-limitations)
16. [Future Improvements](#-future-improvements)

---

# 📖 Project Overview

This project is a simple shopping assistant that uses an LLM to decide what action it needs to take to answer a user's question.

For example, a user can ask:

> I have 5000 rupees. What is the price of an iPhone 17 and how much money will I have left?

The agent can:

1. Find the price of the iPhone 17.
2. Calculate the remaining amount.
3. Return the final answer.

The project uses a **ReAct-style workflow**:

```text
User Question
      ↓
      LLM
      ↓
   Thought
      ↓
    Action
      ↓
     Tool
      ↓
 Observation
      ↓
      LLM
      ↓
    Action
      ↓
     Tool
      ↓
 Observation
      ↓
 Final Answer
```

---

# ✨ Features

### 🤖 LLM-powered reasoning

The agent uses a Groq-hosted language model to determine what action should be performed.

### 🛠️ Tool calling

The agent currently has two custom tools:

* `get_product_price`
* `calculator`

### 🧮 Calculator

The calculator can evaluate mathematical expressions such as:

```text
5000 - 1000
```

### 🛍️ Product price lookup

The product-price tool currently contains prices for:

```text
iPhone 17 → ₹1000
iPhone 15 → ₹500
```

### 🔄 Agent loop

The agent can perform multiple tool calls before producing its final answer.

### 🔐 Environment variables

The Groq API key is loaded from a `.env` file rather than being hard-coded into the Python source.

---

# 💻 Technologies Used

| Technology      | Purpose                            |
| --------------- | ---------------------------------- |
| Python          | Programming language               |
| Groq            | LLM API                            |
| `python-dotenv` | Loading environment variables      |
| `re`            | Parsing tool actions               |
| `os`            | Reading environment variables      |
| `time.sleep`    | Adding a delay between agent steps |

---

# 📁 Project Structure

A simple project structure can look like this:

```text
shopping-agent/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### `main.py`

Contains the complete agent implementation.

### `.env`

Stores the Groq API key.

### `.gitignore`

Prevents sensitive files such as `.env` from being committed to Git.

### `requirements.txt`

Contains the external Python dependencies.

### `README.md`

This documentation file.

---

# 🧰 Prerequisites

Before running the project, make sure you have:

* Python 3.9 or newer
* A Groq API key
* Internet connection
* `pip`

Check your Python installation:

```bash
python --version
```

Check pip:

```bash
pip --version
```

---

# 📦 Installation

## Step 1 — Clone or download the project

Place the project on your computer.

For example:

```text
D:\Study\shopping-agent
```

Open a terminal inside the project directory.

---

## Step 2 — Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should see something similar to:

```text
(venv) D:\Study\shopping-agent>
```

---

## Step 3 — Install dependencies

Only two external packages are required:

```bash
pip install python-dotenv groq
```

Or create a `requirements.txt` file:

```text
python-dotenv
groq
```

Then run:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

The application requires a Groq API key.

Create a file named:

```text
.env
```

in the root directory.

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

For example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

Do **not** commit this file to GitHub.

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

# ⚙️ How the API Key Is Loaded

The application uses:

```python
from dotenv import load_dotenv
import os

load_dotenv()

myKey = os.getenv("GROQ_API_KEY")
```

The process is:

```text
.env
 │
 │ GROQ_API_KEY
 ↓
load_dotenv()
 │
 ↓
os.getenv()
 │
 ↓
myKey
 │
 ↓
Groq(api_key=myKey)
```

If the API key is missing, the application raises:

```python
raise ValueError("API is missing")
```

---

# 🤖 How the Agent Works

The agent uses a simple ReAct-style pattern.

The system prompt instructs the LLM to use this format:

```text
Thought: what you need to do

Action: tool_name(argument)
```

After the tool executes, the result is returned as:

```text
Observation: result
```

The LLM then decides what to do next.

---

# 🛠️ Available Tools

## 1. `get_product_price`

This tool returns the price of a supported product.

```python
def get_product_price(product):
    product = product.lower().strip()

    if product == "iphone 17":
        return 1000
    elif product == "iphone 15":
        return 500
    else:
        return 0
```

### Example

The LLM generates:

```text
Action: get_product_price("iPhone 17")
```

The Python program extracts:

```text
iPhone 17
```

and calls:

```python
get_product_price("iPhone 17")
```

The result is:

```text
1000
```

The agent receives:

```text
Observation: 1000
```

---

## 2. `calculator`

The calculator evaluates a mathematical expression.

```python
def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error"
```

Example:

```text
Action: calculator("5000 - 1000")
```

The tool returns:

```text
4000
```

The agent receives:

```text
Observation: 4000
```

---

# 🧰 Tool Registry

The tools are stored in a Python dictionary:

```python
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}
```

This allows the agent to dynamically select a tool.

For example:

```python
tool_name = "calculator"
```

Then:

```python
tool = tools[tool_name]
```

and finally:

```python
observation = tool(tool_input)
```

---

# ▶️ Running the Application

Run:

```bash
python main.py
```

The application sends the prompt to the Groq model.

For example:

```text
I have 5000 rupees. What is the price of an iphone 17?

and how much money will I have left?
```

---

# 🧪 Example

A successful execution should look similar to:

```text
------------------
STEP 1
------------------

Action: get_product_price("iPhone 17")

Observation: 1000


------------------
STEP 2
------------------

Action: calculator("5000 - 1000")

Observation: 4000


------------------
STEP 3
------------------

Final Answer: The iPhone 17 costs ₹1000.
You will have ₹4000 remaining.
```

---

# 🔄 Understanding the Agent Loop

The core agent loop is:

```python
for step in range(5):
```

This means the agent can execute a maximum of **5 iterations**.

Each iteration performs the following process:

```text
┌──────────────────────┐
│    Send messages     │
│      to the LLM      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│    Receive response  │
└──────────┬───────────┘
           ↓
      Is it Final?
       /        \
     YES        NO
      ↓          ↓
    STOP    Find Action
                 ↓
          Identify Tool
                 ↓
           Execute Tool
                 ↓
          Get Observation
                 ↓
       Add to conversation
                 ↓
             LLM again
```

---

# 🧠 Conversation Memory

The agent stores previous responses in:

```python
messages
```

Initially:

```python
messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": question
    }
]
```

After a tool call, the assistant response is added:

```python
messages.append({
    "role": "assistant",
    "content": answer
})
```

Then the tool result is added:

```python
messages.append({
    "role": "user",
    "content": "Observation: " + str(observation)
})
```

This allows the LLM to see what happened during previous steps.

---

# 🔍 Action Parsing

The application uses Python's `re` module to find an action generated by the LLM.

The recommended pattern is:

```python
match = re.search(
    r'Action:\s*(\w+)\("(.*?)"\)',
    answer
)
```

For:

```text
Action: get_product_price("iPhone 17")
```

the regex extracts:

```text
Tool name:
get_product_price

Tool input:
iPhone 17
```

These values are then used to execute the correct Python function.

---

# 🛡️ Case Handling

Product names may come from the LLM in different cases:

```text
iPhone 17
iphone 17
IPHONE 17
```

Therefore, the product name should be normalized:

```python
product = product.lower().strip()
```

This ensures all of the above become:

```text
iphone 17
```

---

# ⚠️ Important Note About `eval()`

The calculator currently uses:

```python
eval(expression)
```

This is acceptable for a small learning project, but **should not be used directly with untrusted user input in a production application**.

For example, arbitrary Python expressions can potentially be executed through `eval()`.

For a production application, replace it with a safe mathematical expression parser or restrict the allowed operations.

---

# 🐛 Troubleshooting

## API key error

If you see:

```text
ValueError: API is missing
```

Check that `.env` exists:

```text
shopping-agent/
├── main.py
├── .env
└── README.md
```

And contains:

```env
GROQ_API_KEY=your_key
```

---

## Product price returns `0`

If:

```text
Observation: 0
```

is returned for a known product, check the product matching logic.

Use:

```python
product = product.lower().strip()
```

before comparing the product.

---

## Agent repeats the final answer

The LLM may sometimes produce a normal answer without:

```text
Final Answer:
```

The agent should stop when there is no valid `Action` instead of repeatedly calling the LLM.

For example:

```python
if "Final Answer:" in answer:
    break

if not match:
    break
```

---

## Tool not found

If you see:

```text
Tool not found
```

check that the tool name generated by the LLM exactly matches a key in:

```python
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}
```

For example:

```text
get_product_price
```

is valid.

But:

```text
getProductPrice
```

is not registered.

---

# ⚠️ Current Limitations

This is a learning/demo implementation and has several limitations.

### Product database is hard-coded

Currently:

```text
iPhone 17 → ₹1000
iPhone 15 → ₹500
```

There is no real product database or e-commerce API.

### Prices are not real-world prices

The values are only demonstration data.

### Limited number of steps

The agent currently runs:

```python
for step in range(5):
```

so it can perform at most five iterations.

### Basic action parser

The agent relies on the LLM following a strict text format.

### `eval()` security risk

The calculator should not use unrestricted `eval()` in production.

### No persistent memory

Conversation history exists only during the current execution.

---

# 🚀 Future Improvements

This project can be extended in several ways.

## 🛍️ Real product search

Replace the hard-coded function with a real product database or API.

```text
User
 ↓
Agent
 ↓
Product Search API
 ↓
Real Product Data
```

## 💰 Currency support

Add support for:

```text
₹
$
€
£
```

and currency conversion.

## 🧮 Safer calculator

Replace `eval()` with a safe expression parser.

## 🧠 More tools

For example:

```text
get_product_price()
search_product()
compare_products()
calculate_discount()
calculate_tax()
check_stock()
```

## 💾 Persistent memory

Store conversations in:

```text
SQLite
PostgreSQL
MongoDB
Redis
```

## 🌐 Web interface

Build a frontend using:

```text
HTML
CSS
JavaScript
```

or:

```text
React
```

## 🔧 Native tool calling

Instead of asking the LLM to produce:

```text
Action: calculator("5000 - 1000")
```

the application can eventually use the model/API's structured tool-calling functionality.

---

# 📌 Quick Start

If you just want to run the project:

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install python-dotenv groq

# Create .env
GROQ_API_KEY=your_groq_api_key

# Run
python main.py
```

---

# 🎯 Learning Objective

This project is primarily designed to demonstrate the fundamentals of building an **AI agent with tools**.

The most important concept is not the shopping functionality itself, but the interaction between:

```text
LLM
 ↓
Reasoning
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
Observation
 ↓
Reasoning
 ↓
Final Answer
```

This provides a foundation for more advanced AI-agent systems such as:

* Tool-using agents
* ReAct agents
* Multi-tool agents
* AI assistants
* RAG agents
* API-integrated agents
* Autonomous workflows

---

