from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # környezeti változók betöltése

# OpenAI API kulcs a környezeti változóból
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class hashtag_generator(BaseTool):
    """
    Eszköz releváns hashtag-ek generálására ingatlan social media posztokhoz.
    Létrehoz egy listát a legjobb hashtag-ekből az ingatlan jellemzői alapján.
    """
    property_data: dict = Field(
        ..., description="Az ingatlan adatait tartalmazó szótár"
    )
    count: int = Field(
        7, description="A generálandó hashtag-ek száma"
    )
    language: str = Field(
        "hungarian", description="A hashtag-ek nyelve (hungarian, english, vagy mixed)"
    )

    def run(self):
        """
        Generál releváns hashtag-eket az ingatlan jellemzői alapján.
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
            property_features = []
            
            # Az ingatlan főbb jellemzőinek összegyűjtése
            address = self.property_data.get("address", "")
            if address:
                parts = address.split(",")
                if len(parts) > 1:
                    location = parts[0].strip()  # Város
                    district = parts[1].strip() if len(parts) > 1 else ""  # Kerület/környék
                    property_features.extend([location, district])
            
            # Egyéb jellemzők
            features = self.property_data.get("features", [])
            property_features.extend(features)
            
            # Egyedi eladási érvek
            selling_points = self.property_data.get("selling_points", [])
            property_features.extend(selling_points)
            
            # Prompt összeállítása
            language_text = "magyar" if self.language.lower() == "hungarian" else "angol"
            
            prompt = f"""
            Generálj {self.count} darab releváns, {language_text} nyelvű hashtag-et egy luxusingatlan social media posztjához.
            
            Az ingatlan jellemzői:
            - {", ".join(property_features)}
            
            A hashtag-ek legyenek relevánsak a luxusingatlan piachoz, az ingatlan jellemzőihez és a Veyron Hungary brandhez.
            Minden hashtag # jellel kezdődjön, és ne tartalmazzon szóközöket vagy speciális karaktereket.
            """
            
            # Meghívjuk a GPT-4 Turbo-t
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Luxury ingatlan marketing szakértő vagy, aki releváns és hatékony hashtag-eket készít social media posztokhoz."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            # Feldolgozzuk a választ
            hashtag_text = response.choices[0].message.content
            
            # Hashtag-ek kinyerése a szövegből
            hashtags = []
            for line in hashtag_text.split("\n"):
                line = line.strip()
                if line.startswith("#"):
                    # Ha több hashtag van egy sorban, szétválasztjuk őket
                    for tag in line.split():
                        if tag.startswith("#"):
                            hashtags.append(tag)
            
            # Ha nem sikerült megfelelő számú hashtag-et kinyerni, próbáljuk máshogy
            if len(hashtags) < self.count:
                import re
                all_tags = re.findall(r'#\w+', hashtag_text)
                hashtags = list(set(all_tags))  # Egyedi hashtag-ek
            
            # Korlátozzuk a hashtag-ek számát
            hashtags = hashtags[:self.count]
            
            return {
                "success": True,
                "hashtags": hashtags,
                "count": len(hashtags),
                "language": self.language
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Hiba történt a hashtag-ek generálása közben: {str(e)}"
            }

if __name__ == "__main__":
    # Teszteljük az eszközt egy minta ingatlannal
    property_data = {
        "address": "Budapest, XII. kerület, Normafa út",
        "features": ["Panorámás kilátás", "Medence", "Okosotthon", "Privát kert"],
        "selling_points": [
            "A Normafa közvetlen közelében található luxusingatlan",
            "Lenyűgöző panoráma a városra"
        ]
    }
    
    generator = hashtag_generator(
        property_data=property_data,
        count=7,
        language="hungarian"
    )
    
    result = generator.run()
    print(result) 