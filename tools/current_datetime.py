from datetime import datetime, date

current_datetime_tool = {
    "type": "function",
    "name": "current_datetime",
    "description": "Get the current date and time, e.g. format: DD/MM/YYYY HH:MM:SS.",
    "parameters": {
        "type": "object",
        "properties": {
            "current_date": {
                "type": "boolean",
                "description": "Set to true to retrieve only the current date."
            },
            "current_time": {
                "type": "boolean",
                "description": "Set to true to retrieve only the current time."
            }
        },
        "required": []
    }
}

def current_datetime(
        current_date: bool = None,
        current_time: bool = None
    ):
    if current_date:
        now = date.today().strftime("%d/%m/%Y")
    elif current_time:
        now = datetime.now().strftime("%H:%M:%S")
    else:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f"The current date and time: {now}"