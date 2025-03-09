import os
import sys
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

if __name__ == "__main__":
    print("Veyron Hungary AI Ingatlan Marketing Asszisztens indítása...")
    print("A rendszer készen áll a használatra. Írjon üzenetet a kezdéshez!")
    
    # Ügynökség indítása terminál demo módban
    # Belső üzenetek és részletek elrejtése, csak a végső kimenetet mutatjuk
    agency.run_demo() 