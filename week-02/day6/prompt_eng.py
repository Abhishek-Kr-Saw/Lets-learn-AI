import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv('GROQ_API_KEY')
if not key:
    raise ValueError('API key is missing')

client = Groq(api_key = key)
model = 'openai/gpt-oss-120b'

print("------------------------------------")

def llm_ans(prompt):
    message = {
        "role":"user",
        "content":prompt
    } 
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages)
    ans = response.choices[0].message.content
    return ans


prompt = f"""
#Role
You are a support asssistant at mobile/laptop commplany
#Task
You have to classify the issue in a category
#CONSTRAINT
You have to classify the issue in one of three categories namely billing, technical, return
#OUTPUT FORMAT
Your answer should be in one world only. The one word should be one of the categories given in contraints
#EXAMPLE
For instance if a user complain says he want a refund then the category is return
#FALLBACK
If the issue is unrelated to any of the categories mentioned in constraints, then the answer should be other
My laptop is not working.
"""

print(llm_ans(prompt))
print("------------------------------------")