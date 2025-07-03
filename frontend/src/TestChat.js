import React, { useState } from 'react';
import { Send, X, Brain } from 'lucide-react';

export const TestChat = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm SheetGenie AI. Try asking me to calculate sum of Q1 sales!", sender: 'ai', timestamp: '10:30 AM' }
  ]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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
          functionResults: data.function_results
        };
        
        setMessages(prev => [...prev, aiResponse]);
        
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
    <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl border-l border-gray-200 flex flex-col z-50">
      <div className="bg-green-600 text-white p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Brain className="w-5 h-5" />
          <span className="font-semibold">SheetGenie AI</span>
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
              <p className="text-sm">{message.text}</p>
              {message.functionResults && (
                <div className="mt-2 pt-2 border-t border-gray-300">
                  {message.functionResults.map((result, index) => (
                    <div key={index} className="text-xs bg-white/20 rounded p-2 mb-1">
                      <div><strong>Formula:</strong> {result.formula}</div>
                      <div><strong>Result:</strong> {result.result}</div>
                    </div>
                  ))}
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
        
        <div className="flex space-x-2 mt-2">
          <button 
            onClick={() => setNewMessage('calculate sum of Q1 sales')}
            className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded"
          >
            Sum Q1
          </button>
          <button 
            onClick={() => setNewMessage('create chart')}
            className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded"
          >
            Chart
          </button>
        </div>
      </div>
    </div>
  );
};