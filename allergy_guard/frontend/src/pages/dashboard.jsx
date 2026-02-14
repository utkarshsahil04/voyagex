
import React from 'react';

interface Props {
  onScan: () => void;
  onNavigateHome: () => void;
}

const DashboardPage: React.FC<Props> = ({ onScan, onNavigateHome }) => {
  return (
    <div className="pb-24 px-4 bg-background-dark min-h-screen">
      <div className="h-12 w-full"></div>

      {/* Header */}
      <header className="flex justify-between items-center mb-6">
        <div>
          <h1 onClick={onNavigateHome} className="text-2xl font-bold text-white cursor-pointer">Dashboard</h1>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            <span className="text-xs font-medium text-slate-400">Live Status: Active</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="w-10 h-10 flex items-center justify-center rounded-full bg-card-dark relative text-slate-300">
            <span className="material-icons">notifications</span>
            <span className="absolute top-2 right-2 w-2.5 h-2.5 bg-danger border-2 border-background-dark rounded-full"></span>
          </button>
          <div className="w-10 h-10 rounded-full border-2 border-primary overflow-hidden">
            <img className="w-full h-full object-cover" src="https://picsum.photos/seed/user1/100/100" alt="Avatar" />
          </div>
        </div>
      </header>

      {/* Search */}
      <div className="relative mb-6">
        <span className="material-icons absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
        <input className="w-full pl-10 pr-4 py-3 bg-card-dark border-none rounded-xl focus:ring-2 focus:ring-primary text-sm shadow-sm text-white placeholder:text-slate-500" placeholder="Search dishes or ingredients..." type="text"/>
      </div>

      {/* Stats */}
      <div className="flex overflow-x-auto gap-4 mb-8 no-scrollbar pb-2">
        <div className="flex-none w-40 p-4 rounded-xl bg-card-dark border border-slate-800">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Live Menu</p>
          <div className="flex items-end justify-between">
            <span className="text-2xl font-bold text-white">42</span>
            <span className="material-icons text-primary text-xl">restaurant_menu</span>
          </div>
        </div>
        <div className="flex-none w-40 p-4 rounded-xl bg-card-dark border border-slate-800">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Daily Scans</p>
          <div className="flex items-end justify-between">
            <span className="text-2xl font-bold text-white">128</span>
            <span className="material-icons text-primary text-xl">qr_code_scanner</span>
          </div>
        </div>
        <div className="flex-none w-40 p-4 rounded-xl border border-danger/20 bg-danger/5">
          <p className="text-xs font-semibold text-danger/80 uppercase tracking-wider mb-1">Active Alerts</p>
          <div className="flex items-end justify-between">
            <span className="text-2xl font-bold text-danger">02</span>
            <span className="material-icons text-danger text-xl">error_outline</span>
          </div>
        </div>
      </div>

      {/* Inventory */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold text-white">Menu Inventory</h2>
        <button className="text-primary text-sm font-semibold">View All</button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {[
          { title: 'Quinoa Summer Salad', tags: ['GLUTEN-FREE', 'NUT-FREE', 'VEGAN'], img: 'sal1', status: 'Verified' },
          { title: 'Angus Classic Burger', tags: ['DAIRY ALERT', 'NUT-FREE'], img: 'bur1', alert: true },
          { title: 'Harvest Power Bowl', tags: ['NUT-FREE', 'VEGAN'], img: 'bow1', status: 'Verified' },
          { title: 'Margherita Pizza', tags: ['DAIRY ALERT', 'NUT-FREE'], img: 'piz1', out: true }
        ].map((dish, i) => (
          <div key={i} className={`bg-card-dark rounded-xl overflow-hidden flex shadow-sm border border-slate-800 ${dish.out ? 'opacity-60' : ''}`}>
            <div className={`w-28 h-28 flex-none relative ${dish.out ? 'grayscale' : ''}`}>
              <img className="w-full h-full object-cover" src={`https://picsum.photos/seed/${dish.img}/200/200`} alt={dish.title} />
              {dish.status && <div className="absolute top-2 left-2 bg-primary text-background-dark text-[8px] font-bold px-1.5 py-0.5 rounded-full uppercase">{dish.status}</div>}
            </div>
            <div className="p-4 flex flex-col justify-between flex-grow">
              <div>
                <div className="flex justify-between">
                  <h3 className="font-bold text-sm text-white">{dish.title}</h3>
                  {dish.alert && <span className="material-icons text-danger text-sm">warning</span>}
                  {dish.out && <span className="text-[8px] bg-slate-500 text-white px-1.5 py-0.5 rounded">OUT OF STOCK</span>}
                </div>
                <p className="text-[10px] text-slate-500 mt-1 line-clamp-1 italic">Fresh ingredients, daily prep.</p>
              </div>
              <div className="flex flex-wrap gap-1 mt-2">
                {dish.tags.map(t => (
                  <span key={t} className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${t.includes('ALERT') ? 'bg-danger/20 text-danger' : 'bg-primary/20 text-primary'}`}>{t}</span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* FAB */}
      <button onClick={onScan} className="fixed right-6 bottom-24 w-14 h-14 bg-primary text-background-dark rounded-full shadow-lg flex items-center justify-center transition-transform active:scale-90 z-20">
        <span className="material-icons text-3xl font-bold">qr_code_scanner</span>
      </button>

      {/* Tab Bar */}
      <nav className="fixed bottom-0 left-0 right-0 h-20 bg-card-dark/80 backdrop-blur-xl border-t border-slate-800 px-6 flex items-center justify-between z-10 max-w-md mx-auto">
        <button className="flex flex-col items-center gap-1 text-primary">
          <span className="material-icons">grid_view</span>
          <span className="text-[10px] font-bold">Home</span>
        </button>
        <button className="flex flex-col items-center gap-1 text-slate-500">
          <span className="material-icons">inventory_2</span>
          <span className="text-[10px] font-medium">Menu</span>
        </button>
        <div className="w-8"></div>
        <button className="flex flex-col items-center gap-1 text-slate-500">
          <span className="material-icons">notifications_active</span>
          <span className="text-[10px] font-medium">Alerts</span>
        </button>
        <button className="flex flex-col items-center gap-1 text-slate-500">
          <span className="material-icons">insights</span>
          <span className="text-[10px] font-medium">Analytics</span>
        </button>
      </nav>
    </div>
  );
};

export default DashboardPage;
