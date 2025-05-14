import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import subprocess

from capture import get_image
from Pilot.controls import front, back, left, right

load_dotenv()

def analyze_image(image_data):
    API_KEY = os.getenv("GPT_API_KEY")

    client = OpenAI(api_key=API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[ 
                {
                    "role": "system",
                    "content": """Response ALWAYS in JSON. After analyzing picture decide what robot have to do. Your goal is to find and come close to a book with title World of Warcraft SYLWANA. Available commands: "front", "left", "right", "back".
Example:
{"description": "I see something...", "action": "left"}""",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=200,
        )
        raw_response = response.choices[0].message.content
        return raw_response

    except Exception as e:
        print("Blad podczas komunikacji z API:", e)
        sys.exit(1)

def execute_action(action):
    if action == "right":
        right()
    elif action == "left":
        left()
    elif action == "front":
        front()
    elif action == "back":
        back()
    else:
        print("Nieznana komenda:", action)

if __name__ == "__main__":
    
    right()
