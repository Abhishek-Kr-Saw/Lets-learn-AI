import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")
if not key : 
    raise ValueError("Api key is missing")

client = Groq(api_key = key)

model = "openai/gpt-oss-120b"

role = 'user'


# structuer output
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema()

#response type
response_format = {
    "type":"json_object"
} 

system_prompt = f"""
    Extract personal info from this ticket and return in json format
    {schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}

text = 'Hi I am Abhishek from Delhi, I bought iphone from your store and is not working, My email is abc@gmail.com. I am 25 years old.'

prompt = f"""
    This is customer ticket . Please extract the personal info from this
    {text}
"""

message = {
    'role':role,
    'content': prompt
}

messages = [message_system, message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)

content = (response.choices[0].message.content)

ticket = Ticket.model_validate_json(content)

# print(content)

print(ticket)
print(ticket.name)
print(ticket.email)
print(ticket.issue)
