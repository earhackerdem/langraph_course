from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT
from agents.support.nodes.conversation.tools import tools



llm = init_chat_model("openai:gpt-4o",temperature=0)
llm = llm.bind_tools(tools)

def conversation_node(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1].text
    customer_name = state.get('customer_name', 'John Doe')
    ai_message = llm.invoke([("system",SYSTEM_PROMPT.format(customer_name=customer_name)),("user",last_message)])
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