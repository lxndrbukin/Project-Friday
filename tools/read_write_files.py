import os

write_file_tool = {
    "type": "function",
    "name": "write_file",
    "description": "Write data to a new or existing file",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Set the file name to write the data to."
            },
            "content": {
                "type": "string",
                "description": "Content to add to the new or existing file."
            },
            "append": {
                "type": "boolean",
                "description": "Check if the data needs to be appended to a file."
            }
        },
        "required": ["file_name", "content"]
    }
}

read_file_tool = {
    "type": "function",
    "name": "read_file",
    "description": "Read data from an existing file",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "File name to read data from."
            }
        },
        "required": ["file_name"]
    }
}

BASE_DIR = "friday_files"

def write_file(
        file_name: str,
        content: str, 
        append: bool = False
    ):
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        file_name = os.path.basename(file_name)
        path = os.path.join(BASE_DIR, file_name)
        file_exists = os.path.isfile(path)
        if append:
            check = input("● Friday:\nDo you wish to append content to the file?\n")
            if check.lower() not in ["y", "yes"]:
                return "Action aborted"
            with open(path, "a") as f:
                f.write(content)
        else:
            if file_exists:
                check = input("● Friday:\nDo you wish to overwrite the file?\n")
            else:
                check = input("● Friday:\nDo you wish to create a new file?\n")
            if check.lower() not in ["y", "yes"]:
                    return "Action aborted"
            with open(path, "w") as f:
                f.write(content)
    except Exception as e:
        return f"Error: {e}"

def read_file(
        file_name: str
    ):
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        file_name = os.path.basename(file_name)
        path = os.path.join(BASE_DIR, file_name)
        file_exists = os.path.isfile(path)
        if file_exists:
            with open(path, "r") as f:
                return f.read()
        else:
            return "File doesn't exist"
    except Exception as e:
        return f"Error: {e}"