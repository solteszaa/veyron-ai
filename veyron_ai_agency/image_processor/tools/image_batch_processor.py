from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from .imgbb_uploader import imgbb_uploader

class image_batch_processor(BaseTool):
    """
    Eszköz több kép egyszerre történő feldolgozására és feltöltésére az ImgBB szolgáltatásra.
    A feltöltött képekből visszaadja a URL-eket, hogy a social media posztokba beilleszthetők legyenek.
    """
    image_list: list = Field(
        ..., description="Lista, amely tartalmazza a képek adatait (URL-ek vagy base64 kódolt adatok)"
    )
    prefix: str = Field(
        "veyron_property", description="Előtag a képek nevéhez a feltöltéskor"
    )

    def run(self):
        """
        Sorban feltölti a képeket az ImgBB-re és visszaadja a képek URL-jeinek listáját.
        """
        uploaded_urls = []
        errors = []
        
        # Végigmegyünk minden képen a listában
        for i, image_data in enumerate(self.image_list):
            try:
                # Létrehozzuk az ImgBB feltöltő eszközt
                uploader = imgbb_uploader(
                    image_data=image_data,
                    name=f"{self.prefix}_{i+1}"
                )
                
                # Feltöltjük a képet
                result = uploader.run()
                
                # Ellenőrizzük, hogy sikeres volt-e a feltöltés
                if result.get("success"):
                    uploaded_urls.append(result.get("url"))
                else:
                    errors.append(f"Hiba a {i+1}. kép feltöltésekor: {result.get('error')}")
            except Exception as e:
                errors.append(f"Nem várt hiba a {i+1}. kép feldolgozásakor: {str(e)}")
        
        # Visszaadjuk az eredményt
        return {
            "success": len(errors) == 0,
            "uploaded_count": len(uploaded_urls),
            "total_count": len(self.image_list),
            "urls": uploaded_urls,
            "errors": errors
        }

if __name__ == "__main__":
    # Teszt
    processor = image_batch_processor(
        image_list = [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg"
        ]
    )
    
    print(json.dumps(processor.run(), indent=2)) 