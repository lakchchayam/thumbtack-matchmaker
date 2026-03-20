"use client";

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Send, Star, MapPin, Briefcase, CheckCircle2, Loader2, Sparkles } from 'lucide-react';

interface Pro {
  id: string;
  name: string;
  profession: string;
  location: string;
  description: string;
  rating: number;
  reviews: number;
}

interface Message {
  role: 'user' | 'agent';
  content: string;
  pros?: Pro[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'agent', content: "Hi! I'm the Thumbtack AI Matchmaker. Tell me what kind of project you need help with today." }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  // Auto scroll to bottom
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);
  
  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMsg })
      });
      const data = await res.json();
      
      setMessages(prev => [...prev, { 
        role: 'agent', 
        content: data.response || "I couldn't process that request.",
        pros: data.pros 
      }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'agent', content: "Network error. Make sure the backend FastAPI server is running." }]);
    }
    
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10 px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-2 text-indigo-600 font-bold text-2xl tracking-tight">
          <Sparkles className="w-6 h-6 text-indigo-500" />
          <span>Thumbtack AI</span>
        </div>
        <div className="text-sm font-semibold text-slate-500 hover:text-indigo-600 cursor-pointer transition-colors">
          Explore Projects
        </div>
      </header>

      <main className="max-w-5xl mx-auto p-4 md:p-8 flex flex-col items-center">
        
        <div className="w-full text-center mb-8 mt-4">
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight mb-4">
            Find the right pro, <br className="hidden md:block" /> <span className="text-indigo-600">powered by AI.</span>
          </h1>
          <p className="text-lg text-slate-500 font-medium max-w-2xl mx-auto">
            Describe your project in natural language and our Matchmaker agent will instantly find the best local professionals for the job.
          </p>
        </div>

        <div className="w-full max-w-3xl bg-white rounded-3xl shadow-2xl shadow-indigo-100/50 border border-slate-100 overflow-hidden flex flex-col" style={{ height: '600px' }}>
          
          {/* Chat Messages Area */}
          <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-6 bg-slate-50/50 scroller">
            <AnimatePresence>
              {messages.map((msg, idx) => (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  key={idx}
                  className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
                >
                  <div className={`px-5 py-3.5 rounded-2xl max-w-[85%] text-[15px] font-medium ${msg.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-sm shadow-md' : 'bg-white border border-slate-200 text-slate-700 rounded-tl-sm shadow-sm'}`}>
                    <p className="leading-relaxed">{msg.content}</p>
                  </div>
                  
                  {msg.pros && msg.pros.length > 0 && (
                    <div className="mt-4 flex flex-col gap-4 w-full max-w-[95%] md:max-w-[80%] ml-2">
                      {msg.pros.map(pro => (
                        <motion.div 
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 0.1 }}
                          key={pro.id} 
                          className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-lg hover:border-indigo-200 transition-all cursor-pointer flex gap-5 items-start relative overflow-hidden group"
                        >
                          <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-50 rounded-full blur-3xl -mr-10 -mt-10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                          
                          <div className="w-14 h-14 rounded-full bg-indigo-100/80 flex items-center justify-center flex-shrink-0 text-indigo-600 font-extrabold text-xl relative z-10 border border-indigo-200/50">
                            {pro.name.charAt(0)}
                          </div>
                          
                          <div className="flex-1 relative z-10">
                            <h3 className="font-bold text-slate-900 text-lg flex items-center gap-1.5">
                              {pro.name} <CheckCircle2 className="w-4 h-4 text-indigo-500" />
                            </h3>
                            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500 mt-1.5 mb-2.5 font-semibold">
                              <span className="flex items-center gap-1.5 bg-slate-100 px-2 py-1 rounded-md text-slate-600"><Briefcase className="w-3 h-3" /> {pro.profession}</span>
                              <span className="flex items-center gap-1.5 bg-slate-100 px-2 py-1 rounded-md text-slate-600"><MapPin className="w-3 h-3" /> {pro.location}</span>
                            </div>
                            <p className="text-sm text-slate-600 leading-relaxed">{pro.description}</p>
                            <div className="flex items-center gap-1.5 mt-4 pt-4 border-t border-slate-100">
                              <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
                              <span className="text-sm font-bold text-slate-800">{pro.rating}</span>
                              <span className="text-xs text-slate-400 font-medium tracking-wide">({pro.reviews} verified reviews)</span>
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </motion.div>
              ))}
              
              {isLoading && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-start">
                  <div className="px-5 py-3.5 bg-white border border-slate-200 text-slate-700 rounded-2xl rounded-tl-sm shadow-sm flex items-center gap-2.5">
                    <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
                    <span className="text-[14px] text-slate-500 font-medium">Finding the best pros for you...</span>
                  </div>
                </motion.div>
              )}
              <div ref={endOfMessagesRef} />
            </AnimatePresence>
          </div>
          
          {/* Input Area */}
          <div className="p-4 bg-white border-t border-slate-100">
            <div className="relative flex items-center">
              <input 
                type="text" 
                className="w-full bg-slate-50 border border-slate-200 focus:bg-white focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100 rounded-2xl py-4 flex pl-6 pr-16 outline-none transition-all font-medium text-slate-800 placeholder-slate-400"
                placeholder="E.g., I need a plumber to fix a leaking pipe..."
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSend()}
              />
              <button 
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="absolute right-3 p-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-xl transition-all flex items-center justify-center transform active:scale-95 shadow-md shadow-indigo-200"
              >
                <Send className="w-5 h-5 ml-0.5" />
              </button>
            </div>
            <div className="text-center mt-3 mb-1">
              <span className="text-[11px] text-slate-400 font-medium uppercase tracking-wider">AI Matchmaker accesses verified Thumbtack profiles</span>
            </div>
          </div>
          
        </div>
      </main>

      <style jsx global>{`
        .scroller {
          scrollbar-width: thin;
          scrollbar-color: #cbd5e1 transparent;
        }
        .scroller::-webkit-scrollbar {
          width: 6px;
        }
        .scroller::-webkit-scrollbar-track {
          background: transparent;
        }
        .scroller::-webkit-scrollbar-thumb {
          background-color: #cbd5e1;
          border-radius: 20px;
        }
      `}</style>
    </div>
  );
}
