from langchain_core.messages import AIMessage, SystemMessage
from langgraph.graph import message
from langgraph.prebuilt.chat_agent_executor import ToolMessage
import json

from .prompts import sot_system_prompt2
from .vectorstores import truth_vector_store
from .vectorstores import command_vector_store
from .tools import source_of_truth_tools
from .agents import (
    chat_type_agent, 
    source_of_truth_agent,
    assistant_agent,
)
import json


def sot_tool_node_action(state):
    print("sot_tool_node_action")
    outputs = []
    for tool_call in state["sot_messages"][-1].tool_calls:
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
    print("source_of_truth_action")
    messages = state["messages"]
    
    #this is for the tool calling
    # sot_context = ""
    # if state.get("sot_context"):
    #     sot_context = state["sot_context"]
    # sot_messages = None
    # if not state.get("sot_messages"):
    #     content = messages[-1]
    #     sot_messages = [SystemMessage(content=sot_system_prompt2)] + [content]
    # else:
    #     sot_messages = state["sot_messages"]
    #this is for the tool calling
    # last_message = sot_messages[-1]
    # if isinstance(last_message, ToolMessage):
    #     sot_context = sot_context + str(last_message.content)

    content = messages[-1].content
    response = source_of_truth_agent.invoke({"message": content}) # pyright: ignore
    truth_validation_type = "falso" 
    assistant_message = None 

    #this is for the tool calling
    # if isinstance(response, AIMessage):

    try:
        result = json.loads(response.content) # pyright: ignore
        truth_validation_type = result["tipo"]
        assistant_message = result["confirmacao"]
    except Exception as e:
        pass

    return {
        "assistant_message":assistant_message, 
        "truth_validation_type": truth_validation_type, 

        # "sot_messages": sot_messages + [response], 
        #this is for the tool calling
        # "sot_context": sot_context
    }

def bot_response_action(state, config):
    print("bot_response_action")
    messages = state["messages"]
    assistant_message = state.get("assistant_message") 
    # if assistant_message:
    #     return {"messages": messages + [AIMessage(content=assistant_message)]}
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
    last_message = state["messages"][-1]
    assistant_message = state["assistant_message"]
    # print("assistant_message  ", assistant_message)
    result = truth_vector_store.add_texts([assistant_message])
    print("\t\tsaved truth: ", result) 

#this is for using tools
# def source_of_truth_condiction(state, config):
#     print("source_of_truth_condiction")
#     messages = state["sot_messages"]
#     last_message = messages[-1]
#     if isinstance(last_message, AIMessage):
#         if last_message.tool_calls:
#             return "tools"
#     truth_validation_type = state["truth_validation_type"]
#     return truth_validation_type

def source_of_truth_condiction(state, config):
    print("source_of_truth_condiction")
    truth_validation_type = state["truth_validation_type"]
    return truth_validation_type

def chat_type_condition(state, config):
    print("chat_type_condition")
    chat_type = state["chat_type"]
    return chat_type
