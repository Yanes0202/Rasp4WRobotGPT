import json
import os
import sys
import time
from openai import OpenAI
from dotenv import load_dotenv

from file_actions import load, save
from capture import get_image
from Pilot.controls import execute_action

load_dotenv()

TRY = "6"

HISTORY_FILE = "results/history" + TRY + ".json"
RESULTS_FILE = "results/results" + TRY + ".json"

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

if __name__ == "__main__":
    start_time = time.time()
    full_history = load(HISTORY_FILE)
    full_result = load(RESULTS_FILE)
    history_session = {"actions": [], "found": False}
    result_session = {"actions":[], "responsess": [], "steps": 1, "time": "", "found": False}

    i = 0
    for i in range(20):
        print(f"Iteracja {i + 1}/20")

        image = get_image(TRY)

        current_history = full_history.copy()
        current_history.append(history_session)
        response = analyze_image(image, current_history)
        try:
            print(response)
            response_cleaned = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
            response_json = json.loads(response_cleaned)

            action = response_json.get("action")
            description = response_json.get("description", "")

            print("Opis:", description)
            print("Dzialanie:", action)
                
            history_session["actions"].append(action)
            result_session["actions"].append(action)
            result_session["responsess"].append(description)
            
            if action == 'finish':
                print("Znaleziono ksiazke")
                history_session["found"] = True
                result_session["found"] = True
                break
            
            execute_action(action)

        except json.JSONDecodeError as e:
            print("Blad dekodowania odpowiedzi JSON:", e)
            break

    full_history.append(history_session)
    save(HISTORY_FILE, full_history)

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)
    result_session["time"] = f"{elapsed}s"
    result_session["steps"] = i + 1
    full_result.append(result_session)
    save(RESULTS_FILE, full_result)
    print("Zapisano historie oraz wyniki")
