import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

myKey=os.getenv("GROQ_API_KEY")

if not myKey:
    raise ValueError("API is missing")

client = Groq(api_key = myKey)

model = "openai/gpt-oss-20b"

role = "user"

prompt1 = "Hi"
prompt2 = "Explain time travel"
prompt3 = "Write large essay on Machine Learning"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
        "role":role,
        "content":prompt
    }  
    messages=[message]
    response = client.chat.completions.create(model=model,messages=messages, max_tokens=2000)
    usage=response.usage
    print(f"Prompt : {prompt} --> your token: {usage.prompt_tokens} completions_token: {usage.completion_tokens} total tokens: {usage.total_tokens} Final Reason: {response.choices[0].finish_reason}")


# Prompt : Hi --> your token: 72 completions_token: 43 total tokens: 115 Final Reason: stop
# Prompt : Explain time travel --> your token: 74 completions_token: 1917 total tokens: 1991 Final Reason: stop
# Prompt : Write large essay on Machine Learning --> your token: 77 completions_token: 2000 total tokens: 2077 Final Reason: length