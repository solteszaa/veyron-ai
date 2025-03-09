'use client';

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([
    { role: 'assistant', content: 'Üdvözlöm! Én vagyok a Veyron Hungary AI Ingatlan Marketing Asszisztens. Miben segíthetek?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Felhasználói üzenet hozzáadása
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // API hívás a backend felé
      const response = await axios.post('/api/chat', {
        message: input
      });
      
      // Válasz hozzáadása
      setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
    } catch (error) {
      console.error('Hiba történt az üzenet küldése közben:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sajnálom, hiba történt a válasz feldolgozása közben. Kérjük, próbálja újra később.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 sm:p-24">
      <div className="z-10 max-w-5xl w-full flex flex-col h-screen">
        <h1 className="text-3xl font-bold text-center my-6">
          Veyron Hungary AI Ingatlan Marketing Asszisztens
        </h1>
        
        <div className="flex-1 overflow-y-auto border border-gray-300 rounded-lg p-4 mb-4">
          {messages.map((message, index) => (
            <div 
              key={index} 
              className={`mb-4 p-3 rounded-lg ${
                message.role === 'user' 
                  ? 'bg-blue-100 ml-12' 
                  : 'bg-gray-100 mr-12'
              }`}
            >
              <p className="text-sm font-semibold">{message.role === 'user' ? 'Ön' : 'Asszisztens'}</p>
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-center items-center mb-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          )}
        </div>
        
        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Írja be kérdését..."
            className="flex-1 p-2 border border-gray-300 rounded"
            disabled={isLoading}
          />
          <button 
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-blue-300"
            disabled={isLoading || !input.trim()}
          >
            Küldés
          </button>
        </form>
        
        <div className="mt-4 text-center text-xs text-gray-500">
          <p>Vercel Demo Verzió - A válaszok csak illusztratív célt szolgálnak</p>
          <p>A teljes verzió külön háttérszolgáltatást igényel</p>
        </div>
      </div>
    </main>
  );
} 