from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq

from .model import ImperativePhraseClassification

# sot_system_prompt,
from .tools import source_of_truth_tools_list
from .prompts import (
    chat_type_system_prompt,
    #this is for using tools
    # sot_system_prompt,
    sot_system_prompt2,
    assistant_prompt,
)

chat_type_llm = ChatGroq(model="llama3-70b-8192", temperature=0.0) # pyright: ignore
sot_llm = ChatGroq(model="llama3-70b-8192", temperature=0.0) # pyright: ignore
llm_assistant = ChatGroq(model="llama3-8b-8192") # pyright: ignore

def create_agent(
        llm, 
        prompt_template = None,
        structure_type = None,
        tools = None,
):
    if tools:
        llm = llm.bind_tools(tools)

    if structure_type:
        llm = llm.with_structured_output(structure_type)

    if prompt_template: 
        return prompt_template | llm 

    return llm

################ chat type agent 
chat_type_system_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", chat_type_system_prompt),
        ("human", "{message}"),
    ]
)  

chat_type_agent = create_agent(llm=chat_type_llm, 
                               prompt_template=chat_type_system_prompt_template,
                               structure_type=ImperativePhraseClassification,
                               )

################ source of truth agent 
sot_system_prompt_template = ChatPromptTemplate.from_messages(
    [
        #this is for using tools
        # ("system", sot_system_prompt),
        ("system", sot_system_prompt2),
        ("human", "{message}"),
    ]
)  
source_of_truth_agent = create_agent(llm=sot_llm,
                                     prompt_template=sot_system_prompt_template, 
                                     #this is for using tools
                                     # tools=source_of_truth_tools_list,
                                     )

################ assistant agent 
assistant_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",assistant_prompt,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)  

assistant_agent = create_agent(llm=llm_assistant,
                                    prompt_template=assistant_prompt_template)

