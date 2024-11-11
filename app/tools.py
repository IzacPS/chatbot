from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun 
from langchain_community.utilities import WikipediaAPIWrapper

ddg_web_search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()) # pyright: ignore
source_of_truth_tools_list = [wikipedia_tool, ddg_web_search_tool]
source_of_truth_tools = {tool.name: tool for tool in source_of_truth_tools_list}

