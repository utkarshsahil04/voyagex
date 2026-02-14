
import React from 'react';

interface Props {
  onStart: () => void;
}

const LandingPage: React.FC<Props> = ({ onStart }) => {
  return (
    <div className="pb-24">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 ios-blur bg-background-dark/80 border-b border-primary/10 max-w-md mx-auto">
        <div class="px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <span className="material-icons text-background-dark text-xl">shield</span>
            </div>
            <span className="font-bold text-xl tracking-tight text-white">AllergyGuard</span>
          </div>
          <button className="bg-primary/20 text-primary px-4 py-1.5 rounded-full font-medium text-sm">
            Login
          </button>
        </div>
      </header>

      <main className="pt-16">
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-12 pb-20 px-6">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
              Now available in 500+ locations
            </div>
            <h1 className="text-4xl font-extrabold mb-6 leading-tight text-white">
              Safe Dining, <br/>
              <span className="text-primary">Simplified.</span>
            </h1>
            <p className="text-slate-400 text-lg mb-10 max-w-sm mx-auto">
              Navigate menus with confidence using real-time allergen detection designed for your safety.
            </p>
            <div className="flex flex-col gap-4">
              <button onClick={onStart} className="w-full bg-primary hover:bg-primary/90 text-background-dark font-bold py-4 rounded-xl shadow-lg shadow-primary/20 transition-all">
                Get Started
              </button>
              <button className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-4 rounded-xl transition-all">
                View Partner Map
              </button>
            </div>
          </div>

          {/* Hero Illustration */}
          <div className="mt-16 relative">
            <div className="absolute inset-0 bg-primary/20 blur-3xl rounded-full -z-10"></div>
            <div className="bg-slate-900 rounded-[2.5rem] p-3 border-4 border-slate-800 shadow-2xl relative">
              <img alt="App view" className="rounded-[2rem] w-full aspect-[9/19] object-cover opacity-80" src="https://picsum.photos/seed/scanapp/400/800"/>
              <div className="absolute inset-0 flex flex-col items-center justify-center p-8 pointer-events-none">
                <div className="bg-white/10 backdrop-blur-md p-6 rounded-3xl border border-white/20 flex flex-col items-center">
                  <div className="w-16 h-16 rounded-full bg-primary flex items-center justify-center mb-4">
                    <span className="material-icons text-3xl text-background-dark">check_circle</span>
                  </div>
                  <span className="text-white font-bold text-xl text-center">Menu Safe</span>
                  <span className="text-white/60 text-sm text-center">No allergens detected</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-20 px-6 bg-background-dark/50">
          <h2 className="text-3xl font-bold text-center mb-16 text-white">How it Works</h2>
          <div className="space-y-12">
            {[
              { icon: 'qr_code_scanner', title: 'Scan', desc: 'Point your camera at any AllergyGuard QR code on the restaurant menu.' },
              { icon: 'analytics', title: 'Detect', desc: 'Instantly identify ingredients matching your personal allergen profile.' },
              { icon: 'verified_user', title: 'Protect', desc: 'Eat with peace of mind knowing your meal is safe and verified.' }
            ].map((step, idx) => (
              <div key={idx} className="flex gap-6">
                <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center">
                  <span className="material-icons text-primary">{step.icon}</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2 text-white">{step.title}</h3>
                  <p className="text-slate-400">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Map Section */}
        <section className="py-20 px-6">
          <div className="rounded-3xl overflow-hidden border border-slate-800 bg-slate-900">
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-2 text-white">Find Safe Eats</h2>
              <p className="text-slate-400 text-sm mb-6">Explore 500+ restaurants that prioritize your safety.</p>
              <div className="aspect-video rounded-2xl bg-slate-800 overflow-hidden relative">
                <img alt="Map" className="w-full h-full object-cover grayscale opacity-40" src="https://picsum.photos/seed/map/600/400"/>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="bg-primary p-2 rounded-full shadow-lg">
                    <span className="material-icons text-background-dark">location_on</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="border-t border-slate-800 p-4 bg-slate-900/50 flex justify-between items-center">
              <span className="text-sm font-medium text-slate-300">Near your location</span>
              <span className="text-primary text-sm font-bold">12 Restaurants</span>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-24 px-6 bg-primary text-background-dark text-center mt-10">
          <span className="material-icons text-5xl mb-6">restaurant</span>
          <h2 className="text-3xl font-extrabold mb-4">Ready for a worry-free meal?</h2>
          <p className="text-background-dark/80 mb-10 font-medium">Join 50k+ diners who trust AllergyGuard every day.</p>
          <button onClick={onStart} className="bg-background-dark text-primary px-10 py-4 rounded-xl font-bold text-lg shadow-xl">
            Create My Profile
          </button>
        </section>
      </main>

      <footer className="py-12 px-6 border-t border-slate-800 text-center text-slate-500">
        <div className="flex items-center justify-center gap-2 mb-6 opacity-50">
          <span className="material-icons text-sm">shield</span>
          <span className="font-bold tracking-tight text-sm">AllergyGuard</span>
        </div>
        <p className="text-xs mb-8">© 2024 AllergyGuard. Safe dining for everyone.</p>
        <div className="flex justify-center gap-6">
          <span className="material-icons">facebook</span>
          <span className="material-icons">camera_alt</span>
          <span className="material-icons">alternate_email</span>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
