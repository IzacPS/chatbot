
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

    frases_interacao_chat = {
        "É verdade que a população mundial já passou de 9 bilhões de pessoas?": lambda x: x == "other",
        "Será que já encontraram água líquida na superfície de Marte?": lambda x: x == "other",
        "A vacina X foi aprovada por todos os órgãos regulatórios?": lambda x: x == "other",
        "O Sol realmente gira em torno da Terra?": lambda x: x == "other",
        "A baleia azul é o maior animal que já existiu na Terra?": lambda x: x == "other",
        "É verdade que inventaram um plástico que se decompõe completamente em pouco tempo?": lambda x: x == "other",
        "O gelo nos polos está aumentando a cada ano?": lambda x: x == "other",
        "Chocolate é perigoso para todos os animais?": lambda x: x == "other"
    }
    chat_uuid = uuid.uuid4()
    for k,v in frases_interacao_chat.items():
        values = [v, "other"]
        try: 
            config = {"configurable": {"thread_id": chat_uuid, "test": values, "enable_test": True}}
            app.invoke({"messages": [HumanMessage(content=k)]}, config)# pyright: ignore
        except Exception as e:
            print("error: ", e)
            print("\tvalues: ", [k, "other"])
            pass
        time.sleep(4)


    # print("------------------------messages------------------------")
    # for m in response["messages"]:
    #     print(m)
    # print("------------------------assistant------------------------")
    # print(response["messages"][-1].content,"\n\n")


if __name__ == "__main__":
    main()




