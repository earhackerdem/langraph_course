from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

import random

llm = init_chat_model("gemini-2.5-flash",model_provider="google_genai",temperature=0)
gpt4o_llm = ChatOpenAI(model='gpt-4o', temperature=0)

class State(MessagesState):
    customer_name: str
    my_age: int

def node_1(state: State):
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
    else:
        new_state["my_age"] = random.randint(20, 30)
    
    history = state["messages"]
    if history == []:
        ai_message = gpt4o_llm.invoke('')
    else:
        ai_message = gpt4o_llm.invoke(history)
    new_state["messages"] = [ai_message]
    return new_state

builder = StateGraph(State)
builder.add_node("node_1",node_1)
builder.add_edge(START,'node_1')
builder.add_edge('node_1',END)
agent = builder.compile()
