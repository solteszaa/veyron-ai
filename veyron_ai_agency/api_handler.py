import os
import sys
import json
from dotenv import load_dotenv
from agency_swarm import set_openai_key

# Környezeti változók betöltése
load_dotenv()

# OpenAI API kulcs beállítása
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Az OPENAI_API_KEY környezeti változó nincs beállítva!")

# API kulcs beállítása az Agency Swarm számára
set_openai_key(openai_api_key)

# UTF-8 kódolás beállítása
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

# Agent osztály patchelése UTF-8 támogatáshoz
import patch_agent

# Az ügynökség importálása csak az API kulcs beállítása után
from agency import agency

# Ideiglenes fájlok útvonalai
USER_MESSAGE_FILE = "temp_user_message.txt"
ASSISTANT_RESPONSE_FILE = "temp_assistant_response.txt"

def read_user_message():
    """Felhasználói üzenet olvasása a fájlból"""
    try:
        with open(USER_MESSAGE_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Hiba a felhasználói üzenet olvasása közben: {str(e)}")
        return None

def write_assistant_response(response):
    """Asszisztens válaszának írása a fájlba"""
    try:
        with open(ASSISTANT_RESPONSE_FILE, "w", encoding="utf-8") as file:
            file.write(response)
    except Exception as e:
        print(f"Hiba az asszisztens válaszának írása közben: {str(e)}")

class WebResponseCapturer:
    """Osztály a válasz elfogására és fájlba írására"""
    def __init__(self):
        self.response_text = ""
    
    def __call__(self, text):
        self.response_text += text
        return True

def main():
    # Felhasználói üzenet olvasása
    user_message = read_user_message()
    if not user_message:
        write_assistant_response("Nem sikerült olvasni a felhasználói üzenetet.")
        return
    
    # Válasz elfogó inicializálása
    response_capturer = WebResponseCapturer()
    
    try:
        # Agency futtatása a felhasználói üzenettel
        # Az agency.step metódus a választ a response_capturer-be írja
        agency.step(user_message, callback=response_capturer)
        
        # Válasz írása a fájlba
        write_assistant_response(response_capturer.response_text)
    except Exception as e:
        error_message = f"Hiba történt az AI feldolgozása közben: {str(e)}"
        print(error_message)
        write_assistant_response(error_message)

if __name__ == "__main__":
    main() 