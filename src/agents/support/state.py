from langgraph.graph import MessagesState

class State(MessagesState):
    customer_name: str
    my_age: int
    phone: str