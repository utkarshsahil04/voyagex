import React, { useState } from 'react';
import { analyzeDish } from '../services/geminiService';
import { DishReport } from '../types';

interface Props {
  onBack: () => void;
  onResult: (report: DishReport) => void;
}

const ScanPage: React.FC<Props> = ({ onBack, onResult }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [manualId, setManualId] = useState('');

  const handleScan = async (dishName: string) => {
    setIsAnalyzing(true);
    try {
      const result = await analyzeDish(dishName);
      onResult(result);
    } catch (e) {
      console.error(e);
      alert('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="relative h-screen w-full flex flex-col items-center justify-between overflow-hidden">
      {/* Fake Viewfinder */}
      <div className="absolute inset-0 z-0">
        <img alt="Restaurant Bg" className="w-full h-full object-cover brightness-75 contrast-125" src="https://picsum.photos/seed/restaurant/800/1200"/>
        <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-black/60"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 w-full px-6 pt-12 flex items-center justify-between">
        <button onClick={onBack} className="w-10 h-10 rounded-full bg-black/30 backdrop-blur-md flex items-center justify-center border border-white/10 text-white">
          <span className="material-icons">chevron_left</span>
        </button>
        <div className="flex items-center space-x-2 bg-black/30 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 text-white">
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
          <span className="text-[10px] font-medium tracking-widest uppercase">Live Scan</span>
        </div>
        <button className="w-10 h-10 rounded-full bg-black/30 backdrop-blur-md flex items-center justify-center border border-white/10 text-white">
          <span className="material-icons">flash_on</span>
        </button>
      </header>

      {/* Reticle */}
      <main className="relative z-10 flex-1 w-full flex flex-col items-center justify-center px-10">
        <div className="relative w-full max-w-[280px] aspect-square">
          <div className="absolute top-0 left-0 w-12 h-12 border-t-4 border-l-4 border-primary rounded-tl-xl"></div>
          <div className="absolute top-0 right-0 w-12 h-12 border-t-4 border-r-4 border-primary rounded-tr-xl"></div>
          <div className="absolute bottom-0 left-0 w-12 h-12 border-b-4 border-l-4 border-primary rounded-bl-xl"></div>
          <div className="absolute bottom-0 right-0 w-12 h-12 border-b-4 border-r-4 border-primary rounded-br-xl"></div>
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-primary/60 shadow-[0_0_15px_rgba(18,226,88,0.8)] scanning-line"></div>
          <div className="absolute inset-4 border border-white/10 rounded-lg bg-primary/5 backdrop-blur-[2px] flex items-center justify-center">
            {isAnalyzing && (
              <div className="text-center text-white p-4">
                <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
                <p className="text-xs font-bold uppercase tracking-widest">Analyzing...</p>
              </div>
            )}
          </div>
          <div className="absolute -bottom-16 left-0 right-0 text-center">
            <p className="text-white/80 text-sm font-medium drop-shadow-md">Align QR code within the frame</p>
          </div>
        </div>
      </main>

      {/* Footer / Manual Input */}
      <footer className="relative z-10 w-full p-6 pb-10 bg-gradient-to-t from-black via-black/80 to-transparent">
        <div className="max-w-md mx-auto space-y-6">
          <div onClick={() => handleScan("Pad Thai")} className="cursor-pointer bg-white/10 backdrop-blur-xl border border-white/10 rounded-2xl p-5 shadow-2xl">
            <div className="flex items-start space-x-4">
              <div className="p-2 bg-primary/20 rounded-lg">
                <span className="material-icons text-primary">qr_code_scanner</span>
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-white text-lg leading-tight">AllergyGuard Scan</h3>
                <p className="text-white/60 text-sm mt-1">Tap this card to simulate scanning "Pad Thai".</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10"></div>
              </div>
              <div className="relative flex justify-center">
                <span className="px-3 bg-black text-[10px] font-semibold text-white/40 uppercase tracking-widest">or enter manually</span>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 material-icons text-white/40 text-lg">tag</span>
                <input 
                  className="w-full bg-white/5 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-white placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm" 
                  placeholder="Dish name (e.g. Burger)" 
                  type="text"
                  value={manualId}
                  onChange={(e) => setManualId(e.target.value)}
                />
              </div>
              <button 
                onClick={() => handleScan(manualId || "Burger")}
                disabled={isAnalyzing}
                className="bg-primary hover:bg-primary/90 text-background-dark font-bold px-6 py-4 rounded-xl transition-transform active:scale-95 flex items-center justify-center disabled:opacity-50"
              >
                <span className="material-icons">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ScanPage;