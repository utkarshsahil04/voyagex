import React from 'react';
import DishCard from '../components/Dishcard';

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
        <DishCard
          title="Quinoa Summer Salad"
          tags={['GLUTEN-FREE', 'NUT-FREE', 'VEGAN']}
          img="sal1"
          status="Verified"
        />
        <DishCard
          title="Angus Classic Burger"
          tags={['DAIRY ALERT', 'NUT-FREE']}
          img="bur1"
          alert={true}
        />
        <DishCard
          title="Harvest Power Bowl"
          tags={['NUT-FREE', 'VEGAN']}
          img="bow1"
          status="Verified"
        />
        <DishCard
          title="Margherita Pizza"
          tags={['DAIRY ALERT', 'NUT-FREE']}
          img="piz1"
          out={true}
        />
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