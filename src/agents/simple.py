from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import AIMessage, HumanMessage
class State(MessagesState):
    customer_name: str
    my_age: int

def node_1(state: State):
    history = state["messages"]
    if state.get("customer_name") is None:
       return {
           "customer_name": "John Doe"
       }
    else:
        ai_msg = AIMessage(content=f"Hello, {state.get('customer_name')}, how can I help you today?")
        return {
            "messages": [ai_msg]
        }
    
    


builder = StateGraph(State)
builder.add_node("node_1",node_1)

builder.add_edge(START,'node_1')
builder.add_edge('node_1',END)

agent = builder.compile()
