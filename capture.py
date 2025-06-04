import subprocess
import base64
import sys
import os

def take_picture(try_number):
    folder = f"img/try{try_number}"
    os.makedirs(folder, exist_ok=True)

    i = 1
    while os.path.exists(f"{folder}/research{i}.jpeg"):
        i += 1

    image_path = f"{folder}/research{i}.jpeg"


    try:
        subprocess.run([
            "libcamera-still",
            "-t", "1",
            "-n",
            "--autofocus-mode", "manual",
            "--awb", "indoor",
            "-o", image_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return image_path

    except subprocess.CalledProcessError as e:
        sys.exit(1)

def get_image(try_number):
    image_path = take_picture(try_number)
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
