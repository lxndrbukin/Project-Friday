from tavily import TavilyClient
from utils import TAVILY_API_KEY

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

web_search_tool = {
    "type": "function",
    "name": "web_search",
    "description": "Search the web. Present results as a formatted markdown list with each result on its own line, separated by blank lines.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Query provided by the user for the search"
            }
        },
        "required": ["query"]
    }
}

def web_search(query: str, max_results: int = 3):
    try:
        output = ""
        response = tavily_client.search(query, max_results=max_results)
        if not len(response["results"]):
            return "No search results found"
        for idx, result in enumerate(response["results"]):
            output += f'**{idx + 1}. [{result["title"]}]({result["url"]})**\n\n'
            output += f'{result["content"][:200]}\n\n'
        return output
    except Exception as e:
        return f"Error: {e}"