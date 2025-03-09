#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tesztfájl a conversation_manager helyes használatának bemutatására.
Ez a példa azt mutatja, hogyan kell helyesen kezelni a posztgenerálási kéréseket
és az adatgyűjtési folyamatot az ügynökön belül.
"""

import os
import sys

# Közvetlen import a tools könyvtárból
from tools.conversation_manager import conversation_manager

def test_post_request_detection():
    """Teszteli a posztgenerálási kérések felismerését."""
    test_messages = [
        "generálj posztot",
        "szeretnék egy posztot",
        "kérlek készíts egy ingatlan hirdetést",
        "írnál egy szöveget a házról",
        "Budapest, XII. kerület"  # Ez nem poszt generálási kérés
    ]
    
    for msg in test_messages:
        print(f"\nTeszt üzenet: {msg}")
        manager = conversation_manager(
            user_message=msg,
            conversation_state={}
        )
        result = manager.run()
        
        if result.get("is_post_request"):
            print("✓ POSZT KÉRÉS ÉSZLELVE - Adatgyűjtés indul")
            print(f"  Üzenet: {result.get('message')}")
        else:
            print("✗ Nem posztgenerálási kérés")

def simulate_conversation():
    """Szimulál egy teljes beszélgetést, ahol az ágens helyesen reagál a felhasználó üzeneteire."""
    conversation_state = {}
    
    # 1. Felhasználó kér egy posztot
    print("\n=== 1. LÉPÉS: FELHASZNÁLÓ POSZTOT KÉR ===")
    manager = conversation_manager(
        user_message="Generálj egy posztot",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # 2. Felhasználó megadja a címet
    print("\n=== 2. LÉPÉS: FELHASZNÁLÓ MEGADJA A CÍMET ===")
    manager = conversation_manager(
        user_message="Budapest, XII. kerület, Normafa út",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # 3. Felhasználó megadja az árat
    print("\n=== 3. LÉPÉS: FELHASZNÁLÓ MEGADJA AZ ÁRAT ===")
    manager = conversation_manager(
        user_message="150 millió forint",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # 4. Felhasználó megadja a szobák számát
    print("\n=== 4. LÉPÉS: FELHASZNÁLÓ MEGADJA A SZOBÁK SZÁMÁT ===")
    manager = conversation_manager(
        user_message="5 szobás",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # 5. Felhasználó megadja az alapterületet
    print("\n=== 5. LÉPÉS: FELHASZNÁLÓ MEGADJA AZ ALAPTERÜLETET ===")
    manager = conversation_manager(
        user_message="220 m²",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # 6. Felhasználó megadja a jellemzőket
    print("\n=== 6. LÉPÉS: FELHASZNÁLÓ MEGADJA A JELLEMZŐKET ===")
    manager = conversation_manager(
        user_message="Úszómedence, okosotthon, panorámás kilátás a városra",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # 7. Felhasználó megadja az egyedi eladási érveket
    print("\n=== 7. LÉPÉS: FELHASZNÁLÓ MEGADJA AZ EGYEDI ELADÁSI ÉRVEKET ===")
    manager = conversation_manager(
        user_message="Nemrég felújított, egyedi építésű luxusvilla a Normafánál, közvetlen erdőkapcsolattal",
        conversation_state=conversation_state
    )
    result = manager.run()
    print(f"Ágens válasza: {result.get('message')}")
    conversation_state = result.get("updated_state")
    
    # ÖSSZEFOGLALÓ
    print("\n=== BESZÉLGETÉS ÖSSZEFOGLALÁSA ===")
    print(f"Összegyűjtött adatok: {conversation_state.get('collected_data')}")
    print(f"Hiányzó adatok: {conversation_state.get('missing_data')}")
    print(f"Jelenlegi lépés: {conversation_state.get('current_step')}")

if __name__ == "__main__":
    print("=== 1. POSZT KÉRÉS FELISMERÉS TESZT ===")
    test_post_request_detection()
    
    print("\n=== 2. TELJES BESZÉLGETÉS SZIMULÁCIÓ ===")
    simulate_conversation() 