from agency_swarm import Agency
from coordinator import Coordinator
from property_collector import PropertyCollector
from image_processor import ImageProcessor
from content_generator import ContentGenerator
from webhook_manager import WebhookManager

# Ágensek létrehozása
coordinator = Coordinator()
property_collector = PropertyCollector()
image_processor = ImageProcessor()
content_generator = ContentGenerator()
webhook_manager = WebhookManager()

# Ügynökség létrehozása a kommunikációs folyamatokkal
agency = Agency(
    [
        coordinator,  # Koordinátor lesz a belépési pont a felhasználói kommunikációhoz
        [coordinator, property_collector],  # Koordinátor kommunikálhat az adatgyűjtővel
        [coordinator, image_processor],  # Koordinátor kommunikálhat a képfeldolgozóval
        [coordinator, content_generator],  # Koordinátor kommunikálhat a tartalomgenerálóval
        [coordinator, webhook_manager],  # Koordinátor kommunikálhat a webhook kezelővel
        [property_collector, content_generator],  # Adatgyűjtő átadhatja az adatokat a tartalomgenerálónak
        [image_processor, content_generator],  # Képfeldolgozó átadhatja a képeket a tartalomgenerálónak
        [content_generator, webhook_manager]  # Tartalomgeneráló átadhatja a tartalmat a webhook kezelőnek
    ],
    shared_instructions="agency_manifesto.md",  # Közös instrukciók minden ágensnek
    temperature=0.5,  # Alapértelmezett hőmérséklet
    max_prompt_tokens=25000  # Maximális token szám a promptban
)

if __name__ == "__main__":
    # Ügynökség indítása terminál demo módban
    agency.run_demo() 