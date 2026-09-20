from google import genai
from utils import (
    GEMINI_API_KEY, 
    GEMINI_MODEL,
    save_history, 
    fetch_history, 
    list_conversations,
    print_conversations,
    get_int_input
)
from tools.web_search import web_search, web_search_tool
from tools.current_datetime import current_datetime, current_datetime_tool
from tools.read_write_files import (
    read_file,
    write_file,
    read_file_tool,
    write_file_tool
)
import json

function_map = {
    "web_search": web_search,
    "current_datetime": current_datetime,
    "read_file": read_file,
    "write_file": write_file
}

tools = [
    current_datetime_tool,
    web_search_tool,
    read_file_tool,
    write_file_tool
]

def get_response(
    client: genai.Client, 
    prompt: str, 
    conv_id: str = None,
    previous_id: str = None
):
    if not prompt:
        return conv_id, "Please enter a message"
    current_input = prompt
    safety_counter = 0
    title = None
    if conv_id:
        data = fetch_history(conv_id)
        title = data["title"]
        if not previous_id:
            previous_id = data["previous_interaction_id"]
    else:
        title_response = client.interactions.create(
            model=GEMINI_MODEL,
            input=f"Summarize this in a short title (a few words): {prompt}"
        )
        title = title_response.output_text
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
            return conv_id, "Too many tool calls executed"
        if function_results:
            current_input = function_results
            previous_id = response.id
        else:
            conv_id = save_history(
                conv_id=conv_id,
                title=title,
                previous_interaction_id=response.id,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    },
                    {
                        "role": "assistant",
                        "content": response.output_text
                    }
                ]
            )
            return conv_id, response.output_text

def main():
    client = genai.Client(api_key=GEMINI_API_KEY)
    conv_id = None
    action = get_int_input(
        "Hello, I'm Friday, your friendly AI assistant!\n Please select an action:\n1. Start new chat\n2. Continue existing chat\n3. Exit\n",
        valid_options=[1,2,3]    
    )
    if action == 2:
        conversations = list_conversations()
        if not conversations:
            print("● Friday:\nCurrently no existing conversations.\nStarting a new chat...")
        else:
            print_conversations(conversations)
            choice = get_int_input(
                "Select chat number:\n", 
                valid_options=list(range(1, len(conversations) + 1))
            )
            conv_id = conversations[choice-1]["id"]
            data = fetch_history(conv_id)
            for message in data["messages"]:
                print(f"{'○ You' if message['role'] == 'user' else '● Friday'}:\n{message['content']}")
    elif action == 3:
        return
    while True:
        prompt = input("○ You:\n")
        if prompt.lower() in ["q", "exit", "quit"]:
            break
        conv_id, response = get_response(client, prompt, conv_id)
        print(f"● Friday:\n{response}")

if __name__ == "__main__":
    main()