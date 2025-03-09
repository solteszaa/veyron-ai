import { NextRequest, NextResponse } from 'next/server';

// Vercel serverless függvény, amely nem támogatja a hosszan futó folyamatokat vagy fájlrendszer műveleteket
export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json();
    
    // Fejlesztési környezetben naplózzuk az üzenetet
    console.log("Felhasználói üzenet:", message);
    
    // Egyszerű demo válasz az API teszteléséhez
    // Valós implementációban itt API hívás történne egy külső backend szolgáltatás felé
    const demoResponse = "Ez egy ideiglenes válasz a Vercel serverless környezetből. Valós környezetben ez az API végpont továbbítaná a kérést egy külön háttérszolgáltatásnak, amely az AI agentet futtatja.";
    
    // Késleltetés szimulálása az AI válaszidejének utánzásához (500ms)
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return NextResponse.json({ response: demoResponse });
  } catch (error) {
    console.error('Hiba az API kérés feldolgozása közben:', error);
    return NextResponse.json(
      { error: 'Belső szerverhiba történt.' },
      { status: 500 }
    );
  }
} 