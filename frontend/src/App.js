import React, { useState, useEffect } from 'react';
import './App.css';
import { 
  Toolbar, 
  SpreadsheetToolbar, 
  WelcomeModal, 
  Chat, 
  Spreadsheet, 
  FileUpload, 
  StatusBar 
} from './components';

function App() {
  const [showWelcome, setShowWelcome] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [currentFile, setCurrentFile] = useState(null);
  const [spreadsheetData, setSpreadsheetData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load sample data on component mount
  useEffect(() => {
    loadSampleData();
  }, []);

  const loadSampleData = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/sample-data`);
      if (response.ok) {
        const result = await response.json();
        setSpreadsheetData(result.data);
      }
    } catch (error) {
      console.error('Error loading sample data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenFile = () => {
    document.getElementById('fileInput').click();
  };

  const handleFileUpload = async (file) => {
    setCurrentFile(file);
    setIsLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/upload-excel`, {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        setSpreadsheetData(result.data);
        console.log('File uploaded successfully:', result);
      } else {
        console.error('Failed to upload file');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewFile = async () => {
    setCurrentFile(null);
    setIsLoading(true);
    await loadSampleData();
    console.log('New file created');
  };

  const handleSaveFile = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/export-excel`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'sheetgenie_export.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        console.log('File saved successfully');
      }
    } catch (error) {
      console.error('Error saving file:', error);
    }
  };

  const handleSettings = () => {
    console.log('Settings opened');
  };

  const handleSecurity = () => {
    console.log('Security settings opened');
  };

  const handleNewChat = () => {
    setShowChat(true);
  };

  const handleDataUpdate = async (newData) => {
    // Update spreadsheet data from AI responses
    setSpreadsheetData(newData);
    
    // Send updated data to backend
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/set-spreadsheet-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: newData
        })
      });
    } catch (error) {
      console.error('Error updating spreadsheet data:', error);
    }
  };

  const handleSpreadsheetChange = (data) => {
    setSpreadsheetData(data);
  };

  return (
    <div className="App h-screen flex flex-col bg-gray-100">
      {/* Hidden file input */}
      <input
        id="fileInput"
        type="file"
        accept=".xlsx,.xls"
        onChange={(e) => handleFileUpload(e.target.files[0])}
        className="hidden"
      />

      {/* Top Toolbar */}
      <Toolbar
        onOpenFile={handleOpenFile}
        onNewFile={handleNewFile}
        onSaveFile={handleSaveFile}
        onSettings={handleSettings}
        onSecurity={handleSecurity}
      />

      {/* Spreadsheet Toolbar */}
      <SpreadsheetToolbar onNewChat={handleNewChat} />

      {/* Main Content Area */}
      <div className="flex-1 flex">
        {/* Left Content Area */}
        <div className="flex-1 flex flex-col">
          {/* File Upload Section */}
          {!currentFile && (
            <div className="p-4">
              <FileUpload onFileUpload={handleFileUpload} />
            </div>
          )}

          {/* Hero Section with Background */}
          <div className="relative p-8 bg-gradient-to-r from-blue-50 to-indigo-50">
            <div 
              className="absolute inset-0 opacity-10"
              style={{
                backgroundImage: 'url(https://images.unsplash.com/photo-1581094289810-adf5d25690e3)',
                backgroundSize: 'cover',
                backgroundPosition: 'center'
              }}
            />
            <div className="relative z-10 max-w-2xl">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Welcome to SheetGenie
              </h1>
              <p className="text-lg text-gray-600 mb-6">
                Your AI-powered Excel assistant that automates spreadsheet tasks, creates formulas, 
                generates charts, and provides data insights through natural language conversations.
              </p>
              <div className="flex space-x-4">
                <button 
                  onClick={() => setShowWelcome(true)}
                  className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Get Started
                </button>
                <button 
                  onClick={() => setShowChat(true)}
                  className="px-6 py-3 border border-green-600 text-green-600 rounded-lg hover:bg-green-50 transition-colors"
                >
                  Try Chat Assistant
                </button>
              </div>
            </div>
          </div>

          {/* Features Section */}
          <div className="p-8 bg-white">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Key Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4">
                <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-full flex items-center justify-center">
                  <img 
                    src="https://images.pexels.com/photos/8532850/pexels-photo-8532850.jpeg" 
                    alt="AI Assistant" 
                    className="w-full h-full object-cover rounded-full"
                  />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Assistant</h3>
                <p className="text-gray-600">Chat with our AI to get formulas, analysis, and insights</p>
              </div>
              <div className="text-center p-4">
                <div className="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
                  <img 
                    src="https://images.pexels.com/photos/16053029/pexels-photo-16053029.jpeg" 
                    alt="Smart Automation" 
                    className="w-full h-full object-cover rounded-full"
                  />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Automation</h3>
                <p className="text-gray-600">Automate repetitive tasks with intelligent suggestions</p>
              </div>
              <div className="text-center p-4">
                <div className="w-16 h-16 mx-auto mb-4 bg-indigo-100 rounded-full flex items-center justify-center">
                  <img 
                    src="https://images.unsplash.com/photo-1545063328-c8e3faffa16f" 
                    alt="Data Visualization" 
                    className="w-full h-full object-cover rounded-full"
                  />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Data Visualization</h3>
                <p className="text-gray-600">Create beautiful charts and dashboards instantly</p>
              </div>
            </div>
          </div>

          {/* Spreadsheet Component */}
          <Spreadsheet />
        </div>

        {/* Chat Panel */}
        <Chat isOpen={showChat} onClose={() => setShowChat(false)} />
      </div>

      {/* Bottom Status Bar */}
      <StatusBar />

      {/* Welcome Modal */}
      <WelcomeModal
        isOpen={showWelcome}
        onClose={() => setShowWelcome(false)}
      />
    </div>
  );
}

export default App;