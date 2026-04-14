from agents.support.routes.intent.prompt import SYSTEM_PROMPT
from pydantic import BaseModel, Field
from typing import Literal

from agents.support.llm import get_chat_model
from agents.support.state import State


class RouteIntent(BaseModel):
    """Contact information for a person. """
    step: Literal['conversation_node','booking'] = Field(
        None, description="The next step in the routing process"
    )

llm = get_chat_model(temperature=0, tier="full")
llm = llm.with_structured_output(schema=RouteIntent)

def intent_route(state: State) -> Literal["conversation_node","booking"]:
    history = state["messages"]
    print("*"*100)
    print(history)
    print("*"*100)
    schema = llm.invoke([("system",SYSTEM_PROMPT)] + history)
    if schema.step is not None:
        return schema.step
    return "conversation_node"