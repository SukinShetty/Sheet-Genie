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
  Percent,
  PieChart,
  LineChart,
  TrendingUp,
  Brain,
  Zap,
  Target
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
  ['Earbuds Pro', 12000, 14500, 16000, 18500, 61000, 13.1]
];

// Enhanced chat messages with AI suggestions
const initialMessages = [
  { 
    id: 1, 
    text: "Hello! I'm SheetGenie, your AI-powered Excel assistant. I can help you with calculations, create charts, analyze data, and much more!", 
    sender: 'ai', 
    timestamp: '10:30 AM',
    suggestions: [
      "Calculate sum of Q1 Sales",
      "Create a bar chart for sales data",
      "Find the product with highest growth",
      "Generate a pivot table"
    ]
  },
  { 
    id: 2, 
    text: "Try asking me to 'Sum column B' or 'Create a chart showing Q1 vs Q4 sales'. I understand natural language!", 
    sender: 'ai', 
    timestamp: '10:30 AM' 
  }
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
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
            >
              <FolderOpen className="w-4 h-4" />
              <span>Open Xlsx File</span>
            </button>
            <button 
              onClick={onNewFile}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
            >
              <File className="w-4 h-4" />
              <span>New File</span>
            </button>
            <button 
              onClick={onSaveFile}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
            >
              <Save className="w-4 h-4" />
              <span>Save File</span>
            </button>
          </div>
          <div className="text-gray-400">|</div>
          <div className="flex items-center space-x-2">
            <button 
              onClick={onSettings}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
            >
              <Settings className="w-4 h-4" />
              <span>Settings</span>
            </button>
            <button 
              onClick={onSecurity}
              className="flex items-center space-x-1 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
            >
              <Shield className="w-4 h-4" />
              <span>Security</span>
            </button>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600">SheetGenie Pro</span>
        </div>
      </div>
    </div>
  );
};

