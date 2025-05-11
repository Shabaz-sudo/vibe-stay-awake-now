
import React, { useState, useEffect } from 'react';
import { useCursorVibe } from '../context/CursorVibeContext';
import { simulateCursorMovement, isUserIdle } from '../utils/cursorUtils';
import { Button } from '@/components/ui/button';
import { MousePointerClick, MousePointerSquareDashed } from 'lucide-react';

const SimulationStatus: React.FC = () => {
  const { 
    isRunning, 
    toggleRunning, 
    frequency,
    movementDistance,
    idleThreshold,
    lastActivity,
  } = useCursorVibe();
  
  const [simulationCount, setSimulationCount] = useState(0);
  const [idle, setIdle] = useState(false);

  // Check idle status and potentially move cursor on interval
  useEffect(() => {
    if (!isRunning) return;

    const checkIdleAndSimulate = () => {
      const userIsIdle = isUserIdle(lastActivity, idleThreshold);
      setIdle(userIsIdle);
      
      if (userIsIdle) {
        simulateCursorMovement(movementDistance);
        setSimulationCount(prev => prev + 1);
      }
    };

    const interval = setInterval(checkIdleAndSimulate, frequency * 1000);
    return () => clearInterval(interval);
  }, [isRunning, lastActivity, idleThreshold, frequency, movementDistance]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col items-center justify-center py-6">
        <div 
          className={`w-24 h-24 rounded-full flex items-center justify-center mb-4 transition-all duration-300 ${
            isRunning ? 'bg-cv-primary text-white' : 'bg-cv-gray-200 text-cv-gray-600'
          }`}
        >
          {isRunning ? (
            <MousePointerClick size={40} className="animate-cursor-move" />
          ) : (
            <MousePointerSquareDashed size={40} />
          )}
        </div>
        
        <Button 
          onClick={toggleRunning}
          className={`w-48 ${isRunning ? 'bg-cv-danger hover:bg-red-600' : 'bg-cv-primary hover:bg-blue-600'}`}
        >
          {isRunning ? 'Hold the Mouse Back' : 'Go, Mouse, Go!'}
        </Button>
      </div>

      {isRunning && (
        <div className="bg-cv-gray-100 rounded-lg p-4">
          <h3 className="text-sm font-medium mb-2">Current Status</h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="text-cv-gray-600">State:</div>
            <div className="font-medium">{idle ? 'Idle (Moving)' : 'Active (Waiting)'}</div>
            
            <div className="text-cv-gray-600">Frequency:</div>
            <div className="font-medium">{frequency.toFixed(1)}s</div>
            
            <div className="text-cv-gray-600">Distance:</div>
            <div className="font-medium">{movementDistance}px</div>
            
            <div className="text-cv-gray-600">Movements:</div>
            <div className="font-medium">{simulationCount}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SimulationStatus;
