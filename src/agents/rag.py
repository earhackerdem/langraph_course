from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
class ContactInfo(BaseModel):
    """Contact information for a person"""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email of the address of the person")
    phone: str = Field(description="The phone number of the person")
    age: int = Field(description="The age of the person")

llm_with_structured_output = ChatOpenAI(model='gpt-4o', temperature=0).with_structured_output(schema=ContactInfo)

import random

llm = ChatOpenAI(model='gpt-4o', temperature=0)

file_search_tool = {
    "type": "file_search",
    "vector_store_ids" : ['vs_69af0b45173081918ccbab0b48bc49fe']
}

llm = llm.bind_tools([file_search_tool])

class State(MessagesState):
    customer_name: str
    my_age: int
    phone: str
    
    
def extractor(state: State):
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(state["messages"]) >= 10:
        schema =llm_with_structured_output.invoke(state["messages"])
        new_state["customer_name"] = schema.name
        new_state["my_age"] = schema.age
        new_state["phone"] = schema.phone
    return new_state

def conversation_node(state: State):
    new_state: State = {}

    
    history = state["messages"]
    last_message = history[-1].text
    customer_name = state.get('customer_name', 'John Doe')
    system_message = f"You are a helpful assistant that can extract information from a conversation. The customer name is {customer_name}"
    ai_message = llm.invoke([("system",system_message),("user",last_message)])
    text_content = ""
    for block in ai_message.content:
        if isinstance(block, dict) and "text" in block:
            text_content += block["text"]
        elif isinstance(block, str):
            text_content += block
    # Reemplazamos el contenido complejo con el texto plano
    ai_message.content = text_content

    new_state["messages"] = [ai_message]
    # Al devolver el nuevo state, se actualiza la memoria del agente
    return new_state


builder = StateGraph(State)
builder.add_node("conversation_node",conversation_node)
builder.add_node("extractor_node",extractor)


builder.add_edge(START,'extractor_node')
builder.add_edge('extractor_node','conversation_node')
builder.add_edge('conversation_node',END)


agent = builder.compile()
