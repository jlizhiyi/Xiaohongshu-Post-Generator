from dotenv import load_dotenv
import logging
from openai import OpenAI
from src.models.schema import UserInput, StreamChunk
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

class AIClient:
    def __init__ (self, api_key: str):
        self.client = OpenAI (
            api_key = api_key,
            base_url = "https://api.deepseek.com/beta"
        )
        self.system_prompt = self.load_system_prompt()

    def load_system_prompt(self) -> str:
        try:
            with open("src/prompts/system_prompt.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("system_prompt.txt not found")
            raise

    def format_user_prompt(self, user_input: UserInput) -> str:
        return f"""
==INPUT==
Follow EXACTLY!
- Topic: {user_input.topic}
- Username (default=random): {user_input.username}
- Language: {user_input.lang}
- Geotag: {user_input.geotag}
- Further context: {user_input.further_context}
"""
    
    async def respond(self, user_input: UserInput) -> AsyncGenerator[StreamChunk, None]:
        try:
            logger.info("DeepSeek R1 is thinking...")
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.format_user_prompt(user_input)
                }
            ]

            response = self.client.chat.completions.create(
                model="deepseek-reasoner",
                messages=messages,
                stream=True,
                temperature=1.4
            )
            reasoning_content, content = "", ""
            prev_was_reasoning, curr_is_reasoning = False, False

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta:
                    delta = chunk.choices[0].delta
                    has_reasoning, has_content = bool(delta.reasoning_content), bool(delta.content)
                    if has_reasoning:
                        if not curr_is_reasoning:
                            yield StreamChunk(type="section", content="[Reasoning]")
                            curr_is_reasoning = True
                        reasoning_content += delta.reasoning_content
                        yield StreamChunk(
                            type="reasoning",
                            reasoning=delta.reasoning_content
                        )
                    
                    elif has_content:
                        if prev_was_reasoning:
                            yield StreamChunk(type="section", content="[Response]")
                            curr_is_reasoning = False
                        content += delta.content
                        yield StreamChunk(
                            type="response",
                            content=delta.content
                        )
                
                prev_was_reasoning = curr_is_reasoning

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
