import React, { useState } from 'react';
import LandingPage from './pages/landing';
import DashboardPage from './pages/dashboard';
import ScanPage from './pages/scanboard';
import ResultPage from './pages/resultpage';
import { Page, DishReport } from './types';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>(Page.LANDING);
  const [currentDish, setCurrentDish] = useState<DishReport | null>(null);

  const navigateTo = (page: Page) => {
    setCurrentPage(page);
    window.scrollTo(0, 0);
  };

  const showResult = (report: DishReport) => {
    setCurrentDish(report);
    setCurrentPage(Page.RESULT);
  };

  const renderPage = () => {
    switch (currentPage) {
      case Page.LANDING:
        return <LandingPage onStart={() => navigateTo(Page.DASHBOARD)} />;
      case Page.DASHBOARD:
        return <DashboardPage onScan={() => navigateTo(Page.SCAN)} onNavigateHome={() => navigateTo(Page.LANDING)} />;
      case Page.SCAN:
        return <ScanPage onBack={() => navigateTo(Page.DASHBOARD)} onResult={showResult} />;
      case Page.RESULT:
        return <ResultPage report={currentDish} onBack={() => navigateTo(Page.DASHBOARD)} onScanAgain={() => navigateTo(Page.SCAN)} />;
      default:
        return <LandingPage onStart={() => navigateTo(Page.DASHBOARD)} />;
    }
  };

  return (
    <div className="max-w-md mx-auto min-h-screen relative shadow-2xl bg-background-dark overflow-x-hidden">
      {renderPage()}
    </div>
  );
};

export default App;