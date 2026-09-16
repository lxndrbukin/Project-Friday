from google import genai
from utils import GEMINI_API_KEY, GEMINI_MODEL
from tools.web_search import web_search, web_search_tool
from tools.current_datetime import current_datetime, current_datetime_tool
import json

function_map = {
    "web_search": web_search,
    "current_datetime": current_datetime
}

tools = [
    current_datetime_tool,
    web_search_tool
]

def get_response(prompt: str, client: genai.Client):
    if not prompt:
        return "Please enter a message"
    current_input = prompt
    previous_id = None
    safety_counter = 0
    while True:
        response = client.interactions.create(
            model=GEMINI_MODEL,
            input=current_input,
            tools=tools,
            previous_interaction_id=previous_id
        )
        function_results = []
        for step in response.steps:
            if step.type == "function_call":
                result = function_map[step.name](**step.arguments)
                print(f"➤ Called {step.name}({step.arguments})")
                function_results.append({
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [{"type": "text", "text": json.dumps(result)}],
                })
        safety_counter += 1
        if safety_counter >= 10:
            return "Too many tool calls executed"
        if function_results:
            current_input = function_results
            previous_id = response.id
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