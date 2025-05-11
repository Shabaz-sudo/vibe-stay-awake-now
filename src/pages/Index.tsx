
import React, { useState, useEffect } from "react";
import { CursorVibeProvider, useCursorVibe } from "../context/CursorVibeContext";
import WindowFrame from "../components/WindowFrame";
import Taskbar from "../components/Taskbar";
import Settings from "../components/Settings";
import SimulationStatus from "../components/SimulationStatus";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MousePointerClick, Settings as SettingsIcon } from "lucide-react";

// Mouse activity tracker component
const ActivityTracker: React.FC = () => {
  const { updateLastActivity } = useCursorVibe();
  
  useEffect(() => {
    const handleMouseMove = () => {
      updateLastActivity();
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mousedown', handleMouseMove);
    window.addEventListener('keydown', handleMouseMove);
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mousedown', handleMouseMove);
      window.removeEventListener('keydown', handleMouseMove);
    };
  }, [updateLastActivity]);
  
  return null;
};

// Main application component
const CursorVibeApp: React.FC = () => {
  const [activeTab, setActiveTab] = useState("status");
  
  const showSettings = () => {
    setActiveTab("settings");
  };
  
  return (
    <div className="min-h-screen bg-cv-gray-100 flex flex-col items-center justify-center relative">
      <ActivityTracker />
      
      <div className="flex-1 flex items-center justify-center p-4">
        <WindowFrame title="CursorVibe - Prevent System Sleep">
          <div className="text-center mb-4">
            <h1 className="text-xl font-bold text-cv-gray-800">CursorVibe</h1>
            <p className="text-sm text-cv-gray-600">Keep your workflow alive</p>
          </div>
          
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid grid-cols-2">
              <TabsTrigger value="status" className="flex items-center">
                <MousePointerClick size={16} className="mr-2" />
                Status
              </TabsTrigger>
              <TabsTrigger value="settings" className="flex items-center">
                <SettingsIcon size={16} className="mr-2" />
                Settings
              </TabsTrigger>
            </TabsList>
            <TabsContent value="status">
              <SimulationStatus />
            </TabsContent>
            <TabsContent value="settings">
              <Settings />
            </TabsContent>
          </Tabs>
          
          <p className="text-xs text-cv-gray-500 mt-6 text-center">
            Note: This is a web simulation of a desktop app.
            <br />In a real desktop app, this would control the actual system cursor.
          </p>
        </WindowFrame>
      </div>
      
      <Taskbar showSettings={showSettings} />
    </div>
  );
};

// Wrap the app with our context provider
const Index = () => {
  return (
    <CursorVibeProvider>
      <CursorVibeApp />
    </CursorVibeProvider>
  );
};

export default Index;
