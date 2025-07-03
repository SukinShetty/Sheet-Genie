import React, { useState, useEffect } from 'react';
import { HotTable } from '@handsontable/react';
import { 
  Upload, 
  Download, 
  Settings, 
  Shield, 
  MessageSquare, 
  Send, 
  X, 
  ChevronLeft, 
  ChevronRight,
  Play,
  File,
  FolderOpen,
  Save,
  Home,
  Plus,
  BarChart3,
  Calculator,
  Palette,
  AlignLeft,
  Bold,
  Italic,
  Underline,
  Type,
  Hash,
  Percent
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import 'handsontable/dist/handsontable.full.min.css';

// Sample spreadsheet data
const sampleData = [
  ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total', 'Growth %'],
  ['Laptop Pro', 15000, 18000, 22000, 25000, 80000, 12.5],
  ['Tablet Air', 8000, 9500, 11000, 13500, 42000, 15.2],
  ['Phone Max', 25000, 28000, 32000, 35000, 120000, 8.7],
  ['Watch Series', 5000, 6200, 7500, 9000, 27700, 18.3],
  ['Earbuds Pro', 12000, 14500, 16000, 18500, 61000, 13.1],
  ['', '', '', '', '', '', ''],
  ['Total', 65000, 76200, 88500, 101000, 330700, 13.2],
  ['', '', '', '', '', '', ''],
  ['Analysis', '', '', '', '', '', ''],
  ['Best Quarter', 'Q4', '', '', '', '', ''],
  ['Top Product', 'Phone Max', '', '', '', '', ''],
  ['Avg Growth', '13.6%', '', '', '', '', '']
];

// Chat messages data
const initialMessages = [
  { id: 1, text: "Hello! I'm SheetGenie, your AI assistant for Excel automation. How can I help you today?", sender: 'ai', timestamp: '10:30 AM' },
  { id: 2, text: "I can help you with formulas, data analysis, pivot tables, charts, and much more. Just tell me what you need!", sender: 'ai', timestamp: '10:30 AM' }
];

// Toolbar Component
export const Toolbar = ({ onOpenFile, onNewFile, onSaveFile, onSettings, onSecurity }) => {
  return (
    <div className="bg-gray-50 border-b border-gray-200 px-4 py-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <button 
              onClick={onOpenFile}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded"
            >
              <FolderOpen className="w-4 h-4" />
              <span>Open Xlsx File</span>
            </button>
            <button 
              onClick={onNewFile}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded"
            >
              <File className="w-4 h-4" />
              <span>New File</span>
            </button>
            <button 
              onClick={onSaveFile}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded"
            >
              <Save className="w-4 h-4" />
              <span>Save File</span>
            </button>
          </div>
          <div className="text-gray-400">|</div>
          <div className="flex items-center space-x-2">
            <button 
              onClick={onSettings}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded"
            >
              <Settings className="w-4 h-4" />
              <span>Settings</span>
            </button>
            <button 
              onClick={onSecurity}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded"
            >
              <Shield className="w-4 h-4" />
              <span>Security</span>
            </button>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600">Untitled</span>
        </div>
      </div>
    </div>
  );
};

// Spreadsheet Toolbar Component
export const SpreadsheetToolbar = () => {
  return (
    <div className="bg-white border-b border-gray-200 px-4 py-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded">HOME</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded">INSERT</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded">FORMULAS</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded">DATA</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded">VIEW</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded">SETTINGS</button>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button className="flex items-center space-x-1 px-3 py-1.5 text-sm bg-green-600 text-white rounded hover:bg-green-700">
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
          </button>
        </div>
      </div>
      
      {/* Second row of toolbar */}
      <div className="flex items-center space-x-4 mt-2 border-t border-gray-100 pt-2">
        <div className="flex items-center space-x-2">
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Type className="w-4 h-4" />
          </button>
          <select className="text-sm border-none bg-transparent text-gray-600">
            <option>Fonts</option>
          </select>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Bold className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Italic className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Underline className="w-4 h-4" />
          </button>
        </div>
        <div className="text-gray-300">|</div>
        <div className="flex items-center space-x-2">
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <AlignLeft className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Hash className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Percent className="w-4 h-4" />
          </button>
        </div>
        <div className="text-gray-300">|</div>
        <div className="flex items-center space-x-2">
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <BarChart3 className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Calculator className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded">
            <Palette className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

// Welcome Modal Component
export const WelcomeModal = ({ isOpen, onClose, onNext }) => {
  const [currentStep, setCurrentStep] = useState(1);

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      onClose();
    }
  };

  const handleClose = () => {
    onClose();
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Welcome to SheetGenie</h2>
              <button
                onClick={handleClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="text-center mb-6">
              <div className="flex justify-center mb-2">
                <div className="flex space-x-2">
                  <div className={`w-2 h-2 rounded-full ${currentStep === 1 ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                  <div className={`w-2 h-2 rounded-full ${currentStep === 2 ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                  <div className={`w-2 h-2 rounded-full ${currentStep === 3 ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                </div>
              </div>
              <p className="text-gray-600 mb-4">SheetGenie does your Excel work for you</p>
              
              {currentStep === 1 && (
                <div className="space-y-4">
                  <div className="bg-black rounded-lg h-48 flex items-center justify-center">
                    <img 
                      src="https://images.unsplash.com/photo-1545063328-c8e3faffa16f" 
                      alt="SheetGenie Demo" 
                      className="w-full h-full object-cover rounded-lg"
                    />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Play className="w-12 h-12 text-white opacity-80" />
                    </div>
                  </div>
                  <p className="text-sm text-gray-600">Tell SheetGenie what you need and watch it go</p>
                </div>
              )}
              
              {currentStep === 2 && (
                <div className="space-y-4">
                  <img 
                    src="https://images.pexels.com/photos/8532850/pexels-photo-8532850.jpeg" 
                    alt="AI Assistant" 
                    className="w-full h-48 object-cover rounded-lg"
                  />
                  <p className="text-sm text-gray-600">AI-powered analysis and automation for your spreadsheets</p>
                </div>
              )}
              
              {currentStep === 3 && (
                <div className="space-y-4">
                  <img 
                    src="https://images.pexels.com/photos/16053029/pexels-photo-16053029.jpeg" 
                    alt="Smart Features" 
                    className="w-full h-48 object-cover rounded-lg"
                  />
                  <p className="text-sm text-gray-600">Smart formulas, charts, and data insights at your fingertips</p>
                </div>
              )}
            </div>
            
            <div className="flex justify-between items-center">
              <button
                onClick={handleBack}
                className="flex items-center space-x-1 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50"
                disabled={currentStep === 1}
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
              
              <span className="text-sm text-gray-500">{currentStep} of 3</span>
              
              <button
                onClick={handleNext}
                className="flex items-center space-x-1 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
              >
                <span>{currentStep === 3 ? 'Get Started' : 'Next'}</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// Chat Component
export const Chat = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState(initialMessages);
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      const userMessage = {
        id: messages.length + 1,
        text: newMessage,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages([...messages, userMessage]);
      setNewMessage('');
      
      // Simulate AI response
      setTimeout(() => {
        const aiResponse = {
          id: messages.length + 2,
          text: getAIResponse(newMessage),
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, aiResponse]);
      }, 1000);
    }
  };

  const getAIResponse = (userMessage) => {
    const responses = [
      "I can help you create that formula! Let me generate it for you.",
      "Great question! I'll analyze your data and provide insights.",
      "I'll create a pivot table for that data right away.",
      "Let me generate a chart to visualize your data better.",
      "I'll help you format those cells to match your requirements.",
      "I can automate that task for you. Let me set it up."
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          className="fixed right-0 top-0 h-full w-80 bg-white shadow-xl border-l border-gray-200 flex flex-col z-40"
        >
          <div className="bg-green-600 text-white p-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <MessageSquare className="w-5 h-5" />
              <span className="font-medium">SheetGenie Chat</span>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-3 py-2 rounded-lg ${
                    message.sender === 'user'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <p className="text-sm">{message.text}</p>
                  <p className="text-xs opacity-75 mt-1">{message.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask SheetGenie anything..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button
                onClick={handleSendMessage}
                className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// Spreadsheet Component
export const Spreadsheet = () => {
  const [data, setData] = useState(sampleData);

  const hotSettings = {
    data,
    rowHeaders: true,
    colHeaders: true,
    height: 'auto',
    licenseKey: 'non-commercial-and-evaluation',
    contextMenu: true,
    manualColumnResize: true,
    manualRowResize: true,
    filters: true,
    dropdownMenu: true,
    multiColumnSorting: true,
    afterChange: (changes) => {
      if (changes) {
        console.log('Data changed:', changes);
      }
    }
  };

  return (
    <div className="flex-1 p-4 bg-gray-50">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <HotTable
          {...hotSettings}
          className="htCore"
        />
      </div>
    </div>
  );
};

// File Upload Component
export const FileUpload = ({ onFileUpload }) => {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
      <div className="flex items-center space-x-3">
        <Upload className="w-5 h-5 text-blue-600" />
        <div>
          <p className="text-sm font-medium text-blue-900">Upload Excel File</p>
          <p className="text-xs text-blue-700">Upload your .xlsx file to get started</p>
        </div>
      </div>
      <input
        type="file"
        accept=".xlsx,.xls"
        onChange={handleFileChange}
        className="mt-2 w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-600 file:text-white hover:file:bg-blue-700"
      />
    </div>
  );
};

// Bottom Status Bar
export const StatusBar = () => {
  return (
    <div className="bg-green-600 text-white text-xs px-4 py-1 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <span>Ready</span>
        <span>•</span>
        <span>100%</span>
      </div>
      <div className="flex items-center space-x-2">
        <span>Sheet1</span>
        <span>Max: 5</span>
        <span>Add sheets to focus</span>
      </div>
    </div>
  );
};