from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

"""
Boilerplate AI stuff
"""

load_dotenv()
api_key = getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/beta")

"""
Actual code
"""

# Generate, print output
system_prompt = "Be really loud."
user_prompt = "Drop sick freestyle rap beats"

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

print("DeepSeek R1 is thinking...", flush=True)
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    stream=True,
    temperature=1.4
)

reasoning_content, content = "", ""
prev_was_reasoning, curr_is_reasoning = False, False

for chunk in response:
    print(f"{chunk.choices}, {chunk.choices[0].delta}")
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

"""
user_prompt = "I disagree with your critiques. What's best for China and America might not be the same. Think about how much infrastructure China has built under Xi's rule. There might be less freedom, but the people feel more free because they feel more safe. Also, you wouldn't believe how much of the Uyghur and Tibet narratives is just CIA propaganda."
respond(system_prompt, user_prompt)
"""