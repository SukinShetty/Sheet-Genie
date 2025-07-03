import React, { useState } from 'react';
import { Send, X, Brain, BarChart3, TrendingUp, Eye } from 'lucide-react';
import { ChartRenderer, DashboardGrid, ChartSuggestion } from './ChartComponents';

export const TestChat = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm SheetGenie AI. Try these advanced commands: 'Generate insights', 'Create dashboard', or 'Suggest chart'!", sender: 'ai', timestamp: '10:30 AM' }
  ]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeChart, setActiveChart] = useState(null);
  const [activeDashboard, setActiveDashboard] = useState(null);

  const handleSendMessage = async () => {
    if (newMessage.trim() && !isLoading) {
      const userMessage = {
        id: messages.length + 1,
        text: newMessage,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages([...messages, userMessage]);
      const currentMessage = newMessage;
      setNewMessage('');
      setIsLoading(true);
      
      try {
        console.log('Sending request to backend...');
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: currentMessage
          })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
        const aiResponse = {
          id: messages.length + 2,
          text: data.response || 'I processed your request!',
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          functionResults: data.function_results,
          insights: data.function_results?.[0]?.insights,
          dashboard: data.function_results?.[0]?.dashboard_config,
          chartSuggestion: data.function_results?.[0]?.suggestions
        };
        
        setMessages(prev => [...prev, aiResponse]);
        
        // Handle special responses
        if (data.function_results) {
          const result = data.function_results[0];
          
          // Dashboard creation
          if (result.dashboard_config) {
            setActiveDashboard(result.dashboard_config);
          }
          
          // Chart suggestions
          if (result.chart_config) {
            setActiveChart(result.chart_config);
          }
        }
        
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage = {
          id: messages.length + 2,
          text: `Error: ${error.message}`,
          sender: 'ai',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Chat Panel */}
      <div className="w-96 bg-white shadow-2xl border-r border-gray-200 flex flex-col">
        <div className="bg-green-600 text-white p-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Brain className="w-5 h-5" />
            <span className="font-semibold">SheetGenie AI Pro</span>
          </div>
          <button onClick={onClose} className="text-white hover:text-gray-200">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs px-4 py-3 rounded-2xl ${
                message.sender === 'user' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-800'
              }`}>
                {/* Main message text with improved formatting */}
                <div className="text-sm whitespace-pre-line">{message.text}</div>
                
                {/* Function Results */}
                {message.functionResults && (
                  <div className="mt-3 pt-3 border-t border-gray-300">
                    <div className="text-xs font-semibold text-gray-600 mb-2">📊 Analysis Details:</div>
                    {message.functionResults.map((result, index) => (
                      <div key={index} className="text-xs bg-white/30 rounded p-2 mb-2">
                        {result.formula && (
                          <div className="mb-1"><strong>Formula:</strong> <code>{result.formula}</code></div>
                        )}
                        {result.result !== undefined && (
                          <div className="mb-1"><strong>Result:</strong> {typeof result.result === 'number' ? result.result.toLocaleString() : result.result}</div>
                        )}
                        {result.analysis_type && (
                          <div className="mb-1"><strong>Analysis:</strong> {result.analysis_type}</div>
                        )}
                        {result.message && !result.formula && (
                          <div><strong>Action:</strong> {result.message}</div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Chart Suggestions */}
                {message.chartSuggestion && (
                  <div className="mt-2">
                    <ChartSuggestion 
                      suggestion={message.chartSuggestion}
                      onCreateChart={(chart) => setActiveChart(chart)}
                    />
                  </div>
                )}
                
                <p className="text-xs opacity-75 mt-2">{message.timestamp}</p>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center space-x-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask SheetGenie anything..."
              disabled={isLoading}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading}
              className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          
          {/* Quick Action Buttons */}
          <div className="grid grid-cols-2 gap-2 mt-3">
            <button 
              onClick={() => setNewMessage('Generate detailed insights')}
              className="text-xs bg-purple-100 text-purple-700 px-2 py-2 rounded flex items-center justify-center space-x-1"
            >
              <Eye className="w-3 h-3" />
              <span>Insights</span>
            </button>
            <button 
              onClick={() => setNewMessage('Create dashboard')}
              className="text-xs bg-blue-100 text-blue-700 px-2 py-2 rounded flex items-center justify-center space-x-1"
            >
              <BarChart3 className="w-3 h-3" />
              <span>Dashboard</span>
            </button>
            <button 
              onClick={() => setNewMessage('Forecast Q4 sales for 3 periods')}
              className="text-xs bg-orange-100 text-orange-700 px-2 py-2 rounded flex items-center justify-center space-x-1"
            >
              <TrendingUp className="w-3 h-3" />
              <span>Forecast</span>
            </button>
            <button 
              onClick={() => setNewMessage('Suggest best chart for Product vs Total')}
              className="text-xs bg-green-100 text-green-700 px-2 py-2 rounded flex items-center justify-center space-x-1"
            >
              <BarChart3 className="w-3 h-3" />
              <span>Chart</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 bg-gray-50 overflow-auto">
        {activeDashboard ? (
          <DashboardGrid dashboardConfig={activeDashboard} />
        ) : activeChart ? (
          <div className="p-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <ChartRenderer chartConfig={activeChart} />
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <Brain className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-700 mb-2">AI-Powered Analytics</h3>
              <p className="text-gray-500 mb-4">Ask me to create insights, dashboards, or charts</p>
              <div className="space-y-2 text-sm text-gray-600">
                <p>• "Generate detailed insights"</p>
                <p>• "Create dashboard"</p>
                <p>• "Suggest chart for Product vs Sales"</p>
                <p>• "Forecast next quarter"</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};