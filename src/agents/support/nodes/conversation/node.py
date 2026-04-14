from agents.support.llm import get_chat_model, is_ollama_backend
from agents.support.state import State
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT
from agents.support.nodes.conversation.tools import tools
from langchain.messages import AIMessage

_base_llm = get_chat_model(temperature=0, tier="full")
llm = _base_llm if is_ollama_backend() else _base_llm.bind_tools(tools)

def conversation_node(state: State):
    new_state: State = {}
    history = state["messages"]
    last_message = history[-1].text
    customer_name = state.get('customer_name', 'John Doe')
    ai_message = llm.invoke([("system",SYSTEM_PROMPT.format(customer_name=customer_name)),("user",last_message)])
    raw = ai_message.content
    if isinstance(raw, str):
        text_content = raw
    else:
        text_content = ""
        for block in raw:
            if isinstance(block, dict) and "text" in block:
                text_content += block["text"]
            elif isinstance(block, str):
                text_content += block
    # Reemplazamos el contenido complejo con el texto plano
    ai_message.content = text_content
    ai_message = AIMessage(content=ai_message.text)

    new_state["messages"] = [ai_message]
    # Al devolver el nuevo state, se actualiza la memoria del agente
    return new_state