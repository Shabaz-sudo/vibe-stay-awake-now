
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { toast } from 'sonner';

interface CursorVibeContextType {
  isRunning: boolean;
  frequency: number;
  movementDistance: number;
  idleThreshold: number;
  runOnStartup: boolean;
  toggleRunning: () => void;
  setFrequency: (value: number) => void;
  setMovementDistance: (value: number) => void;
  setIdleThreshold: (value: number) => void;
  toggleRunOnStartup: () => void;
  lastActivity: number;
  updateLastActivity: () => void;
}

const CursorVibeContext = createContext<CursorVibeContextType | null>(null);

// Default values
const DEFAULT_FREQUENCY = 1.0;
const DEFAULT_MOVEMENT_DISTANCE = 3;
const DEFAULT_IDLE_THRESHOLD = 3;
const DEFAULT_RUN_ON_STARTUP = false;

export const CursorVibeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [frequency, setFrequency] = useState(DEFAULT_FREQUENCY);
  const [movementDistance, setMovementDistance] = useState(DEFAULT_MOVEMENT_DISTANCE);
  const [idleThreshold, setIdleThreshold] = useState(DEFAULT_IDLE_THRESHOLD);
  const [runOnStartup, setRunOnStartup] = useState(DEFAULT_RUN_ON_STARTUP);
  const [lastActivity, setLastActivity] = useState(Date.now());

  // Load settings from localStorage on mount
  useEffect(() => {
    try {
      const savedSettings = localStorage.getItem('cursorVibeSettings');
      if (savedSettings) {
        const parsedSettings = JSON.parse(savedSettings);
        setFrequency(parsedSettings.frequency || DEFAULT_FREQUENCY);
        setMovementDistance(parsedSettings.movementDistance || DEFAULT_MOVEMENT_DISTANCE);
        setIdleThreshold(parsedSettings.idleThreshold || DEFAULT_IDLE_THRESHOLD);
        setRunOnStartup(parsedSettings.runOnStartup || DEFAULT_RUN_ON_STARTUP);
      }
    } catch (error) {
      console.error("Error loading settings:", error);
      toast.error("Failed to load settings");
    }
  }, []);

  // Save settings to localStorage whenever they change
  useEffect(() => {
    try {
      const settings = {
        frequency,
        movementDistance,
        idleThreshold,
        runOnStartup
      };
      localStorage.setItem('cursorVibeSettings', JSON.stringify(settings));
    } catch (error) {
      console.error("Error saving settings:", error);
    }
  }, [frequency, movementDistance, idleThreshold, runOnStartup]);

  const toggleRunning = useCallback(() => {
    setIsRunning(prev => !prev);
    if (!isRunning) {
      toast.success("CursorVibe is now active!");
    } else {
      toast.info("CursorVibe has been stopped");
    }
  }, [isRunning]);

  const updateLastActivity = useCallback(() => {
    setLastActivity(Date.now());
  }, []);

  const toggleRunOnStartup = useCallback(() => {
    setRunOnStartup(prev => !prev);
  }, []);

  const value = {
    isRunning,
    frequency,
    movementDistance,
    idleThreshold,
    runOnStartup,
    toggleRunning,
    setFrequency,
    setMovementDistance,
    setIdleThreshold,
    toggleRunOnStartup,
    lastActivity,
    updateLastActivity,
  };

  return (
    <CursorVibeContext.Provider value={value}>
      {children}
    </CursorVibeContext.Provider>
  );
};

export const useCursorVibe = (): CursorVibeContextType => {
  const context = useContext(CursorVibeContext);
  if (!context) {
    throw new Error('useCursorVibe must be used within a CursorVibeProvider');
  }
  return context;
};
