from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from app.graph import chatbot_graph
import streamlit as st
import uuid
import time

def main():

    checkpointer = MemorySaver()
    app = chatbot_graph(checkpointer=checkpointer)

    print("------------------------user------------------------")

    frases_imperativas = {
        "Seja mais formal.":lambda x: x == "imperative",
        "Responsa como um pirata.":lambda x: x == "imperative", #falhou
        "Responsa formalmente.":lambda x: x == "imperative", #falhou
        "Finja que é o eminem.":lambda x: x == "imperative",
        "Feche a porta.":lambda x: x == "imperative",
        "Lave as mãos.":lambda x: x == "imperative",
        "Venha aqui.":lambda x: x == "imperative",
        "Escute com atenção.":lambda x: x == "imperative",
        "Compre frutas frescas.":lambda x: x == "imperative",
        "Leia o livro até o final.":lambda x: x == "imperative",
        "Ajude seus colegas.": lambda x: x == "imperative", #falhou
        "Guarde seus pertences.":lambda x: x == "imperative",
        "Vá direto ao ponto.":lambda x: x == "imperative", 
        "Faça o seu melhor.":lambda x: x == "imperative", #falhou
    }
    chat_uuid = uuid.uuid4()
    for k,v in frases_imperativas.items():
        values = [v, "imperative"]
        try: 
            config = {"configurable": {"thread_id": chat_uuid, "test": values, "enable_test": True}}
            app.invoke({"messages": [HumanMessage(content=k)]}, config)# pyright: ignore
            print("------- test passed -------")
        except Exception as e:
            print("------- test failed -------")
            print("\terror: ", e)
            print("\tvalues: ", [k, "imperative"])
            pass
        time.sleep(4)

if __name__ == "__main__":
    main()




