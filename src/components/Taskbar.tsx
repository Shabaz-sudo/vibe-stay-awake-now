
import React from 'react';
import { useCursorVibe } from '../context/CursorVibeContext';
import { MousePointerClick, Settings, Power } from 'lucide-react';
import { 
  Popover, 
  PopoverContent, 
  PopoverTrigger 
} from '@/components/ui/popover';
import { toast } from 'sonner';

interface TaskbarProps {
  showSettings: () => void;
}

const Taskbar: React.FC<TaskbarProps> = ({ showSettings }) => {
  const { isRunning, toggleRunning } = useCursorVibe();
  
  const handleQuit = () => {
    toast.info("In a real desktop app, this would close the application");
  };
  
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-cv-gray-200 border-t border-cv-gray-300 h-12 flex items-center px-4">
      {/* Start button */}
      <div className="flex-1 flex items-center">
        <button className="w-8 h-8 bg-cv-primary rounded-full flex items-center justify-center text-white">
          <MousePointerClick size={18} />
        </button>
      </div>
      
      {/* System tray */}
      <div className="flex items-center space-x-4 pr-2">
        <Popover>
          <PopoverTrigger asChild>
            <button className="relative flex items-center justify-center">
              <MousePointerClick 
                size={20} 
                className={isRunning ? "text-cv-primary animate-cursor-move" : "text-cv-gray-600"}
              />
              {isRunning && (
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-cv-success rounded-full"></span>
              )}
            </button>
          </PopoverTrigger>
          <PopoverContent className="w-60 p-0" side="top">
            <div className="p-2 border-b border-cv-gray-200">
              <p className="font-medium text-sm">CursorVibe</p>
              <p className="text-xs text-cv-gray-600">Keep your workflow alive</p>
            </div>
            <div className="p-2 space-y-2">
              <button 
                onClick={toggleRunning} 
                className="w-full text-left px-3 py-2 text-sm hover:bg-cv-gray-100 rounded-md flex items-center"
              >
                <span className={`w-2 h-2 rounded-full mr-2 ${isRunning ? 'bg-cv-success' : 'bg-cv-danger'}`}></span>
                {isRunning ? 'Stop CursorVibe' : 'Start CursorVibe'}
              </button>
              <button 
                onClick={showSettings} 
                className="w-full text-left px-3 py-2 text-sm hover:bg-cv-gray-100 rounded-md flex items-center"
              >
                <Settings size={14} className="mr-2" />
                Settings
              </button>
              <button 
                onClick={handleQuit} 
                className="w-full text-left px-3 py-2 text-sm hover:bg-cv-gray-100 rounded-md flex items-center text-cv-danger"
              >
                <Power size={14} className="mr-2" />
                Quit CursorVibe
              </button>
            </div>
          </PopoverContent>
        </Popover>
        
        {/* Show time */}
        <div className="text-xs text-cv-gray-800">
          {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
        </div>
      </div>
    </div>
  );
};

export default Taskbar;
