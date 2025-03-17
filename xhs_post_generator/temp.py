from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv
from typing import Optional

"""
Boilerplate AI stuff
"""

load_dotenv()
api_key = getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/beta")

"""
Actual code
"""

# Define user input schema
class UserInput():
    topic: str
    username: Optional[str] = ""
    lang: str
    geotag: str
    further_context: Optional[str] = ""

# Read in system prompt from txt
with open("deepseek\system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# Prompt user for input
## TODO: actual topics
topic = "苏州"
username = ""
lang = "中文"
geotag = "北京"
further_context = ""

user_input = {
    "topic" : topic,
    "username": username,
    "lang": lang,
    "geotag": geotag,
    "further_context": further_context
}

user_prompt = f"""
==INPUT== 
Follow EXACTLY!
- Topic: {user_input["topic"]}
- Username (default=random): {username}
- Language: {lang}
- Geotag: {geotag}
- Further context: {further_context}
"""

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
]

# Generate, print output
print("DeepSeek R1 is thinking...")
try:
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True,
        temperature=1.4
    )
except Exception as e:
    print(f"Error: {e}")

reasoning_content, content = "", ""
prev_was_reasoning, curr_is_reasoning = False, False

for chunk in response:
    if chunk.choices and chunk.choices[0].delta:
        delta = chunk.choices[0].delta
        has_reasoning, has_content = bool(delta.reasoning_content), bool(delta.content)
        if has_reasoning:
            if not curr_is_reasoning:
                print("\n[Reasoning]\n", end="", flush=True)
                curr_is_reasoning = True
            reasoning_content += delta.reasoning_content
            print(delta.reasoning_content, end="", flush=True)
        
        elif has_content:
            if prev_was_reasoning:
                print("\n\n[Response]\n", end="", flush=True)
                curr_is_reasoning = False
            content += delta.content
            print(delta.content, end="", flush=True)
    
    prev_was_reasoning = curr_is_reasoning

# TODO: multi-round conversation support
# messages.append({"role": "assistant", "content": content})
# messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})

# TODO: "more detailed try again"