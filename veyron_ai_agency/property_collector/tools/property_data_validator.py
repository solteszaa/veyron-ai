from agency_swarm.tools import BaseTool
from pydantic import Field
import re

class property_data_validator(BaseTool):
    """
    Eszköz az ingatlanadatok validálására és strukturálására.
    Ellenőrzi, hogy minden szükséges adat megvan-e és megfelelő formátumú-e.
    """
    property_data: dict = Field(
        ..., description="Az ingatlan adatait tartalmazó szótár"
    )
    
    def run(self):
        """
        Validálja az ingatlan adatait és visszaadja a strukturált, tisztított adatokat.
        """
        validated_data = {}
        missing_fields = []
        warnings = []
        
        # Kötelező mezők ellenőrzése
        required_fields = ["address", "price", "rooms", "size"]
        
        for field in required_fields:
            if field not in self.property_data or not self.property_data[field]:
                missing_fields.append(field)
            else:
                validated_data[field] = self.property_data[field]
        
        # Ha hiányzik bármelyik kötelező mező, hibaüzenetet adunk vissza
        if missing_fields:
            return {
                "success": False,
                "missing_fields": missing_fields,
                "message": f"Hiányzó kötelező mezők: {', '.join(missing_fields)}"
            }
        
        # Opcionális mezők átvitele
        optional_fields = ["features", "selling_points"]
        for field in optional_fields:
            if field in self.property_data:
                # Ellenőrizzük, hogy lista-e
                if isinstance(self.property_data[field], list):
                    validated_data[field] = self.property_data[field]
                else:
                    # Ha string, próbáljuk meg listává alakítani
                    try:
                        if isinstance(self.property_data[field], str):
                            # Vesszővel elválasztott elemek listája
                            items = [item.strip() for item in self.property_data[field].split(",")]
                            validated_data[field] = [item for item in items if item]  # Üres elemek eltávolítása
                        else:
                            warnings.append(f"A(z) '{field}' mezőnek listának kell lennie.")
                    except Exception:
                        warnings.append(f"Nem sikerült a(z) '{field}' mezőt listává alakítani.")
        
        # Ár formátum ellenőrzése és tisztítása
        if "price" in validated_data:
            price = validated_data["price"]
            
            # Számjegyek kinyerése és ezres tagolás eltávolítása
            price_digits = re.sub(r'[^\d]', '', price)
            
            if price_digits:
                # Formázás: 123 456 789 Ft
                formatted_price = f"{int(price_digits):,} Ft".replace(",", " ")
                validated_data["price"] = formatted_price
            else:
                warnings.append("Az ár nem tartalmaz számjegyeket.")
        
        # Alapterület formátum ellenőrzése
        if "size" in validated_data:
            size = validated_data["size"]
            
            # Ha nincs mértékegység, hozzáadjuk
            if re.match(r'^\d+$', size.strip()):
                validated_data["size"] = f"{size.strip()} m²"
            # Ha nincs megfelelő formátum, figyelmeztetést adunk
            elif not re.search(r'm²|m2|négyzetméter', size, re.IGNORECASE):
                warnings.append("Az alapterületnél nincs vagy nem megfelelő a mértékegység. Ajánlott formátum: '150 m²'")
        
        # Egyéb adatmezők átvitele
        for key, value in self.property_data.items():
            if key not in validated_data and key not in optional_fields:
                validated_data[key] = value
        
        return {
            "success": True,
            "validated_data": validated_data,
            "warnings": warnings
        }

if __name__ == "__main__":
    # Teszteljük az eszközt egy minta ingatlannal
    property_data = {
        "address": "Budapest, XII. kerület, Normafa út",
        "price": "750000000",  # Formázatlan ár
        "rooms": "5 szoba + 2 fürdőszoba",
        "size": "240",  # Mértékegység nélkül
        "features": "Panorámás kilátás, Medence, Okosotthon, Privát kert",  # String formátum
        "selling_points": [  # Lista formátum
            "A Normafa közvetlen közelében található luxusingatlan",
            "Lenyűgöző panoráma a városra"
        ]
    }
    
    validator = property_data_validator(property_data=property_data)
    result = validator.run()
    print(result) 