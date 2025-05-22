import json
import time

from file_actions import load, save
from capture import get_image
from Pilot.controls import execute_action
from ai import analyze_image
from compression import compress

TRY = "8"
HISTORY_FILE = "results/history" + TRY + ".json"
RESULTS_FILE = "results/results" + TRY + ".json"

LAST_DESCRIPTION = ""

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
        response = analyze_image(image, current_history, LAST_DESCRIPTION)
        try:
            print(response)
            response_cleaned = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
            response_json = json.loads(response_cleaned)

            action = response_json.get("action")
            description = response_json.get("description", "")
            LAST_DESCRIPTION = description
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
