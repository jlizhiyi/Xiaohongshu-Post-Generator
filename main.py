from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from src.client.ai_client import AIClient
from src.models.schema import UserInput

app = FastAPI()

@app.post("/generate")
async def generate_content(user_input: UserInput):
    try:
        ai_client = AIClient(user_input.api_key.get_secret_value())
        async def stream_response():
            async for chunk in ai_client.respond(user_input):
                yield f"data: {chunk.model_dump_json()}\n\n"
        return StreamingResponse (
            stream_response(),
            media_type = "text/event-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# TODO: front-end