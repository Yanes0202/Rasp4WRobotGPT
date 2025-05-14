import json
import os
import sys
import time
from openai import OpenAI
from dotenv import load_dotenv

from file_actions import load, save
from capture import get_image
from Pilot.controls import front, back, left, far_left, right, far_right

load_dotenv()

TRY = "4"

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
                    "content": """Response ALWAYS in JSON. After analyzing picture decide what robot have to do. Your goal is to find and move as close as possible to a book with title World of Warcraft SYLWANA. Available commands: "front", "left"(approx. 45 degrees), "far_left"(approx. 90 degrees), "right"(approx. 45 degrees), "far_right"(approx. 90 degrees), "back", "finish" (!only when you decide that you are very close to the book!). Example:{"description": "I see something...", "action": "left"}""",
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

def execute_action(action):
    match action:
        case "front":
            front()
        case "right":
            right()
        case "far_right":
            far_right()
        case "left":
            left()
        case "far_left":
            far_left()
        case "back":
            back()
        case _:
            print("Nieznana komenda:", action)

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
            response_cleaned = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
            response_json = json.loads(response_cleaned)

            action = response_json.get("action")
            description = response_json.get("description", "")

            print("Opis:", description)
            print("Dzialanie:", action)


            if action == 'finish':
                print("Znaleziono ksiazke")
                history_session["found"] = True
                result_session["found"] = True
                result_session["steps"] = i + 1
                break
                
            history_session["actions"].append(action)
            result_session["actions"].append(action)
            result_session["responsess"].append(description)
            
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
