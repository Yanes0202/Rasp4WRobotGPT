from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/move", methods=["POST"])
def move():
    direction = request.form.get("direction")
    
    if direction in ["front", "back", "left", "right"]:
        subprocess.run(["python3", f"{direction}.py"])
        return f"Executed {direction}", 200
    else:
        return "Invalid command", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
