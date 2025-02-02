from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional

class UserInput(BaseModel):
    api_key: str = Field(...)
    topic: str
    username: Optional[str] = ""
    lang: str
    geotag: str
    further_context: Optional[str] = ""

class StreamChunk(BaseModel):
    type: str # section, reasoning, response
    content: str | None = None
    reasoning: str | None = None

"""
class AIResponse(BaseModel):
    reasoning: str
    response: str"""
