from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def fetch_history(conv_id: str):
    file_path = os.path.join(os.path.dirname(__file__), f"history/{conv_id}.json")
    if not conv_id or not os.path.exists(file_path):
        return "Conversation doesn't exist"
    with open(file_path, "r") as f:
        return json.load(f)

def save_history(
    conv_id: str | None = None,
    title: str | None = None,
    previous_interaction_id: str | None = None,
    messages: list = []
):
    os.makedirs("history", exist_ok=True)
    file_path = os.path.join(os.path.dirname(__file__), f"history/{conv_id}.json")
    if not conv_id or not os.path.exists(file_path):
        timestamp = datetime.now().strftime("%d-%m-%Y_%H%M%S")
        new_conv_id = f"conv_{timestamp}"
        new_file_path = os.path.join(
            os.path.dirname(__file__), 
            f"history/{new_conv_id}.json"
        )
        with open(new_file_path, "w") as f:
            data = {
                "id": new_conv_id,
                "title": title,
                "previous_interaction_id": previous_interaction_id,
                "messages": messages
            }
            json.dump(data, f, indent=4)
        return new_conv_id
    else:
        existing_data = fetch_history(conv_id)
        existing_data["messages"] = existing_data["messages"] + messages
        existing_data["previous_interaction_id"] = previous_interaction_id
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)
        return conv_id

def list_conversations():
    history_dir = os.path.join(os.path.dirname(__file__), "history")
    os.makedirs(history_dir, exist_ok=True)
    conversations = []
    for file_name in os.listdir(history_dir):
        if not file_name.endswith('.json'):
            continue
        conv_id = file_name.removesuffix('.json')
        data = fetch_history(conv_id)
        file_path = os.path.join(history_dir, file_name)
        conversations.append({
            "id": conv_id, 
            "title": data["title"],
            "modified": os.path.getmtime(file_path)
        })
    conversations.sort(key=lambda c: c["modified"], reverse=True)
    return conversations

def print_conversations(conversations):
    if not conversations:
        print("No saved conversations found.")
        return
    print("○ Past conversations:")
    for i, conv in enumerate(conversations, start=1):
        print(f"  {i}. {conv['title']}")

def get_int_input(prompt, valid_options=None):
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a number.")
            continue
        if valid_options and value not in valid_options:
            print("Please select one of the above options.")
            continue
        return value