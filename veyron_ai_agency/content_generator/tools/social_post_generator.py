from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # környezeti változók betöltése

# OpenAI API kulcs a környezeti változóból
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class social_post_generator(BaseTool):
    """
    Eszköz professzionális social media posztok generálására luxusingatlanokhoz OpenAI segítségével.
    A generált poszt figyelemfelkeltő szöveget, strukturált információkat és hashtag-eket tartalmaz.
    """
    property_data: dict = Field(
        ..., description="Az ingatlan adatait tartalmazó szótár (cím, ár, szobák száma, stb.)"
    )
    image_urls: list = Field(
        [], description="A feltöltött képek URL-jeinek listája"
    )
    post_language: str = Field(
        "hungarian", description="A poszt nyelve (hungarian vagy english)"
    )
    post_style: str = Field(
        "elegant", description="A poszt stílusa (elegant, creative, minimalist, stb.)"
    )

    def run(self):
        """
        Generál egy professzionális social media posztot a megadott ingatlanadatok alapján.
        """
        try:
            # Ellenőrizzük az API kulcsot
            if not OPENAI_API_KEY:
                return {
                    "success": False, 
                    "error": "Az OPENAI_API_KEY környezeti változó nincs beállítva"
                }
            
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            # Előkészítjük a prompt-ot
            prompt = self._prepare_prompt()
            
            # Meghívjuk a GPT-4 Turbo-t
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": """
                    Luxury ingatlan marketing szakértő vagy, aki lenyűgöző és professzionális social media posztokat készít.
                    A posztodnak elegánsnak, figyelemfelkeltőnek és értékesítés-orientáltnak kell lennie.
                    
                    Követelmények:
                    1. Figyelemfelkeltő, érzelmi húrokat pengető bevezetés
                    2. Az ingatlan főbb adatainak strukturált bemutatása
                    3. Az egyedi értékesítési pontok kiemelése
                    4. Erőteljes záró felhívás
                    5. Releváns hashtag-ek (5-7 db)
                    
                    A szöveg legyen elegáns, presztízst sugárzó, de ne legyen túlzó vagy hamis.
                    """},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Visszaadjuk a generált posztot
            post_content = response.choices[0].message.content
            
            return {
                "success": True,
                "post_content": post_content,
                "image_count": len(self.image_urls),
                "language": self.post_language
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Hiba történt a poszt generálása közben: {str(e)}"
            }
    
    def _prepare_prompt(self):
        """
        Előkészíti a promptot a GPT számára az ingatlanadatok alapján.
        """
        # Alapvető adatok ellenőrzése
        address = self.property_data.get("address", "")
        price = self.property_data.get("price", "")
        rooms = self.property_data.get("rooms", "")
        size = self.property_data.get("size", "")
        features = self.property_data.get("features", [])
        selling_points = self.property_data.get("selling_points", [])
        
        # Képek számának ellenőrzése
        image_count = len(self.image_urls)
        
        # Nyelvi beállítás
        language_text = "magyar" if self.post_language.lower() == "hungarian" else "angol"
        
        # Prompt összeállítása
        prompt = f"""
        Kérlek, generálj egy professzionális {language_text} nyelvű social media posztot (Facebook/Instagram) az alábbi luxusingatlanról:
        
        Alapadatok:
        - Cím: {address}
        - Ár: {price}
        - Szobák száma: {rooms}
        - Alapterület: {size}
        """
        
        if features:
            prompt += "\nFőbb jellemzők:\n"
            for feature in features:
                prompt += f"- {feature}\n"
        
        if selling_points:
            prompt += "\nEgyedi eladási érvek:\n"
            for point in selling_points:
                prompt += f"- {point}\n"
        
        if image_count > 0:
            prompt += f"\nA poszthoz {image_count} kép lesz csatolva."
            
        prompt += """
        
        A posztnak az alábbi részeket kell tartalmaznia:
        1. Egy figyelemfelkeltő bevezető rész, amely érzelmi húrokat is megpendít
        2. Az ingatlan főbb adatainak strukturált bemutatása
        3. Az egyedi értékesítési pontok kiemelése
        4. Erőteljes záró felhívás további információk kérésére
        5. 5-7 releváns hashtag
        
        A szöveg legyen elegáns, presztízst sugárzó, de ne legyen túlzó.
        """
        
        return prompt

if __name__ == "__main__":
    # Teszteljük az eszközt egy minta ingatlannal
    property_data = {
        "address": "Budapest, XII. kerület, Normafa út",
        "price": "750 000 000 Ft",
        "rooms": "5 szoba + 2 fürdőszoba",
        "size": "240 m²",
        "features": ["Panorámás kilátás", "Medence", "Okosotthon", "Privát kert", "Jakuzzi"],
        "selling_points": [
            "A Normafa közvetlen közelében található luxusingatlan",
            "Lenyűgöző panoráma a városra",
            "Teljesen felújított, modern technológiával felszerelt",
            "Exkluzív környék, kiváló befektetés"
        ]
    }
    
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg"
    ]
    
    generator = social_post_generator(
        property_data=property_data,
        image_urls=image_urls,
        post_language="hungarian"
    )
    
    result = generator.run()
    print(result) 