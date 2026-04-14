from api.db import CheckpointerDep, lifespan
from dotenv import load_dotenv
from fastapi.routing import StreamingResponse
load_dotenv()


from typing import Union
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from agents.support.agent import make_graph

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Message(BaseModel):
    message:str

@app.post("/chat/{chat_id}")
async def chat(chat_id: str, item: Message, checkpointer: CheckpointerDep):
    config = {
        'configurable':{
            'thread_id': chat_id
        }
    }
    human_message = HumanMessage(content=item.message)
    agent = make_graph(config={"checkpointer":checkpointer})
    state = {"messages": [human_message], "customer_name":"John Doe"}
    response = agent.invoke(state,config)
    last_message = response['messages'][-1]
    return last_message.text


@app.post("/chat/{chat_id}/stream")
async def stream_chat(chat_id: str, message:Message, checkpointer: CheckpointerDep):
    human_message = HumanMessage(content=message.message)
    async def generate_response():
        agent = make_graph(config={"checkpointer":checkpointer})
        for message_chunk, metadata in agent.stream({"messages":[human_message]}, stream_mode="messages"):
            if message_chunk.content:
                yield f"data: {message_chunk.content}\n\n"
                
        print(message_chunk.content, end="|", flush=True)
        
    return StreamingResponse(generate_response(), media_type="text/event-stream")