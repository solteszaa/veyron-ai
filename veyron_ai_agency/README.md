# Veyron Hungary AI Ingatlan Marketing Asszisztens

## Áttekintés

A Veyron Hungary AI Ingatlan Marketing Asszisztens egy intelligens chatbot, amely luxusingatlanok hatékony közösségi média promócióját segíti. Az asszisztens chat-alapú interfészen keresztül kommunikál, begyűjti az ingatlanhoz kapcsolódó adatokat, képeket kezel, és professzionális Facebook/Instagram posztot generál.

## Funkciók

- **Strukturált adatgyűjtés**: Automatikusan bekéri az ingatlan összes releváns adatát (cím, ár, szobák száma, alapterület, jellemzők, stb.)
- **Képkezelés**: Feltölti és optimalizálja a képeket az ImgBB szolgáltatásra
- **AI-alapú tartalomgenerálás**: Professzionális social media posztok és hashtag-ek generálása
- **Webhook integráció**: A kész anyagok továbbítása külső rendszerekbe

## Telepítés

1. Klónozd a repository-t:
```
git clone https://github.com/yourusername/veyron-ai.git
cd veyron-ai/veyron_ai_agency
```

2. Telepítsd a függőségeket:
```
pip install -r requirements.txt
```

3. Hozz létre egy `.env` fájlt a következő API kulcsokkal:
```
OPENAI_API_KEY=your_openai_api_key
IMGBB_API_KEY=your_imgbb_api_key
WEBHOOK_URL=your_webhook_url
```

## Használat

Az ügynökség indításához futtasd:

```
python agency.py
```

Ez elindítja a terminál demo módot, ahol közvetlenül kommunikálhatsz az asszisztenssel.

## Ügynökség Struktúra

Az ügynökség a következő ágensekből áll:

1. **Koordinátor**: Fő kommunikációs pont a felhasználóval
2. **Ingatlan Adatgyűjtő**: Ingatlanadatok validálása és strukturálása
3. **Képfeldolgozó**: Képek kezelése és ImgBB-re való feltöltése
4. **Tartalomgeneráló**: Social media posztok és hashtag-ek generálása
5. **Webhook Kezelő**: A generált tartalom továbbítása külső rendszerekbe

## Fejlesztés

A projekt az Agency Swarm keretrendszerre épül, amely lehetővé teszi együttműködő AI ágensek létrehozását. Minden ágens saját eszközökkel és utasításokkal rendelkezik.

### Új eszköz hozzáadása

Új eszköz hozzáadásához hozz létre egy új Python fájlt a megfelelő ágens `tools` mappájában:

```python
from agency_swarm.tools import BaseTool
from pydantic import Field

class MyNewTool(BaseTool):
    """
    Az új eszköz leírása.
    """
    param1: str = Field(..., description="Az első paraméter leírása")
    
    def run(self):
        """
        Az eszköz futtatási logikája.
        """
        # Implementáció
        return "Eredmény"
```

## Licenc

[MIT](LICENSE)

## Kapcsolat

Veyron Hungary - [info@veyron.hu](mailto:info@veyron.hu) 