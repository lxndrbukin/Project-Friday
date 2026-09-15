from google import genai
from utils import GEMINI_API_KEY, GEMINI_MODEL
from tools.web_search import web_search, web_search_tool
import json

function_map = {
    "web_search": web_search
}

def get_response(prompt: str, client: genai.Client):
    if not prompt:
        return "Please enter a message"
    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
        tools=[web_search_tool]
    )
    function_results = []
    for step in response.steps:
        if step.type == "function_call":
            result = function_map[step.name](**step.arguments)
            print(f"Called {step.name}({step.arguments})")
            function_results.append({
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            })
    if function_results:
        final_response = client.interactions.create(
            model=GEMINI_MODEL,
            input=function_results,
            tools=[web_search_tool],
            previous_interaction_id=response.id
        )
        return final_response.output_text
    else:
        return response.output_text

def main():
    client = genai.Client(api_key=GEMINI_API_KEY)
    while True:
        prompt = input('○ You:\n')
        if prompt.lower() in ['q', 'exit', 'quit']:
            break
        response = get_response(prompt, client)
        print(f"● Friday:\n{response}")

if __name__ == '__main__':
    main()