from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()  # környezeti változók betöltése

# Webhook URL a környezeti változóból
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://hook.eu2.make.com/e7v3t475ch1urzohmthysi2hf3005tx7")

class webhook_sender(BaseTool):
    """
    Eszköz a generált social media poszt és kapcsolódó adatok küldésére a Webhookra.
    """
    post_content: str = Field(
        ..., description="A generált social media poszt szövege"
    )
    property_data: dict = Field(
        ..., description="Az ingatlan adatait tartalmazó szótár"
    )
    image_urls: list = Field(
        [], description="A feltöltött képek URL-jeinek listája"
    )
    additional_data: dict = Field(
        {}, description="További adatok, amelyeket a webhookra kell küldeni"
    )

    def run(self):
        """
        Elküldi a posztot és a kapcsolódó adatokat a webhookra.
        """
        try:
            # Webhook URL ellenőrzése
            if not WEBHOOK_URL:
                return {
                    "success": False,
                    "error": "A WEBHOOK_URL környezeti változó nincs beállítva"
                }
            
            # Előkészítjük a küldendő adatokat
            payload = {
                "post_content": self.post_content,
                "property_data": self.property_data,
                "image_urls": self.image_urls,
                "timestamp": int(time.time()),
                "source": "Veyron Hungary AI Assistant"
            }
            
            # Hozzáadjuk a további adatokat, ha vannak
            if self.additional_data:
                payload.update(self.additional_data)
            
            # Elküldjük a POST kérést a webhookra
            response = requests.post(
                WEBHOOK_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            
            # Ellenőrizzük a válasz státuszát
            if response.status_code in (200, 201, 202):
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response": self._safe_parse_json(response.text)
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": f"A webhook nem fogadta el a kérést: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Hiba történt a webhook hívása közben: {str(e)}"
            }
    
    def _safe_parse_json(self, text):
        """
        Biztonságosan próbálja meg parse-olni a JSON választ.
        """
        try:
            return json.loads(text)
        except:
            return text

if __name__ == "__main__":
    # Teszteljük az eszközt egy minta poszttal
    property_data = {
        "address": "Budapest, XII. kerület, Normafa út",
        "price": "750 000 000 Ft",
        "rooms": "5 szoba + 2 fürdőszoba",
        "size": "240 m²"
    }
    
    post_content = """🌟 LUXUS A NORMAFÁNÁL - PANORÁMÁS ÁLOMOTTHON 🌟

Büszkén mutatjuk be ezt a lélegzetelállító luxusingatlant a Normafa szívében, amely ötvözi az exkluzivitást és a természet közelségét.

📍 Budapest, XII. kerület, Normafa út
💰 750 000 000 Ft
🏠 5 szoba + 2 fürdőszoba
📏 240 m²

Különleges jellemzők:
✅ Páratlan panoráma a városra
✅ Privát medence és jakuzzi
✅ Intelligens okosotthon rendszer
✅ Exkluzív belső design

Érdeklődés esetén keresse luxus ingatlan tanácsadóinkat!

#luxusingatlan #normafa #panorama #budapestluxury #exclusivehome #veyronhungary #dreamhome"""
    
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
    
    sender = webhook_sender(
        post_content=post_content,
        property_data=property_data,
        image_urls=image_urls
    )
    
    # Teszt üzemmódban ne küldjük el ténylegesen
    print("Webhook payload előkészítve:", json.dumps(
        {
            "post_content": sender.post_content,
            "property_data": sender.property_data,
            "image_urls": sender.image_urls,
            "timestamp": int(time.time()),
            "source": "Veyron Hungary AI Assistant"
        }, 
        indent=2
    )) 