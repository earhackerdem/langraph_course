from pydantic import BaseModel, Field

from agents.support.llm import get_chat_model
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT
from agents.support.state import State

class ContactInfo(BaseModel):
    """Contact information for a person"""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email of the address of the person")
    phone: str = Field(description="The phone number of the person")
    age: int = Field(description="The age of the person")

llm = get_chat_model(temperature=0, tier="full").with_structured_output(
    schema=ContactInfo
)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state: State = {}
    if customer_name is None or len(history) >= 10:
        schema =llm.invoke([("system",SYSTEM_PROMPT)]+history)
        new_state["customer_name"] = schema.name
        new_state["my_age"] = schema.age
        new_state["phone"] = schema.phone
    return new_state