import json
import os

def load(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

def save(file_name, history):
    with open(file_name, "w") as f:
        json.dump(history, f, indent=4)
