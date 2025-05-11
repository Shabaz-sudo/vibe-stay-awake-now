
import React from 'react';
import { Minus, X, Square, Maximize2 } from 'lucide-react';

interface WindowFrameProps {
  title: string;
  children: React.ReactNode;
}

const WindowFrame: React.FC<WindowFrameProps> = ({ title, children }) => {
  return (
    <div className="flex flex-col border border-cv-gray-300 rounded-lg shadow-lg overflow-hidden w-full max-w-md">
      {/* Title bar */}
      <div className="flex items-center p-2 bg-cv-gray-100 border-b border-cv-gray-300">
        <div className="flex space-x-2 mr-2">
          <div className="w-3 h-3 rounded-full bg-cv-danger"></div>
          <div className="w-3 h-3 rounded-full bg-cv-warning"></div>
          <div className="w-3 h-3 rounded-full bg-cv-success"></div>
        </div>
        <div className="flex-1 text-center text-sm font-medium text-cv-gray-800">{title}</div>
        <div className="flex space-x-3">
          <button className="text-cv-gray-500 hover:text-cv-gray-700">
            <Minus size={14} />
          </button>
          <button className="text-cv-gray-500 hover:text-cv-gray-700">
            <Square size={14} />
          </button>
          <button className="text-cv-gray-500 hover:text-cv-danger">
            <X size={14} />
          </button>
        </div>
      </div>
      
      {/* Window content */}
      <div className="p-4 bg-white">
        {children}
      </div>
    </div>
  );
};

export default WindowFrame;
