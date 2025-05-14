import json
import sys
import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

def analyze_image(image_data, history):
    API_KEY = os.getenv("GPT_API_KEY")
    client = OpenAI(api_key=API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Respond ONLY in JSON format:{"description": "What you see (e.g. books, distance to book, any useful observations)", "action": "one of the available actions"}. You control a robot that must find and get as close as possible to a book titled 'World of Warcraft SYLWANA'. Your ONLY goal is to LOCATE and MOVE AS CLOSE AS POSSIBLE to this specific book. Use 'finish' ONLY if the book is clearly readable and VERY close. Available commands: "front", "back", "left", "far_left", "right", "far_right", "finish". You have 20 steps per session. Use them strategically.""",
                },
                {
                    "role": "user",
                    "content": f"Below is the full movement history. Use this context to avoid repeating inefficient paths and to locate the target book more effectively. {json.dumps(history, indent=2)}"
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
