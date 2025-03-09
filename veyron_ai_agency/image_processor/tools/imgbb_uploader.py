from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import requests
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

load_dotenv()  # környezeti változók betöltése

# ImgBB API kulcs a környezeti változóból
API_KEY = os.getenv("IMGBB_API_KEY", "10a106f9930a12af0764cd2b8c28b274")

class imgbb_uploader(BaseTool):
    """
    Eszköz képek feltöltésére az ImgBB szolgáltatásra.
    A feltöltött képekből visszaadja a URL-t, hogy a social media posztokba beilleszthető legyen.
    """
    image_data: str = Field(
        ..., description="Base64 kódolt kép adat, vagy a kép URL-je"
    )
    name: str = Field(
        "veyron_image", description="A feltöltött kép neve"
    )

    def run(self):
        """
        Feltölti a képet az ImgBB-re és visszaadja a képadatokat, beleértve a közvetlen URL-t.
        """
        try:
            # Ellenőrzés, hogy van-e API kulcs
            if not API_KEY:
                return {
                    "success": False,
                    "error": "Az IMGBB_API_KEY környezeti változó nincs beállítva"
                }
            
            # Ha URL-t kaptunk, letöltjük a képet
            image_data = self.image_data
            if image_data.startswith(('http://', 'https://')):
                image_data = self._download_and_encode_image(image_data)
                if not image_data:
                    return {
                        "success": False,
                        "error": "Nem sikerült letölteni a képet a megadott URL-ről"
                    }
            
            # Eltávolítjuk a base64 prefix-et, ha van
            if image_data.startswith('data:image'):
                image_data = image_data.split(',', 1)[1]
            
            # API végpont
            url = "https://api.imgbb.com/1/upload"
            
            # Form adatok előkészítése
            payload = {
                'key': API_KEY,
                'image': image_data,
                'name': self.name
            }
            
            # POST kérés küldése
            response = requests.post(url, data=payload)
            
            # Válasz ellenőrzése
            if response.status_code == 200:
                json_response = response.json()
                if json_response.get('success'):
                    data = json_response.get('data', {})
                    return {
                        "success": True,
                        "url": data.get('url'),
                        "delete_url": data.get('delete_url'),
                        "display_url": data.get('display_url'),
                        "thumbnail": data.get('thumb', {}).get('url')
                    }
                else:
                    return {
                        "success": False,
                        "error": json_response.get('error', {}).get('message', 'Ismeretlen hiba az ImgBB API-val')
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP hiba: {response.status_code}, {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Hiba történt a kép feltöltése közben: {str(e)}"
            }
    
    def _download_and_encode_image(self, url):
        """
        Letölt egy képet a megadott URL-ről és base64 kódolásban visszaadja.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Képoptimalizálás
                image = Image.open(BytesIO(response.content))
                output = BytesIO()
                image.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Base64 kódolás
                return base64.b64encode(output.getvalue()).decode('utf-8')
            return None
        except Exception:
            return None

if __name__ == "__main__":
    # Teszt URL-lel
    test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png"
    uploader = imgbb_uploader(image_data=test_image_url, name="test_image")
    result = uploader.run()
    print(result) 