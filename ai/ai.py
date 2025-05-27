from openai import OpenAI
import json
import os
from tools.loaders import loadNurses, loadPatients
from interfaces.interface import match_nurses_patients 
from dotenv import load_dotenv

load_dotenv()
key =  os.environ.get("OPEN_AI_API_KEY")

client = OpenAI(api_key=key)
def chat_loop():
    print("Welcome to the Nurse-Patient Matching Assistant (CLI)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        if user_input.lower().startswith("run match"):
            nurse_path = input("Enter nurse file path: ").strip()
            patient_path = input("Enter patient file path: ").strip()
            print(f"Checking files:\n  Nurse path: '{nurse_path}'\n  Patient path: '{patient_path}'")
            print("File exists:", os.path.exists(nurse_path), os.path.exists(patient_path))
            if not os.path.exists(nurse_path) or not os.path.exists(patient_path):
                print("One or both files not found.")
                continue

            print("📊 Running matching algorithm...")
            nurses = loadNurses(nurse_path)
            patients = loadPatients(patient_path)
            result_path = match_nurses_patients(nurses, patients)
            
            print(f"Matching complete! Result saved to {result_path}")
            continue

        # Assistant API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        print(f"Assistant: {response.choices[0].message.content}\n")

if __name__ == "__main__":
    chat_loop()