from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import message
from langgraph.prebuilt.chat_agent_executor import ToolMessage
import json
import os

from .prompts import sot_system_prompt
from .vectorstores import truth_vector_store
from .vectorstores import command_vector_store
from .tools import source_of_truth_tools
from .agents import (
    chat_type_agent, 
    assistant_agent,
    source_of_truth_agent,
)
import json


def sot_tool_node_action(state):
    print("sot_tool_node_action")
    outputs = []
    for tool_call in state["sot_messages"][-1].tool_calls:
        print("tool name: ", tool_call["name"])
        print("tool args: ",tool_call["args"])
        tool_result = source_of_truth_tools[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"]
            )
        )
    return {"sot_messages": state["sot_messages"] + outputs}

def chat_type_action(state, config):
    print("check_chat_type_action")
    messages = state["messages"]
    content = messages[-1].content
    response = chat_type_agent.invoke({"message": content})# pyright: ignore
    chat_type = response.phrase_type # pyright: ignore
    if config["configurable"].get("enable_test") and config["configurable"].get("test"):
        if not config["configurable"]["test"][0](chat_type):
            raise Exception(f"Test failed: chat_type == {chat_type}. Expected: {config["configurable"]["test"][1]}")
        chat_type = config["configurable"]["test"][1]

    return {"chat_type": chat_type} 

def source_of_truth_action(state, config):
    enable_tools = False
    if os.environ.get("ENABLE_TOOLS") and os.environ["ENABLE_TOOLS"] == "true":
        enable_tools = True

    messages = state["messages"]

    sot_context = ""
    sot_messages = None
    if state.get("sot_context"):
        sot_context = state["sot_context"]
    if not state.get("sot_messages"):
        content = messages[-1]
        sot_messages = [SystemMessage(content=sot_system_prompt)] + [content]
    else:
        sot_messages = state["sot_messages"]

    if enable_tools:
        last_message = sot_messages[-1]
        if isinstance(last_message, ToolMessage):
            sot_context = sot_context + str(last_message.content)

    response = source_of_truth_agent.invoke(sot_messages) # pyright: ignore
    truth_validation_type = "falso" 
    assistant_message = None 

    if enable_tools: 
        if isinstance(response, AIMessage):
            try:
                result = json.loads(response.content) # pyright: ignore
                truth_validation_type = result["tipo"]
                assistant_message = result["confirmacao"]
            except Exception as e:
                pass
    else:
        try:
            result = json.loads(response.content) # pyright: ignore
            truth_validation_type = result["tipo"]
            assistant_message = result["confirmacao"]
        except Exception as e:
            pass

    return {
        "assistant_message":assistant_message, 
        "truth_validation_type": truth_validation_type, 
        "sot_messages": (sot_messages + [response]) if enable_tools else [response], # pyright: ignore
        "sot_context": sot_context if enable_tools else None,
    }

def bot_response_action(state, config):
    print("bot_response_action")
    messages = state["messages"]

    if os.environ.get("ENABLE_TOOLS") and os.environ["ENABLE_TOOLS"] == "true":
        assistant_message = state.get("assistant_message") 
        if assistant_message:
            return {
                "messages": [AIMessage(content=assistant_message)],
                "assistant_message": None, 
                "truth_validation_type": None,
                "sot_context": None,
                "sot_messages": None,
            }

    response = assistant_agent.invoke({"messages": messages})# pyright: ignore
    return {
        "messages": [response], 
        "assistant_message": None, 
        "truth_validation_type": None,
        "sot_context": None,
        "sot_messages": None,
    }

def save_command_action(state, config):
    print("save_command_action")
    last_message = state["messages"][-1]
    result = command_vector_store.add_texts([last_message.content])
    print("\t\tsaved commands: ", result) 

def save_truth_action(state, config):
    print("save_truth_action")
    assistant_message = state["assistant_message"]
    result = truth_vector_store.add_texts([assistant_message])
    print("\t\tsaved truth: ", result) 

#this is for using tools
def source_of_truth_condiction(state, config):
    print("source_of_truth_condiction")
    if os.environ.get("ENABLE_TOOLS") and os.environ["ENABLE_TOOLS"] == "true":
        messages = state["sot_messages"]
        last_message = messages[-1]
        if isinstance(last_message, AIMessage):
            if last_message.tool_calls:
                return "tools"
        truth_validation_type = state["truth_validation_type"]
        return truth_validation_type
    else:
        truth_validation_type = state["truth_validation_type"]
        return truth_validation_type

def chat_type_condition(state, config):
    print("chat_type_condition")
    chat_type = state["chat_type"]
    return chat_type
