import React from 'react';
import { QRCodeData } from '../types';

interface Props {
  qrData: QRCodeData;
  onClose?: () => void;
}

const QRCodeDisplay: React.FC<Props> = ({ qrData, onClose }) => {
  const handleDownload = () => {
    if (qrData.imageUrl) {
      window.open(qrData.imageUrl, '_blank');
    }
  };

  const handleCopyUrl = () => {
    navigator.clipboard.writeText(qrData.scanUrl);
    alert('QR scan URL copied to clipboard!');
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-6">
      <div className="bg-card-dark rounded-3xl max-w-sm w-full p-8 relative border border-slate-700">
        {onClose && (
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
          >
            <span className="material-icons text-xl">close</span>
          </button>
        )}

        <div className="text-center mb-6">
          <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-3">
            <span className="material-icons text-primary text-2xl">qr_code</span>
          </div>
          <h3 className="text-xl font-bold text-white">QR Code Ready!</h3>
          <p className="text-slate-400 text-sm mt-1">Scan to view allergen information</p>
        </div>

        <div className="bg-white p-6 rounded-2xl mb-6">
          {qrData.imageUrl ? (
            <img src={qrData.imageUrl} alt="QR Code" className="w-full h-auto" />
          ) : (
            <div className="aspect-square flex items-center justify-center text-slate-400">
              <div className="text-center">
                <span className="material-icons text-6xl mb-2">qr_code_2</span>
                <p className="text-sm">QR Code Preview</p>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-3">
          <button
            onClick={handleDownload}
            className="w-full bg-primary hover:bg-primary/90 text-background-dark font-bold py-3 rounded-xl transition-colors"
          >
            Download QR Code
          </button>
          <button
            onClick={handleCopyUrl}
            className="w-full bg-slate-800 hover:bg-slate-700 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
          >
            <span className="material-icons text-sm">link</span>
            Copy Scan URL
          </button>
        </div>

        <div className="mt-6 p-4 bg-slate-900/50 rounded-xl border border-slate-800">
          <p className="text-[10px] text-slate-500 text-center">
            Token: <span className="text-slate-300 font-mono">{qrData.token.slice(0, 16)}...</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default QRCodeDisplay;