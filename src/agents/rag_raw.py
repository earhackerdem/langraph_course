from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI


client = OpenAI()


class ContactInfo(BaseModel):
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: int = Field(description="The age of the person")


class State(TypedDict, total=False):
    messages: List[dict]
    customer_name: Optional[str]
    my_age: Optional[int]
    phone: Optional[str]


def extractor(state: State) -> State:
    customer_name = state.get("customer_name")
    messages = state.get("messages", [])

    if customer_name is not None and len(messages) < 10:
        return {}

    response = client.responses.parse(
        model="gpt-4o",
        input=messages,
        text_format=ContactInfo,
    )

    contact = response.output_parsed

    return {
        "customer_name": contact.name,
        "my_age": contact.age,
        "phone": contact.phone,
    }


def conversation_node(state: State) -> State:
    messages = state.get("messages", [])
    last_message = messages[-1]["content"] if messages else ""
    customer_name = state.get("customer_name", "John Doe")

    system_message = (
        "You are a helpful assistant that can extract information from a conversation. "
        f"The customer name is {customer_name}"
    )

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": last_message},
        ],
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": ["vs_69af0b45173081918ccbab0b48bc49fe"],
            }
        ],
    )

    text_content = response.output_text

    return {
        "messages": messages + [{"role": "assistant", "content": text_content}]
    }


def run_agent(state: State) -> State:
    extracted_data = extractor(state)
    state = {**state, **extracted_data}

    conversation_data = conversation_node(state)

    if "messages" in conversation_data:
        state["messages"] = conversation_data["messages"]

    return state


initial_state: State = {
    "messages": [
        {"role": "user", "content": "Hola, soy Carlos, tengo 32 años y mi teléfono es 555-1234"}
    ]
}

final_state = run_agent(initial_state)

print(final_state)