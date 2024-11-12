from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun, tool 
from langchain_community.utilities import WikipediaAPIWrapper
import os

from .vectorstores import truth_vector_store

@tool("search_truth_database")
def search_on_truth_database(query):
    """search for a query on the truth database"""
    # print("query: ", query)
    # docs_retriever = truth_vector_store.as_retriever()
    # docs = docs_retriever.invoke(query)
    # print("docs", docs)
    return ""


ddg_web_search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()) # pyright: ignore

source_of_truth_tools_list = None
source_of_truth_tools = None
if os.environ.get("ENABLE_TOOLS") and os.environ["ENABLE_TOOLS"] == "true":
    source_of_truth_tools_list = [wikipedia_tool, ddg_web_search_tool, search_on_truth_database]
    source_of_truth_tools = {tool.name: tool for tool in source_of_truth_tools_list}



