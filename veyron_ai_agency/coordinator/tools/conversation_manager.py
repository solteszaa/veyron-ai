from agency_swarm.tools import BaseTool
from pydantic import Field
import json
import re

class conversation_manager(BaseTool):
    """
    Eszköz a felhasználóval folytatott beszélgetés kezelésére és a folyamat állapotának követésére.
    Nyomon követi, hogy mely adatokat gyűjtöttük már be és mi hiányzik még.
    """
    user_message: str = Field(
        ..., description="A felhasználó legutóbbi üzenete"
    )
    conversation_state: dict = Field(
        {}, description="A beszélgetés jelenlegi állapota"
    )

    def run(self):
        """
        Feldolgozza a felhasználó üzenetét és frissíti a beszélgetés állapotát.
        """
        # AZONNALI ELLENŐRZÉS - Ha a felhasználó posztot kér, azonnal kezeljük
        # Poszt generálási kérés felismerése - kibővített minta lista
        is_post_request = self._is_post_generation_request(self.user_message)
        if is_post_request:
            # KRITIKUS: Azonnal jelezzük, hogy adatgyűjtést kell indítani
            print("POSZT KÉRÉS ÉSZLELVE - Adatgyűjtés indul")
            return {
                "is_post_request": True,
                "must_collect_data": True,  # Ezt a jelzést figyeli a Coordinator
                "action": "start_data_collection",
                "message": "Szívesen segítek egy ingatlan poszt létrehozásában! Ehhez szükségem lesz néhány fontos információra az ingatlanról.\n\nElőször kérem, adja meg az ingatlan címét (város, kerület/környék):",
                "updated_state": {
                    "collected_data": {},
                    "missing_data": ["address", "price", "rooms", "size", "features", "selling_points"],
                    "images": [],
                    "current_step": "data_collection",
                    "next_question": "address"
                }
            }
        
        # Ha nincs még állapot, inicializáljuk
        if not self.conversation_state:
            self.conversation_state = {
                "collected_data": {},
                "missing_data": ["address", "price", "rooms", "size", "features", "selling_points"],
                "images": [],
                "current_step": "data_collection",
                "next_question": "address"
            }
        
        # Állapot másolása, hogy ne módosítsuk közvetlenül a bemeneti paramétert
        state = self.conversation_state.copy()
        collected_data = state.get("collected_data", {}).copy()
        missing_data = state.get("missing_data", []).copy()
        current_step = state.get("current_step", "data_collection")
        
        # Felhasználói üzenet feldolgozása az aktuális lépés alapján
        if current_step == "data_collection":
            # Következő kérdés meghatározása
            next_question = state.get("next_question")
            
            # Ha van következő kérdés, és a felhasználó válaszolt rá
            if next_question and self.user_message:
                # Adat mentése
                collected_data[next_question] = self.user_message
                
                # Eltávolítás a hiányzó adatok listájából
                if next_question in missing_data:
                    missing_data.remove(next_question)
                
                # Következő kérdés meghatározása
                if missing_data:
                    next_question = missing_data[0]
                    
                    # Felhasználóbarát kérdés megfogalmazása a következő adatra
                    next_question_text = ""
                    if next_question == "price":
                        next_question_text = "Kérem, adja meg az ingatlan árát:"
                    elif next_question == "rooms":
                        next_question_text = "Hány szobás az ingatlan?"
                    elif next_question == "size":
                        next_question_text = "Mekkora az ingatlan alapterülete (m²)?"
                    elif next_question == "features":
                        next_question_text = "Milyen különleges jellemzői vannak az ingatlannak? (pl. medence, panoráma, okosotthon-funkciók)"
                    elif next_question == "selling_points":
                        next_question_text = "Mi az ingatlan legfőbb egyedi eladási érve, ami kiemelkedővé teszi?"
                    
                    # Frissített állapot visszaadása a következő kérdéssel
                    return {
                        "action": "continue_data_collection",
                        "message": next_question_text,
                        "updated_state": {
                            "collected_data": collected_data,
                            "missing_data": missing_data,
                            "images": state.get("images", []),
                            "current_step": "data_collection",
                            "next_question": next_question
                        }
                    }
                else:
                    # Ha minden adat megvan, lépjünk tovább a képfeltöltésre
                    current_step = "image_upload"
                    next_question = None
                    return {
                        "action": "data_collection_complete",
                        "message": "Köszönöm az információkat! Most feltölthet képeket az ingatlanról. Ha elkészült, kérem írja: 'kész'.",
                        "updated_state": {
                            "collected_data": collected_data,
                            "missing_data": missing_data,
                            "images": state.get("images", []),
                            "current_step": "image_upload",
                            "next_question": next_question
                        }
                    }
            
        elif current_step == "image_upload":
            # Itt csak nyomon követjük, hogy a felhasználó feltöltött-e képeket
            # A tényleges képfeltöltést más eszköz végzi
            
            # Ha a felhasználó jelezte, hogy befejezte a képfeltöltést
            if "kész" in self.user_message.lower() or "befejeztem" in self.user_message.lower():
                current_step = "post_generation"
        
        elif current_step == "post_generation":
            # Itt várjuk a felhasználó visszajelzését a generált posztra
            
            # Ha a felhasználó elfogadta a posztot
            if any(word in self.user_message.lower() for word in ["elfogadom", "jó", "rendben", "küldés"]):
                current_step = "post_sending"
            
            # Ha a felhasználó módosítást kér
            elif any(word in self.user_message.lower() for word in ["módosítás", "változtatás", "nem jó"]):
                # Maradunk a post_generation lépésnél, de jelezzük a módosítási kérést
                state["modification_requested"] = True
        
        elif current_step == "post_sending":
            # A poszt elküldése után lezárjuk a folyamatot
            current_step = "completed"
        
        # Frissített állapot összeállítása
        updated_state = {
            "collected_data": collected_data,
            "missing_data": missing_data,
            "images": state.get("images", []),
            "current_step": current_step,
            "next_question": next_question
        }
        
        # Egyéb állapotinformációk megőrzése
        for key, value in state.items():
            if key not in updated_state:
                updated_state[key] = value
        
        return {
            "message": self.user_message,
            "updated_state": updated_state
        }
    
    def _is_post_generation_request(self, message):
        """
        Ellenőrzi, hogy a felhasználó üzenete tartalmaz-e poszt generálási kérést.
        Ez a kulcsfontosságú függvény - ha észlel kérést, akkor adatgyűjtést kell indítani.
        """
        message_lower = message.lower()
        
        # 1. Közvetlen poszt generálási kérések
        direct_patterns = [
            "generálj", "generálnál", "készíts", "készítenél", "írj", "írnál",
            "csinálj", "csinálnál", "kérek", "szeretnék", "kellene"
        ]
        
        # 2. Ingatlan/poszt kombináció
        object_patterns = [
            "poszt", "posztot", "post", "bejegyzés", "hirdetés", "reklám",
            "szöveg", "szöveget", "tartalmat", "hirdetést", "reklámot"
        ]
        
        # 3. Közvetlen egyértelmű kérések
        if any(pattern in message_lower for pattern in ["generálj posztot", "kérek egy posztot", "készíts egy posztot"]):
            return True
        
        # 4. Ha tartalmaz egy direkt és egy tárgy mintát
        if any(dp in message_lower for dp in direct_patterns) and any(op in message_lower for op in object_patterns):
            return True
        
        # 5. Egyéb gyakori kombinációk
        if "ingatlan" in message_lower and any(op in message_lower for op in object_patterns):
            return True
        
        if "ház" in message_lower and any(op in message_lower for op in object_patterns):
            return True
            
        if "lakás" in message_lower and any(op in message_lower for op in object_patterns):
            return True
        
        # A minta nem egyezik
        return False

if __name__ == "__main__":
    # Teszteljük az eszközt egy kezdeti állapottal
    initial_state = {
        "collected_data": {},
        "missing_data": ["address", "price", "rooms", "size", "features", "selling_points"],
        "images": [],
        "current_step": "data_collection",
        "next_question": "address"
    }
    
    # Poszt generálási kérés teszt
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
            print("POSZT KÉRÉS ÉSZLELVE - Adatgyűjtés indul")
        else:
            print("Nem posztgenerálási kérés") 