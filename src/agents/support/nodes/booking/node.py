from langchain.agents import create_agent

from agents.support.llm import get_chat_model
from agents.support.nodes.booking.prompt import prompt_template
from agents.support.nodes.booking.tools import tools

booking_node = create_agent(
    model=get_chat_model(temperature=0, tier="mini"),
    tools=tools,
    system_prompt=prompt_template.format(),
)

# Run the agent
