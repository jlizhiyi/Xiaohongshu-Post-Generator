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

messages = []

# Generate, print output
def respond(system_prompt, user_prompt):
    messages.extend([
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }]
    )
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True,
        temperature=1.4
    )

    reasoning_content, content = "", ""
    prev_was_reasoning, curr_is_reasoning = False, False

    print("DeepSeek R1 is thinking...", flush=True)
    for chunk in response:
        #print(f"{chunk.choices}, {chunk.choices[0].delta}")
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
    messages.append({"role": "system", "content" : content})

system_prompt = ""
user_prompts = [
    """
        John Wang is born in the US to Mr. Wang and Mrs. Li, who have green cards and are legal permanent residents of the US, but carry PRC passports and lack US citizenship.

        Since the US currently has birthright citizenship, John is born a US citizen, and since the PRC does not recognize dual citizenship, he is only a US citizen and not a PRC citizen. However, if John likes, can he relinquish his US citizenship for PRC citizenship and move to China later in life?
    """,
    """
        James White is born in the US to Mr. White and Mrs. White, who were both born in the US and are US citizens.

        James White and his family have no ties to the PRC at the time of his birth, however James grows up to love China, and wants to move there. He familiarizes himself with China's language and culture in the meantime, but of course, the process towards PRC naturalization is rocky and difficult. But my question is this: are John Wang (from the previous question) and James White on an equal footing when it comes to competing for PRC citizenship, or does one person have a head-start over the other?
    """,
    """
        Jeremy Wei is born in the US to Mr. Wei and Mrs. Zhang, who had green cards and were legal permanent residents of the US, but carried PRC passports and lacked US citizenship at the time of their son's birth.

        Since the US currently has birthright citizenship, Jeremy is born a US citizen, and since the PRC does not recognize dual citizenship, he is only a US citizen and not a PRC citizen. Eventually, by the time Jeremy entered middle school, both of his parents had passed the US citizenship test, allowing them to vote in elections etc., and in doing so, they had to relinquish their PRC citizenship. Meanwhile, Jeremy became interested in his heritage, and is thinking about moving to China and getting PRC citizenship.

        My new question is as follows: where does Jeremy Wei fall in the queue? Somewhere near John Wang (another ABC whose situation is similar to his own, except his parents still have PRC citizenship), somewhere near James White (a laowai born with 0 Chinese connections or ancestry), or somewhere else entirely?
    """
]
for user_prompt in user_prompts:
    respond(system_prompt, user_prompt)