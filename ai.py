import json
import sys
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")
client = OpenAI(api_key=API_KEY)

def analyze_image(image_data):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analize what you can see on the image(e.g. books, distance to book, any useful observations). Try to locate the book 'World of Warcraft SYLWANA'. Shortly write what you can see, keep only important information",
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
        return response.choices[0].message.content

    except Exception as e:
        print("Blad podczas komunikacji z API:", e)
        sys.exit(1)


def decide_action(image_data, history, last_description):
    try:
        response = client.responses.create(
            model="o4-mini",
            reasoning={"effort":"medium"},
            input=[
                {
                    "role": "system",
                    "content": """You control a robot movement, your only goal is to find and get as close as possible to a book titled 'World of Warcraft SYLWANA'. Respond only in format:{"action": "one of the available actions", "reason": "Why you made such decision"}. Available actions: f(front), b(back), l(left approx. 45), fl(far_left approx. 90), r(right), fr(far_right), finish(only when book is clearly readable and very close).""",
                },
                {
                    "role": "user",
                    "content": f"Here is description of image one move before: {last_description}. Here is current image description: {image_data} Below is the compressed movement history. {json.dumps(history, indent=2)}. Be smart and use this context to locate the target book in the shortest way possible."
                }
            ]
        )
        raw_response = response.output[1].content[0].text
        return raw_response

    except Exception as e:
        print("Blad podczas komunikacji z API:", e)
        sys.exit(1)
    
