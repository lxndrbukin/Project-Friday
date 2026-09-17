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
            json.dump(data, f)
        return new_conv_id
    else:
        existing_data = fetch_history(conv_id)
        existing_data["messages"] = existing_data["messages"] + messages
        existing_data["previous_interaction_id"] = previous_interaction_id
        with open(file_path, "w") as f:
            json.dump(existing_data, f)
        return conv_id