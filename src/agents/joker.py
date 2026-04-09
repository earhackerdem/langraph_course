from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

class State(TypedDict):
    joke: str
    topic: str
    feedback: str
    is_funny: str
    
class Feedback(BaseModel):
    is_funny: bool = Field(
        description="Decide if the joke is funny or not. Return True if it is, False otherwise."
    )
    feedback: str = Field(
        description="If the joke is not funny, provide feedback on how to improve it."
    )
    
llm = init_chat_model("openai:gpt-4.1-mini", temperature=0)
ll_evaluator = llm.with_structured_output(Feedback,temperature=0)

SYSTEM_PROMPT = """
A joke to be funny must be greater than three lines
"""


def generator_node(state: State):
    feedback = state.get('feedback',None)
    topic = state.get('topic',None)
    if feedback:
        msg = llm.invoke(f"Write a joke about {topic} but take into account the feedback:{feedback} respond in Spanish")
    else:
        msg = llm.invoke(f"Write a joke about {topic} respond in Spanish")
    return {"joke":msg.text}

def evaluator_node(state: State):
    joke = state.get("joke", None)
    schema = ll_evaluator.invoke(f"Grade the joke {joke} with the Following Prompt: {SYSTEM_PROMPT}")
    return {'is_funny': schema.is_funny, "feedback" : schema.feedback}

def route_edge(state: State) -> Literal[END,"generator"]:
    is_funny = state.get("is_funny",True)
    if is_funny:
        return END
    else:
        return "generator"

builder = StateGraph(State)

builder.add_node('generator',generator_node)
builder.add_node('evaluator',evaluator_node)

builder.add_edge(START,'generator')
builder.add_edge('generator','evaluator')
builder.add_conditional_edges('evaluator',route_edge)

agent = builder.compile()