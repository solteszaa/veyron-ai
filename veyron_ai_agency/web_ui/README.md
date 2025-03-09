# Veyron AI Web Felület

Ez a projekt egy webes felületet biztosít a Veyron Hungary AI Ingatlan Marketing Asszisztens számára.

## Telepítés és Futtatás

### Fejlesztői környezet beállítása

1. Telepítse a függőségeket:

```bash
npm install
```

2. Indítsa el a fejlesztői szervert:

```bash
npm run dev
```

3. Nyissa meg a böngészőben: [http://localhost:3000](http://localhost:3000)

### Vercel Telepítés

A projekt egyszerűen telepíthető a Vercel platformra az alábbi lépésekkel:

1. Regisztráljon vagy jelentkezzen be a [Vercel](https://vercel.com) platformra.

2. Importálja a GitHub projektjét.

3. Adja meg a környezeti változókat (ha szükséges).

4. Kattintson a "Deploy" gombra.

## Rendszerkövetelmények

- Node.js 18.x vagy újabb
- Python 3.8 vagy újabb a háttérrendszerhez

## Architektúra

A webfelület a Next.js keretrendszert használja, amely a háttérben kommunikál a Python-alapú AI agentekkel. A kommunikáció fájlalapú, ahol:

1. A felhasználói üzeneteket a `temp_user_message.txt` fájlba írjuk.
2. Az AI válaszát a `temp_assistant_response.txt` fájlból olvassuk ki.

A háttérrendszer egy egyszerű Python szkript (`api_handler.py`), amely kezeli az AI agent futtatását és a válaszok visszaadását.

## Környezeti Változók

Az alkalmazás működéséhez az alábbi környezeti változók szükségesek:

- `OPENAI_API_KEY` - Az OpenAI API kulcsa, amelyet az AI agent használ.

## Korlátok a Vercel Platformon

A Vercel platformon való futtatás során ügyelni kell arra, hogy:

1. Az API végpontok "serverless" környezetben futnak, így hosszú ideig tartó folyamatok nem ajánlottak.
2. A fájlrendszer nem perzisztens, így a fájlalapú kommunikációt módosítani kell a termelési környezetben.

A termelési környezetben érdemes lehet a következő módosításokat elvégezni:
- Adatbázis használata a fájlok helyett (pl. MongoDB, Supabase, stb.)
- Az AI agent futtatása egy külön szerveren (pl. AWS Lambda, Google Cloud Functions, stb.)
- WebSocket bevezetése a valós idejű kommunikációhoz 