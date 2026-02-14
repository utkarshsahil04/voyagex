import React from 'react';
import { Allergen } from '../types';

interface Props {
  allergen: Allergen;
  size?: 'sm' | 'md' | 'lg';
}

const AllergenBadge: React.FC<Props> = ({ allergen, size = 'md' }) => {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-danger/20 text-danger border-danger/30';
      case 'medium':
        return 'bg-warning/20 text-warning border-warning/30';
      case 'low':
        return 'bg-yellow-500/20 text-yellow-500 border-yellow-500/30';
      default:
        return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'px-2 py-0.5 text-[10px]';
      case 'lg':
        return 'px-4 py-2 text-sm';
      default:
        return 'px-3 py-1 text-xs';
    }
  };

  const getIcon = (name: string) => {
    const lower = name.toLowerCase();
    if (lower.includes('nut') || lower.includes('peanut')) return 'eco';
    if (lower.includes('dairy') || lower.includes('milk')) return 'water_drop';
    if (lower.includes('gluten') || lower.includes('wheat')) return 'grain';
    if (lower.includes('shellfish') || lower.includes('fish')) return 'set_meal';
    if (lower.includes('egg')) return 'egg';
    if (lower.includes('soy')) return 'nature';
    return 'warning';
  };

  return (
    <div
      className={`inline-flex items-center gap-1.5 rounded-full border font-bold uppercase tracking-wide ${getSizeClasses()} ${getSeverityColor(
        allergen.severity
      )}`}
    >
      <span className="material-icons" style={{ fontSize: size === 'sm' ? '12px' : size === 'lg' ? '18px' : '14px' }}>
        {getIcon(allergen.name)}
      </span>
      <span>{allergen.name}</span>
    </div>
  );
};

export default AllergenBadge;