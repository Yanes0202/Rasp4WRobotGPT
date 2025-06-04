from flask import Flask, request
from controls import execute_action

app = Flask(__name__)

@app.route("/move", methods=["POST"])
def move():
    direction = request.form.get("direction")
    
    if direction in ["f", "b", "l", "r"]:
        execute_action(direction)
        return f"Executed {direction}", 200
    else:
        return "Invalid command", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
