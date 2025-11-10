from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from agents.basic_agent import agent  # 네가 쓰는 agent
import json

app = FastAPI(title="Agent API", version="0.1.0")


# 요청 바디 스키마
class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "agent 살아있음"}


# 1) 한 번에 답 받는 엔드포인트
@app.post("/chat")
async def chat(req: ChatRequest):
    last_text = ""
    # 네가 터미널에서 하던 패턴 그대로
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": req.message}]},
        stream_mode="values",
    ):
        latest_message = chunk["messages"][-1]
        if latest_message.content:
            last_text = latest_message.content

    return {"answer": last_text}


# 2) 스트리밍으로 받는 엔드포인트 (SSE 스타일)
@app.post("/chat/stream")
async def chat_stream(req: Request):
    body = await req.json()
    user_msg = body.get("message", "")

    def event_gen():
        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": user_msg}]},
            stream_mode="values",
        ):
            latest_message = chunk["messages"][-1]

            if latest_message.content:
                data = {"type": "message", "content": latest_message.content}
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            elif latest_message.tool_calls:
                data = {
                    "type": "tool_calls",
                    "tools": [tc["name"] for tc in latest_message.tool_calls],
                }
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

        # 끝났다고 알림
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")
