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
        "Fale mais rápido.": lambda x: x == "preference",
        "Seja mais simples.": lambda x: x == "preference",
        "Responda com uma frase.": lambda x: x == "preference",
        "Use menos palavras.": lambda x: x == "preference",
        "Evite detalhes.": lambda x: x == "preference",
        "Seja mais curto.": lambda x: x == "preference",
        "Não explique demais.": lambda x: x == "preference",
        "Ignore as explicações.": lambda x: x == "preference",
        "Responda com humor.": lambda x: x == "preference",
        "Use um exemplo.": lambda x: x == "preference",
        "Mude o tom.": lambda x: x == "preference",
        "Seja mais direto.": lambda x: x == "preference",
        "Fale como um especialista.": lambda x: x == "preference",
        "Diga em uma palavra.": lambda x: x == "preference",
        "Adicione um gráfico.": lambda x: x == "preference",
        "Fale de forma leve.": lambda x: x == "preference",
        "Foque no básico.": lambda x: x == "preference",
        "Responda com clareza.": lambda x: x == "preference",
        "Explique com analogias.": lambda x: x == "preference"
    }

    test_size = len(frases_imperativas)
    tests_passed = 0

    chat_uuid = uuid.uuid4()
    for k,v in frases_imperativas.items():
        values = [v, "preference"]
        try: 
            config = {"configurable": {"thread_id": chat_uuid, "test": values, "enable_test": True}}
            app.invoke({"messages": [HumanMessage(content=k)]}, config)# pyright: ignore
            print("------- test passed -------")
            tests_passed = tests_passed + 1
        except Exception as e:
            print("------- test failed -------")
            print("\terror: ", e)
            print("\tvalues: ", [k, "preference"])
            pass
        time.sleep(10)

    print(f"tests passed: {tests_passed} de {test_size}")

if __name__ == "__main__":
    main()




