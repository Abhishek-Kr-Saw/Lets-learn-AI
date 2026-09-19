import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

apiKey = os.getenv('GROQ_API_KEY')
if not apiKey:
    raise ValueError('API key is missing...')

client = Groq(api_key=apiKey)
model = 'openai/gpt-oss-120b'

role = 'user'
prompt = 'Explain AI Engineering in 100 words.' 

message = {
    "role": role,
    "content": prompt
}

messages = [message]


# Response without streaming - everything in one go
# response = client.chat.completions.create(
#     model=model,
#     messages=messages
# )

# print(response.choices[0].message.content)


stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream = True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)

# flush=True : Immediately send the printed content to the terminal.