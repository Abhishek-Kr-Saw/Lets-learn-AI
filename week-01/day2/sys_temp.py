import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")

if not key:
    raise ValueError("API key is missing")

client = Groq(api_key=key)

# models = client.models.list()

# for model in models.data:
#     print(model.id)

model = "openai/gpt-oss-20b"

role = "user"

prompt = "Suggest me two MERN stack project with some details which shortlist my resume in any product based company."

message_system = {
    "role": "system",
    "content":"You are a manager of a product based company."
}

message = {
    "role": role,
    "content": prompt
}

messages = [message_system,message]


#tempertaure by default is 0 and range between [0,2]
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)


print("------------------------------------------------")

print(response.choices[0].message.content)

print("------------------------------------------------")