// Enhanced Spreadsheet Toolbar Component
export const SpreadsheetToolbar = ({ onNewChat }) => {
  return (
    <div className="bg-white border-b border-gray-200 px-4 py-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1">
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors">HOME</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors">INSERT</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors">FORMULAS</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors">DATA</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors">VIEW</button>
            <button className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded transition-colors">AI INSIGHTS</button>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button 
            onClick={onNewChat}
            className="flex items-center space-x-1 px-4 py-2 text-sm bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-200 shadow-md hover:shadow-lg"
          >
            <Brain className="w-4 h-4" />
            <span>AI Assistant</span>
          </button>
        </div>
      </div>
      
      {/* Enhanced second row of toolbar */}
      <div className="flex items-center space-x-4 mt-2 border-t border-gray-100 pt-2">
        <div className="flex items-center space-x-2">
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <Type className="w-4 h-4" />
          </button>
          <select className="text-sm border-none bg-transparent text-gray-600 hover:bg-gray-50 rounded px-2 py-1">
            <option>Calibri</option>
            <option>Arial</option>
            <option>Times New Roman</option>
          </select>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <Bold className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <Italic className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <Underline className="w-4 h-4" />
          </button>
        </div>
        <div className="text-gray-300">|</div>
        <div className="flex items-center space-x-2">
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <AlignLeft className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <Hash className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors">
            <Percent className="w-4 h-4" />
          </button>
        </div>
        <div className="text-gray-300">|</div>
        <div className="flex items-center space-x-2">
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors" title="Create Chart">
            <BarChart3 className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors" title="Functions">
            <Calculator className="w-4 h-4" />
          </button>
          <button className="p-1 text-gray-600 hover:bg-gray-100 rounded transition-colors" title="Format">
            <Palette className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

// Enhanced Welcome Modal Component with better animations
export const WelcomeModal = ({ isOpen, onClose, onNext }) => {
  const [currentStep, setCurrentStep] = useState(1);

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      onClose();
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleClose = () => {
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 backdrop-blur-sm"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.9, opacity: 0, y: 20 }}
            transition={{ type: "spring", duration: 0.5 }}
            className="bg-white rounded-xl shadow-2xl p-8 max-w-lg w-full mx-4"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800 bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                Welcome to SheetGenie
              </h2>
              <button
                onClick={handleClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="text-center mb-8">
              <div className="flex justify-center mb-4">
                <div className="flex space-x-2">
                  {[1, 2, 3].map((step) => (
                    <motion.div
                      key={step}
                      className={`w-3 h-3 rounded-full transition-all duration-300 ${
                        currentStep === step ? 'bg-green-500 shadow-lg' : 'bg-gray-300'
                      }`}
                      animate={{
                        scale: currentStep === step ? 1.2 : 1,
                      }}
                    />
                  ))}
                </div>
              </div>
              <p className="text-gray-600 mb-6">Your AI-powered Excel assistant that revolutionizes spreadsheet work</p>
              
              <AnimatePresence mode="wait">
                {currentStep === 1 && (
                  <motion.div
                    key="step1"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="space-y-4"
                  >
                    <div className="bg-gradient-to-br from-blue-50 to-green-50 rounded-lg h-56 flex items-center justify-center relative overflow-hidden">
                      <img 
                        src="https://images.unsplash.com/photo-1545063328-c8e3faffa16f" 
                        alt="SheetGenie Demo" 
                        className="w-full h-full object-cover rounded-lg"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent flex items-center justify-center">
                        <motion.div
                          animate={{ scale: [1, 1.1, 1] }}
                          transition={{ duration: 2, repeat: Infinity }}
                          className="bg-white/20 backdrop-blur-sm rounded-full p-4"
                        >
                          <Play className="w-12 h-12 text-white" />
                        </motion.div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">Natural language commands that transform into Excel magic</p>
                  </motion.div>
                )}
                
                {currentStep === 2 && (
                  <motion.div
                    key="step2"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="space-y-4"
                  >
                    <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg h-56 flex items-center justify-center p-6">
                      <img 
                        src="https://images.pexels.com/photos/8532850/pexels-photo-8532850.jpeg" 
                        alt="AI Assistant" 
                        className="w-full h-full object-cover rounded-lg"
                      />
                    </div>
                    <p className="text-sm text-gray-600">Advanced AI that understands context and provides intelligent insights</p>
                  </motion.div>
                )}
                
                {currentStep === 3 && (
                  <motion.div
                    key="step3"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="space-y-4"
                  >
                    <div className="bg-gradient-to-br from-green-50 to-yellow-50 rounded-lg h-56 flex items-center justify-center p-6">
                      <img 
                        src="https://images.pexels.com/photos/16053029/pexels-photo-16053029.jpeg" 
                        alt="Smart Features" 
                        className="w-full h-full object-cover rounded-lg"
                      />
                    </div>
                    <p className="text-sm text-gray-600">Automated charts, formulas, and data visualization at lightning speed</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
            
            <div className="flex justify-between items-center">
              <button
                onClick={handleBack}
                className="flex items-center space-x-1 px-4 py-2 text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50 transition-colors rounded-lg hover:bg-gray-50"
                disabled={currentStep === 1}
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
              
              <span className="text-sm text-gray-500 font-medium">{currentStep} of 3</span>
              
              <button
                onClick={handleNext}
                className="flex items-center space-x-1 px-6 py-2 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg hover:from-green-700 hover:to-green-800 text-sm transition-all duration-200 shadow-md hover:shadow-lg"
              >
                <span>{currentStep === 3 ? 'Start Creating!' : 'Next'}</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// Chart Display Component
export const ChartDisplay = ({ chartData, onClose }) => {
  if (!chartData) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg border border-gray-200 p-4 mb-4"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">{chartData.title || 'Generated Chart'}</h3>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
      <div className="w-full h-64">
        <Plot
          data={chartData.data}
          layout={{
            ...chartData.layout,
            autosize: true,
            margin: { t: 40, r: 40, b: 40, l: 40 }
          }}
          config={{
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d']
          }}
          style={{ width: '100%', height: '100%' }}
          useResizeHandler={true}
        />
      </div>
    </motion.div>
  );
};

// Enhanced Chat Component with AI suggestions and function results
export const Chat = ({ isOpen, onClose, onDataUpdate }) => {
  const [messages, setMessages] = useState(initialMessages);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [charts, setCharts] = useState([]);

  const handleSendMessage = async () => {
    if (newMessage.trim() && !isLoading) {
      const userMessage = {
        id: messages.length + 1,
        text: newMessage,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages([...messages, userMessage]);
      setNewMessage('');
      setIsLoading(true);
      
      try {
        // Call the backend API
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: newMessage
          })
        });
        
        if (!response.ok) {
          throw new Error('Failed to get AI response');
        }
        
        const data = await response.json();
        
        // Add AI response
        const aiResponse = {
          id: messages.length + 2,
          text: data.response || 'I processed your request!',
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          functionResults: data.function_results,
          updatedData: data.updated_data
        };
        
        setMessages(prev => [...prev, aiResponse]);
        
        // Handle chart generation
        if (data.function_results) {
          data.function_results.forEach(result => {
            if (result.chart_data) {
              setCharts(prev => [...prev, {
                id: Date.now(),
                ...result.chart_data
              }]);
            }
          });
        }
        
        // Update spreadsheet data if available
        if (data.updated_data && onDataUpdate) {
          onDataUpdate(data.updated_data);
        }
        
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage = {
          id: messages.length + 2,
          text: 'Sorry, I encountered an error processing your request. Please try again.',
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setNewMessage(suggestion);
  };

  const removeChart = (chartId) => {
    setCharts(prev => prev.filter(chart => chart.id !== chartId));
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ type: "spring", damping: 25, stiffness: 200 }}
          className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl border-l border-gray-200 flex flex-col z-40"
        >
          <div className="bg-gradient-to-r from-green-600 to-green-700 text-white p-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="w-5 h-5" />
              <span className="font-semibold">SheetGenie AI</span>
              <span className="bg-white/20 px-2 py-1 rounded-full text-xs">Pro</span>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-3 rounded-2xl ${
                    message.sender === 'user'
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <p className="text-sm leading-relaxed">{message.text}</p>
                  {message.functionResults && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      {message.functionResults.map((result, index) => (
                        <div key={index} className="text-xs bg-white/10 rounded p-2 mb-1">
                          <span className="font-semibold">Formula:</span> {result.formula}
                          <br />
                          <span className="font-semibold">Result:</span> {result.result}
                        </div>
                      ))}
                    </div>
                  )}
                  <p className="text-xs opacity-75 mt-2">{message.timestamp}</p>
                  
                  {message.suggestions && (
                    <div className="mt-3 space-y-1">
                      <p className="text-xs font-semibold">Try these:</p>
                      {message.suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="block w-full text-left text-xs bg-white/10 hover:bg-white/20 rounded p-2 transition-colors"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
            
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-start"
              >
                <div className="bg-gray-100 rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
          
          <div className="p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
                placeholder="Ask SheetGenie anything..."
                disabled={isLoading}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:opacity-50 transition-all"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading}
                className="p-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
              >
                {isLoading ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </button>
            </div>
            
            {/* Quick Action Buttons */}
            <div className="flex space-x-2 mt-3">
              <button 
                onClick={() => handleSuggestionClick('Sum all sales')}
                className="flex-1 text-xs bg-green-100 text-green-700 px-3 py-2 rounded-lg hover:bg-green-200 transition-colors"
              >
                <Calculator className="w-3 h-3 inline mr-1" />
                Sum
              </button>
              <button 
                onClick={() => handleSuggestionClick('Create chart')}
                className="flex-1 text-xs bg-blue-100 text-blue-700 px-3 py-2 rounded-lg hover:bg-blue-200 transition-colors"
              >
                <BarChart3 className="w-3 h-3 inline mr-1" />
                Chart
              </button>
              <button 
                onClick={() => handleSuggestionClick('Analyze trends')}
                className="flex-1 text-xs bg-purple-100 text-purple-700 px-3 py-2 rounded-lg hover:bg-purple-200 transition-colors"
              >
                <TrendingUp className="w-3 h-3 inline mr-1" />
                Analyze
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

// Enhanced Spreadsheet Component
export const Spreadsheet = ({ data, onDataChange }) => {
  const [currentData, setCurrentData] = useState(data || sampleData);

  useEffect(() => {
    if (data) {
      setCurrentData(data);
    }
  }, [data]);

  const hotSettings = {
    data: currentData,
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
    stretchH: 'all',
    columnSorting: true,
    afterChange: (changes) => {
      if (changes && onDataChange) {
        onDataChange(currentData);
      }
    },
    cells: function (row, col) {
      const cellProperties = {};
      
      // Header row styling
      if (row === 0) {
        cellProperties.className = 'htCenter htMiddle font-semibold bg-gray-50';
      }
      
      // Numeric formatting for certain columns
      if (col > 0 && col < 6 && row > 0) {
        cellProperties.numericFormat = {
          pattern: '$0,0.00'
        };
      }
      
      return cellProperties;
    }
  };

  return (
    <div className="flex-1 p-6 bg-gray-50">
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        <div className="p-4 bg-gradient-to-r from-gray-50 to-white border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-800">Sales Performance Dashboard</h2>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Target className="w-4 h-4" />
              <span>AI-Enhanced Spreadsheet</span>
            </div>
          </div>
        </div>
        <div className="p-4">
          <HotTable
            {...hotSettings}
            className="htCore"
          />
        </div>
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
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-dashed border-blue-300 rounded-xl hover:border-blue-400 transition-colors"
    >
      <div className="text-center">
        <Upload className="w-12 h-12 text-blue-600 mx-auto mb-4" />
        <div>
          <p className="text-lg font-semibold text-blue-900 mb-2">Upload Excel File</p>
          <p className="text-sm text-blue-700 mb-4">Drop your .xlsx file here or click to browse</p>
        </div>
        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileChange}
          className="w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:transition-colors file:cursor-pointer cursor-pointer"
        />
      </div>
    </motion.div>
  );
};

// Enhanced Status Bar
export const StatusBar = () => {
  return (
    <div className="bg-gradient-to-r from-green-600 to-green-700 text-white text-xs px-6 py-2 flex items-center justify-between">
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-300 rounded-full animate-pulse"></div>
          <span>AI Ready</span>
        </div>
        <span>•</span>
        <span>100% Performance</span>
        <span>•</span>
        <div className="flex items-center space-x-1">
          <Zap className="w-3 h-3" />
          <span>Real-time Processing</span>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <span>Sheet1</span>
        <span>•</span>
        <span>Enhanced with AI</span>
        <span>•</span>
        <span>SheetGenie Pro</span>
      </div>
    </div>
  );
};