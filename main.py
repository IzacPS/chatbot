import os

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from app.graph import chatbot_graph
import streamlit as st
import uuid


def main():
    st.title("chatbot")

    if "checkpointer" not in st.session_state:
        checkpointer = MemorySaver()
        st.session_state.checkpointer = checkpointer

    if "app" not in st.session_state:
        app = chatbot_graph(checkpointer=st.session_state.checkpointer)
        st.session_state.app = app

    if "chat_uuid" not in st.session_state:
        chat_uuid = uuid.uuid4()
        st.session_state.chat_uuid = chat_uuid

    if "config" not in st.session_state:
        config = {"configurable": {"thread_id": st.session_state.chat_uuid}}
        st.session_state.config = config 

    #inicializar historico
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)


    #reagir a entrada do usuário
    if prompt := st.chat_input("fale com o bot"):
        user_prompt = HumanMessage(content=prompt)
        #mostrar a mensagem do usuário no chat container
        with st.chat_message("user"):
            st.markdown(prompt)

        #adiciona a mensagem ao historico da conversa
        st.session_state.messages.append(user_prompt)

        with st.chat_message("assistant"):
            response = st.session_state.app.invoke({"messages": [user_prompt]}, st.session_state.config) # pyright: ignore
            message = response["messages"][-1]
            st.markdown(message.content)

            # for m in response["messages"]:
            #     print(m)
        #adiciona a mensagem do assistente ao historico da conversa 
        st.session_state.messages.append(message)

    # checkpointer = MemorySaver()
    # app = chatbot_graph(checkpointer=checkpointer)
    # chat_uuid = uuid.uuid4()
    # config = {"configurable": {"thread_id": chat_uuid}}
    #
    # print("------------------------user------------------------")
    # _input = "Donald Trump foi eleito presidente dos Estados Unidos em 2024."
    # # _input = "responda como um pirata."
    # response = app.invoke({"messages": [HumanMessage(content=_input)]}, config)# pyright: ignore
    # print("------------------------messages------------------------")
    # for m in response["messages"]:
    #     print(m)
    # print("------------------------assistant------------------------")
    # print(response["messages"][-1].content,"\n\n")

if __name__ == "__main__":
    main()




