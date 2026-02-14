import React from 'react';

interface DishCardProps {
  title: string;
  tags: string[];
  img: string;
  status?: string;
  alert?: boolean;
  out?: boolean;
  onGenerateQR?: () => void;
}

const DishCard: React.FC<DishCardProps> = ({ title, tags, img, status, alert, out, onGenerateQR }) => {
  return (
    <div className={`bg-card-dark rounded-xl overflow-hidden flex shadow-sm border border-slate-800 ${out ? 'opacity-60' : ''}`}>
      <div className={`w-28 h-28 flex-none relative ${out ? 'grayscale' : ''}`}>
        <img className="w-full h-full object-cover" src={`https://picsum.photos/seed/${img}/200/200`} alt={title} />
        {status && (
          <div className="absolute top-2 left-2 bg-primary text-background-dark text-[8px] font-bold px-1.5 py-0.5 rounded-full uppercase">
            {status}
          </div>
        )}
      </div>
      <div className="p-4 flex flex-col justify-between flex-grow">
        <div>
          <div className="flex justify-between items-start">
            <h3 className="font-bold text-sm text-white">{title}</h3>
            {alert && <span className="material-icons text-danger text-sm">warning</span>}
            {out && <span className="text-[8px] bg-slate-500 text-white px-1.5 py-0.5 rounded">OUT OF STOCK</span>}
          </div>
          <p className="text-[10px] text-slate-500 mt-1 line-clamp-1 italic">Fresh ingredients, daily prep.</p>
        </div>
        <div className="flex flex-wrap gap-1 mt-2">
          {tags.map((t) => (
            <span
              key={t}
              className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${
                t.includes('ALERT') ? 'bg-danger/20 text-danger' : 'bg-primary/20 text-primary'
              }`}
            >
              {t}
            </span>
          ))}
        </div>
        {onGenerateQR && !out && (
          <button
            onClick={onGenerateQR}
            className="mt-3 text-xs bg-primary/10 hover:bg-primary/20 text-primary font-semibold py-1.5 px-3 rounded-lg transition-colors"
          >
            Generate QR
          </button>
        )}
      </div>
    </div>
  );
};

export default DishCard;