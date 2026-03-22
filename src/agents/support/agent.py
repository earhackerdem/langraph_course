from langgraph.graph import StateGraph, START, END
from agents.support.state import State
from agents.support.nodes.extractor.node import extractor
from agents.support.nodes.conversation.node import conversation_node


builder = StateGraph(State)
builder.add_node("conversation_node",conversation_node)
builder.add_node("extractor_node",extractor)


builder.add_edge(START,'extractor_node')
builder.add_edge('extractor_node','conversation_node')
builder.add_edge('conversation_node',END)


agent = builder.compile()
