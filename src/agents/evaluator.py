from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
import random

class State(TypedDict):
    nodes: list[str]
    
def generator_node(state: State):
    return state

def evaluator_node(state: State):
    return state

def route_edge(state: State) -> Literal[END,'generator_node']:
    if random.random() < 0.5:
        return END
    return 'generator_node'

builder = StateGraph(State)

builder.add_node('generator_node',generator_node)
builder.add_node('evaluator_node',evaluator_node)

builder.add_edge(START,'generator_node')
builder.add_edge('generator_node','evaluator_node')
builder.add_conditional_edges('evaluator_node', route_edge)

agent = builder.compile()