import json
import sys
import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

def analyze_image(image_data, history, last_description):
    API_KEY = os.getenv("GPT_API_KEY")
    client = OpenAI(api_key=API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """Respond ONLY in JSON format:{"description": "What you see(e.g. books, distance to book, any useful observations)", "action": "one of the available actions"}. Use ONLY this commands: "f"(front), "b"(back), "l"(left approx. 45), "fl"(far_left approx. 90), "r"(right), "fr"(far_right), "finish". You control a robot, your only goal is to look around to FIND and GET AS CLOSE AS POSSIBLE to a book titled 'World of Warcraft SYLWANA'. Use 'finish' ONLY if the book is clearly readable and VERY close.""",
                },
                {
                    "role": "user",
                    "content": f"Here is description of image one move before: {last_description}. Below is the compressed movement history. {json.dumps(history, indent=2)}. Be smart and use this context to locate the target book in the shortest way possible."
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
