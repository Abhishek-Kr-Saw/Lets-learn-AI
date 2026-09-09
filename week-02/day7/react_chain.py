import os
from dotenv import load_dotenv
from time import sleep
from groq import Groq
import re

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API is missing")

client = Groq(api_key=api_key)
model = "openai/gpt-oss-120b"

def get_product_price(product):
    product = product.lower().strip()

    if product == "iphone 17":
        return 1000
    elif product == "iphone 15":
        return 500
    else:
        return 0


def calculator(expression: str):    
    try:
        return eval(expression)
    except Exception:
        return "Calculation error"
    

tools = {
    "get_product_price" : get_product_price,
    "calculator" : calculator
}

system_prompt = f"""
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)
IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="ihhone 17")

Never write:
calculator(expression="5000 - 1000")
Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""


def run_agent(question):

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

    MAX_STEPS = 5

    for step in range(MAX_STEPS):

        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")

        response = client.chat.completions.create(
            model = model,
            messages = messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)

        #When agent has finished its task
        if "Final Answer:" in answer:
            break

        # Find the action
        match = re.search(
            r'Action:\s*(\w+)\("(.*?)"\)',
            answer
        )

        if match:

            tool_name = match.group(1)

            tool_input = match.group(2)

            tool_input = tool_input.strip()

            tool_input = tool_input.strip('"')

            # Run the tool
            if tool_name in tools:

                tool = tools[tool_name]

                observation = tool(tool_input)

            else:

                observation = "Tool not found"


            print(
                "Observation:",
                observation
            )

            # Add LLM response to memory
            messages.append({
                "role": "assistant",
                "content": answer
            })


            # Give tool result back to LLM
            messages.append({
                "role": "user",
                "content":
                    "Observation: "
                    + str(observation)
            })

            # sleep(5)


prompt="""
I have 5000 rupees. What is the price of an iphone 17?
and how much money will I have left?
"""
run_agent(prompt)
