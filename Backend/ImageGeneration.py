import asyncio
import base64
import io
import os
from random import randint
from time import sleep
from PIL import Image
import requests
from dotenv import get_key
from huggingface_hub import InferenceClient


# Setup
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
HuggingFaceAPIKey = "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"
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}
DATA_DIR = "Data"
os.makedirs(DATA_DIR, exist_ok=True)


def open_images(prompt):
    prompt_clean = prompt.replace(" ", "_")
    files = [f"{prompt_clean}{i}.jpg" for i in range(1, 5)]

    for file_name in files:
        path = os.path.join(DATA_DIR, file_name)
        try:
            img = Image.open(path)
            print(f"Opening image: {path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {path}")


async def query(prompt, seed):
    payload = {
        "inputs": f"{prompt}, quality=4K, ultra-detailed, high resolution, seed={seed}"
    }
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.content
    else:
        print(f"API Error {response.status_code}: {response.text}")
        return None


async def generate_images(prompt: str):
    prompt_clean = prompt.replace(" ", "_")
    tasks = [asyncio.create_task(query(prompt, randint(0, 1000000))) for _ in range(1)]
    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        file_path = os.path.join(DATA_DIR, f"{prompt_clean}{i + 1}.jpg")
        if image_bytes:
            try:
                img = Image.open(io.BytesIO(image_bytes))
                img.save(file_path)
                print(f"Saved image: {file_path}")
            except Exception as e:
                print(f"Invalid image data for {file_path}: {e}")
        else:
            print(f"No image data received for {file_path}")


def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)


# Main listener loop
while True:
    try:
        with open("Frontend/Files/ImageGeneration.data", "r") as f:
            data = f.read().strip()

        Prompt, Status = data.split(",")

        if Status == "True":
            print("Generating Images ...")
            GenerateImages(prompt=Prompt)

            with open("Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
