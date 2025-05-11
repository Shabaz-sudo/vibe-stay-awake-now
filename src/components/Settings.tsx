
import React from 'react';
import { useCursorVibe } from '../context/CursorVibeContext';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';

const Settings: React.FC = () => {
  const { 
    frequency, 
    movementDistance, 
    idleThreshold,
    runOnStartup,
    setFrequency,
    setMovementDistance,
    setIdleThreshold,
    toggleRunOnStartup
  } = useCursorVibe();

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <Label htmlFor="frequency">Check Frequency (seconds)</Label>
          <span className="text-sm text-cv-gray-600">{frequency.toFixed(1)}s</span>
        </div>
        <Slider 
          id="frequency"
          min={0.1}
          max={3.0}
          step={0.1}
          value={[frequency]}
          onValueChange={(vals) => setFrequency(vals[0])}
        />
        <p className="text-xs text-cv-gray-500">How often CursorVibe checks if movement is needed</p>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <Label htmlFor="distance">Movement Distance (pixels)</Label>
          <span className="text-sm text-cv-gray-600">{movementDistance}px</span>
        </div>
        <Slider 
          id="distance"
          min={1}
          max={10}
          step={1}
          value={[movementDistance]}
          onValueChange={(vals) => setMovementDistance(vals[0])}
        />
        <p className="text-xs text-cv-gray-500">How far the cursor moves each time</p>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <Label htmlFor="idle">Idle Threshold (seconds)</Label>
          <span className="text-sm text-cv-gray-600">{idleThreshold}s</span>
        </div>
        <Slider 
          id="idle"
          min={1}
          max={10}
          step={1}
          value={[idleThreshold]}
          onValueChange={(vals) => setIdleThreshold(vals[0])}
        />
        <p className="text-xs text-cv-gray-500">Seconds of inactivity before cursor movement begins</p>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-cv-gray-200">
        <div>
          <Label htmlFor="startup" className="text-sm font-medium">Run on Startup</Label>
          <p className="text-xs text-cv-gray-500">Start automatically when you log in</p>
        </div>
        <Switch 
          id="startup" 
          checked={runOnStartup}
          onCheckedChange={toggleRunOnStartup}
        />
      </div>
    </div>
  );
};

export default Settings;
