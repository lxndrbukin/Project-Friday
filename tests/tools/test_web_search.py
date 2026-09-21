from unittest.mock import patch
from tools.web_search import web_search

@patch("tools.web_search.tavily_client")
def test_web_search(mock_client):
    mock_client.search.return_value = {
        "results": [
            {"title": "Example", "url": "https://example.com", "content": "Some content here"}
        ]
    }
    result = web_search("test query")
    assert "Example" in result

@patch("tools.web_search.tavily_client")
def test_web_search_no_results(mock_client):
    mock_client.search.return_value = {"results": []}
    result = web_search("test query")
    assert result == "No search results found"