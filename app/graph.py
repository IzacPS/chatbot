from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from .model import State

from .node_actions import (
        #this is for using tools
        # sot_tool_node_action,
        chat_type_action,
        source_of_truth_action,
        bot_response_action,
        source_of_truth_condiction,
        chat_type_condition,
        save_command_action,
        save_truth_action,
)

def chatbot_graph(checkpointer):
    graph_builder = StateGraph(State)

    graph_builder.add_node("check_chat_type", chat_type_action)
    graph_builder.add_node("source_of_truth", source_of_truth_action)
    graph_builder.add_node("bot_response", bot_response_action)
    graph_builder.add_node("save_pref", save_command_action)
    graph_builder.add_node("save_truth", save_truth_action)

    #this is for using tools
    # graph_builder.add_node("truth_tools", sot_tool_node_action)

    graph_builder.set_entry_point("check_chat_type")

    graph_builder.add_edge("save_pref", "bot_response")
    graph_builder.add_edge("save_truth", "bot_response")

    #this is for using tools
    # graph_builder.add_edge("truth_tools", "source_of_truth")
    
    graph_builder.add_conditional_edges(
        "check_chat_type",
        chat_type_condition,
        {"imperative": "save_pref", "declarative": "source_of_truth", "other": "bot_response"}
    )

    #this is for using tools
    # graph_builder.add_conditional_edges(
    #     "source_of_truth",
    #     source_of_truth_condiction,
    #     {"tools": "truth_tools", "verdadeiro": "save_truth", "falso": "bot_response"}
    # )

    graph_builder.add_conditional_edges(
        "source_of_truth",
        source_of_truth_condiction,
        {"verdadeiro": "save_truth", "falso": "bot_response"}
    )

    graph_builder.set_finish_point("bot_response")

    return graph_builder.compile(checkpointer=checkpointer)


