from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI

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
    
    
def extractor(state: State):
    return {}

def conversation_node(state: State):
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "John Doe"
    else:
        new_state["my_age"] = random.randint(20, 30)
    
    history = state["messages"]
    last_message = history[-1].text
    ai_message = llm.invoke(last_message)
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
