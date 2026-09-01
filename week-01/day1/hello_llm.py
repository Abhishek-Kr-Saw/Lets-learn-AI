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

# models = client.models.list()

# for model in models.data:
#     print(model.id)