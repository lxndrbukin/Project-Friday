from google import genai
from utils import GEMINI_API_KEY, GEMINI_MODEL

def get_response(prompt: str, client: genai.Client):
    if not prompt:
        return "Please enter a message"
    response = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt
    )
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