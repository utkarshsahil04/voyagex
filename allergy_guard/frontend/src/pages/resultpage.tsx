import React from 'react';
import { DishReport } from '../types';
import AllergenBadge from '../components/allergen-badge';

interface Props {
  report: DishReport | null;
  onBack: () => void;
  onScanAgain: () => void;
}

const ResultPage: React.FC<Props> = ({ report, onBack, onScanAgain }) => {
  if (!report) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="text-center">
          <span className="material-icons text-6xl text-slate-600 mb-4">error_outline</span>
          <p className="text-slate-400">No scan data available</p>
          <button onClick={onBack} className="mt-6 bg-primary text-background-dark px-6 py-3 rounded-xl font-bold">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'HIGH':
        return 'bg-danger/20 text-danger border-danger/30';
      case 'MEDIUM':
        return 'bg-warning/20 text-warning border-warning/30';
      case 'LOW':
        return 'bg-primary/20 text-primary border-primary/30';
      default:
        return 'bg-slate-500/20 text-slate-400';
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'HIGH':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'check_circle';
      default:
        return 'info';
    }
  };

  return (
    <div className="min-h-screen bg-background-dark pb-24">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-background-dark/95 backdrop-blur-xl border-b border-slate-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <button
            onClick={onBack}
            className="w-10 h-10 rounded-full bg-card-dark flex items-center justify-center text-slate-300 hover:text-white transition-colors"
          >
            <span className="material-icons">chevron_left</span>
          </button>
          <div className="flex-1 text-center">
            <h1 className="font-bold text-white">Scan Results</h1>
            <p className="text-[10px] text-slate-500 uppercase tracking-wider">Analysis Complete</p>
          </div>
          <button
            onClick={onScanAgain}
            className="w-10 h-10 rounded-full bg-card-dark flex items-center justify-center text-slate-300 hover:text-white transition-colors"
          >
            <span className="material-icons">qr_code_scanner</span>
          </button>
        </div>
      </header>

      <main className="px-6 py-8 space-y-6">
        {/* Dish Info */}
        <div className="bg-card-dark rounded-3xl p-6 border border-slate-800">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">{report.dishName}</h2>
              {report.restaurant && <p className="text-sm text-slate-400">📍 {report.restaurant}</p>}
            </div>
            <div
              className={`px-4 py-2 rounded-full border font-bold text-sm uppercase tracking-wide ${getRiskColor(
                report.riskLevel
              )}`}
            >
              <div className="flex items-center gap-2">
                <span className="material-icons text-base">{getRiskIcon(report.riskLevel)}</span>
                {report.riskLevel}
              </div>
            </div>
          </div>

          {/* Dietary Flags */}
          <div className="flex flex-wrap gap-2 pt-4 border-t border-slate-800">
            {[
              { label: 'Vegetarian', value: report.isVegetarian, icon: 'eco' },
              { label: 'Vegan', value: report.isVegan, icon: 'spa' },
              { label: 'Gluten-Free', value: report.isGlutenFree, icon: 'grain' },
              { label: 'Dairy-Free', value: report.isDairyFree, icon: 'water_drop' },
              { label: 'Nut-Free', value: report.isNutFree, icon: 'nature' },
            ].map((flag) => (
              <div
                key={flag.label}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold ${
                  flag.value ? 'bg-primary/10 text-primary' : 'bg-slate-800 text-slate-500'
                }`}
              >
                <span className="material-icons text-sm">{flag.icon}</span>
                {flag.label}
              </div>
            ))}
          </div>
        </div>

        {/* Allergen Alerts */}
        {report.allergens.length > 0 ? (
          <div className="bg-danger/5 border border-danger/20 rounded-3xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-danger/20 rounded-full flex items-center justify-center">
                <span className="material-icons text-danger">warning</span>
              </div>
              <div>
                <h3 className="font-bold text-white text-lg">Allergen Warning</h3>
                <p className="text-xs text-slate-400">Contains {report.allergens.length} allergen(s)</p>
              </div>
            </div>
            <div className="space-y-3">
              {report.allergens.map((allergen, idx) => (
                <div key={idx} className="bg-background-dark/50 rounded-xl p-4">
                  <div className="flex items-start justify-between mb-2">
                    <AllergenBadge allergen={allergen} size="md" />
                  </div>
                  {allergen.description && <p className="text-xs text-slate-400 mt-2">{allergen.description}</p>}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="bg-primary/5 border border-primary/20 rounded-3xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="material-icons text-primary">check_circle</span>
              </div>
              <div>
                <h3 className="font-bold text-white text-lg">All Clear!</h3>
                <p className="text-xs text-slate-400">No major allergens detected</p>
              </div>
            </div>
          </div>
        )}

        {/* Safe Allergens */}
        {report.safeAllergens && report.safeAllergens.length > 0 && (
          <div className="bg-card-dark rounded-3xl p-6 border border-slate-800">
            <h3 className="font-bold text-white mb-3 flex items-center gap-2">
              <span className="material-icons text-primary text-sm">verified</span>
              Safe (Not Detected)
            </h3>
            <div className="flex flex-wrap gap-2">
              {report.safeAllergens.map((allergen) => (
                <span key={allergen} className="px-3 py-1.5 bg-slate-800 text-slate-300 rounded-lg text-xs font-semibold">
                  {allergen}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Ingredients */}
        <div className="bg-card-dark rounded-3xl p-6 border border-slate-800">
          <h3 className="font-bold text-white mb-3 flex items-center gap-2">
            <span className="material-icons text-primary text-sm">restaurant</span>
            Ingredients
          </h3>
          <div className="flex flex-wrap gap-2">
            {report.ingredients.map((ingredient, idx) => (
              <span key={idx} className="px-3 py-1.5 bg-slate-800 text-slate-300 rounded-lg text-xs">
                {ingredient}
              </span>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        {report.recommendations && report.recommendations.length > 0 && (
          <div className="bg-card-dark rounded-3xl p-6 border border-slate-800">
            <h3 className="font-bold text-white mb-3 flex items-center gap-2">
              <span className="material-icons text-primary text-sm">lightbulb</span>
              Recommendations
            </h3>
            <ul className="space-y-2">
              {report.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="material-icons text-primary text-sm mt-0.5">check</span>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Scan Time */}
        {report.scanTime && (
          <div className="text-center text-xs text-slate-500">
            Scanned at {new Date(report.scanTime).toLocaleString()}
          </div>
        )}
      </main>

      {/* Actions */}
      <div className="fixed bottom-0 left-0 right-0 bg-background-dark/95 backdrop-blur-xl border-t border-slate-800 p-6 max-w-md mx-auto">
        <div className="flex gap-3">
          <button
            onClick={onBack}
            className="flex-1 bg-slate-800 hover:bg-slate-700 text-white font-semibold py-4 rounded-xl transition-colors"
          >
            Dashboard
          </button>
          <button
            onClick={onScanAgain}
            className="flex-1 bg-primary hover:bg-primary/90 text-background-dark font-bold py-4 rounded-xl transition-colors flex items-center justify-center gap-2"
          >
            <span className="material-icons">qr_code_scanner</span>
            Scan Again
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;