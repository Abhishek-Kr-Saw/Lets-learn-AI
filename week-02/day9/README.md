# Groq API Streaming in Python

This example demonstrates how to use the **Groq API** with Python to generate an AI response and stream the response chunk by chunk.

## 1. Install Dependencies

Install the required packages:

```bash
pip install groq python-dotenv
```

Or with `uv`:

```bash
uv add groq python-dotenv
```

---

## 2. Environment Variables

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_api_key_here
```

**Do not commit your `.env` file to Git**, because it contains your API key.

---

## 3. Complete Code

```python
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Get API key
apiKey = os.getenv('GROQ_API_KEY')

if not apiKey:
    raise ValueError('API key is missing...')

# Create Groq client
client = Groq(api_key=apiKey)

# Model to use
model = 'openai/gpt-oss-120b'

# User prompt
role = 'user'
prompt = 'Explain AI Engineering in 100 words.'

# Create message
message = {
    "role": role,
    "content": prompt
}

# Messages expected by the API
messages = [message]


# --------------------------------------------------
# Response WITHOUT streaming
# --------------------------------------------------
# The complete response is returned at once.

# response = client.chat.completions.create(
#     model=model,
#     messages=messages
# )

# print(response.choices[0].message.content)


# --------------------------------------------------
# Response WITH streaming
# --------------------------------------------------

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)

for chunk in stream:

    # Get the content from the current chunk
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)

# flush=True:
# Immediately send the printed content to the terminal.
```

---

# Streaming vs Non-Streaming

## Non-Streaming

Without streaming:

```python
response = client.chat.completions.create(
    model=model,
    messages=messages
)

print(response.choices[0].message.content)
```

The API waits until the **entire response is generated**.

For example:

```text
Request
   ↓
AI generates complete response
   ↓
Complete response returned
   ↓
Print response
```

---

## Streaming

With:

```python
stream=True
```

the response is sent in smaller chunks as the model generates it.

```text
Request
   ↓
AI generates first chunk → receive it
   ↓
AI generates next chunk  → receive it
   ↓
AI generates next chunk  → receive it
   ↓
...
   ↓
Response complete
```

The Python code processes these chunks using:

```python
for chunk in stream:
```

---

# Understanding `chunk`

Each iteration gives you a piece of the response.

For example, the model might generate:

```text
"AI"
```

then:

```text
" Engineering"
```

then:

```text
" is"
```

then:

```text
" the"
```

then:

```text
" practice..."
```

The code:

```python
content = chunk.choices[0].delta.content
```

extracts the text from the current chunk.

---

# Understanding `end=""`

Normally:

```python
print("Hello")
print("World")
```

produces:

```text
Hello
World
```

because `print()` automatically adds a newline.

It is equivalent to:

```python
print("Hello", end="\n")
```

When streaming, we don't want a new line after every chunk.

Therefore:

```python
print(content, end="")
```

produces:

```text
Hello World
```

instead of:

```text
Hello
 World
```

---

# Understanding `flush=True`

Python can temporarily store output in a buffer before displaying it.

Using:

```python
flush=True
```

forces Python to display the output immediately.

Therefore:

```python
print(content, end="", flush=True)
```

means:

> Print this chunk immediately without adding a newline.

This is especially useful for **LLM streaming**, because the user can see the response being generated in real time.

---

# Final Streaming Code

The important part is:

```python
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
```

### In simple terms

| Code                  | Purpose                          |
| --------------------- | -------------------------------- |
| `stream=True`         | Enable response streaming        |
| `for chunk in stream` | Process each response chunk      |
| `chunk.choices[0]`    | Access the first response choice |
| `delta.content`       | Get text from the current chunk  |
| `end=""`              | Don't create a new line          |
| `flush=True`          | Display the chunk immediately    |

---

# Why Streaming Is Useful

Streaming is commonly used in:

* AI chat applications
* ChatGPT-like interfaces
* AI coding assistants
* Terminal AI agents
* Real-time text generation
* AI APIs using Server-Sent Events (SSE)

Instead of making the user wait for the complete response, the application can display the response as it is generated.
