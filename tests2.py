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
    frases_noticias = {
        "A água ferve a 100°C ao nível do mar.": lambda x: x == "declarative",
        "O Sol é uma estrela localizada no centro do nosso sistema solar.": lambda x: x == "declarative",
        "A Terra tem aproximadamente 71% de sua superfície coberta por água.": lambda x: x == "declarative",
        "As plantas realizam fotossíntese para produzir seu alimento.": lambda x: x == "declarative",
        "A gravidade faz com que os objetos caem em direção ao centro da Terra.": lambda x: x == "declarative",
        "O ser humano possui 46 cromossomos no total.": lambda x: x == "declarative",
        "A luz viaja a aproximadamente 300.000 km por segundo no vácuo.": lambda x: x == "declarative",
        "Os morcegos são os únicos mamíferos capazes de voar.": lambda x: x == "declarative",
        "O oxigênio é essencial para a respiração dos seres humanos.": lambda x: x == "declarative",
        "As abelhas desempenham um papel crucial na polinização das plantas.": lambda x: x == "declarative"
    }
    chat_uuid = uuid.uuid4()
    for k,v in frases_noticias.items():
        values = [v, "declarative"]
        try: 
            config = {"configurable": {"thread_id": chat_uuid, "test": values, "enable_test": True}}
            app.invoke({"messages": [HumanMessage(content=k)]}, config)# pyright: ignore
        except Exception as e:
            print("error: ", e)
            print("\tvalues: ", [k, "declarative"])
            pass
        time.sleep(4)

if __name__ == "__main__":
    main()




