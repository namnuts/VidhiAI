import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const RagInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [charCount, setCharCount] = useState(0);
  const [theme, setTheme] = useState('default'); // 'default', 'dark', 'ocean', 'forest'
  const textareaRef = useRef(null);
  const responseRef = useRef(null);
  const containerRef = useRef(null);
  const [containerHeight, setContainerHeight] = useState(0);


  // const backendURL = process.env.REACT_APP_BACKEND_URL;
  const backendURL = import.meta.env.VITE_BACKEND_URL;

  // Theme configurations
  const themes = {
    default: {
      background: 'bg-gradient-to-br from-indigo-50 to-purple-50',
      card: 'bg-white',
      text: 'text-gray-800',
      accent: 'from-indigo-600 to-purple-600',
      button: 'bg-white text-indigo-600',
      input: 'border-gray-200 focus:ring-indigo-500',
      response: 'bg-gray-50 border-gray-100',
      history: 'border-gray-100 hover:bg-gray-50'
    },
    dark: {
      background: 'bg-gradient-to-br from-gray-900 to-gray-800',
      card: 'bg-gray-800',
      text: 'text-gray-100',
      accent: 'from-purple-500 to-pink-500',
      button: 'bg-gray-700 text-purple-300',
      input: 'border-gray-700 focus:ring-purple-500 bg-gray-700 text-gray-100',
      response: 'bg-gray-700 border-gray-600 text-gray-100',
      history: 'border-gray-700 hover:bg-gray-700'
    },
    ocean: {
      background: 'bg-gradient-to-br from-blue-50 to-cyan-50',
      card: 'bg-white',
      text: 'text-gray-800',
      accent: 'from-blue-600 to-cyan-600',
      button: 'bg-white text-blue-600',
      input: 'border-gray-200 focus:ring-blue-500',
      response: 'bg-blue-50 border-blue-100',
      history: 'border-blue-100 hover:bg-blue-50'
    },
    forest: {
      background: 'bg-gradient-to-br from-green-50 to-emerald-50',
      card: 'bg-white',
      text: 'text-gray-800',
      accent: 'from-green-600 to-emerald-600',
      button: 'bg-white text-green-600',
      input: 'border-gray-200 focus:ring-green-500',
      response: 'bg-green-50 border-green-100',
      history: 'border-green-100 hover:bg-green-50'
    }
  };

  const currentTheme = themes[theme];

  useEffect(() => {
    // Set container height based on viewport
    const updateHeight = () => {
      if (containerRef.current) {
        const headerHeight = 100; // Approximate height of header
        const historyHeight = showHistory ? 350 : 0; // Approximate height of history section
        const availableHeight = window.innerHeight - headerHeight - historyHeight - 40; // 40px for padding
        setContainerHeight(availableHeight);
      }
    };

    updateHeight();
    window.addEventListener('resize', updateHeight);
    return () => window.removeEventListener('resize', updateHeight);
  }, [showHistory]);

  useEffect(() => {
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [query]);

  useEffect(() => {
    // Scroll to bottom of response when it updates
    if (responseRef.current && response) {
      responseRef.current.scrollTop = responseRef.current.scrollHeight;
    }
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsLoading(true);
    const currentQuery = query;
    setQuery('');
    
    // Add to history
    const newHistoryItem = {
      id: Date.now(),
      query: currentQuery,
      response: '',
      timestamp: new Date().toLocaleTimeString()
    };
    
    setHistory(prev => [newHistoryItem, ...prev]);
    
    // TODO: Replace with actual API call
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      const responseText = await fetch(`${backendURL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: currentQuery
        })
      });
      
      const result = await responseText.json();
      // console.log(result);
      setResponse(result.answer.text);
      
      // Update history with response
      setHistory(prev => 
        prev.map(item => 
          item.id === newHistoryItem.id 
            ? { ...item, response: result.answer.text } 
            : item
        )
      );
    } catch (error) {
      console.error('Error:', error);
      setResponse('Sorry, there was an error processing your request.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const clearAll = () => {
    setQuery('');
    setResponse('');
    setHistory([]);
  };

  const loadHistoryItem = (item) => {
    setQuery(item.query);
    setResponse(item.response);
    setShowHistory(false);
  };

  const cycleTheme = () => {
    const themeKeys = Object.keys(themes);
    const currentIndex = themeKeys.indexOf(theme);
    const nextIndex = (currentIndex + 1) % themeKeys.length;
    setTheme(themeKeys[nextIndex]);
  };

  return (
    <div className={`min-h-screen w-full ${currentTheme.background} flex flex-col`}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full px-4 py-4 flex-shrink-0"
      >
        <div className="flex justify-between items-center mb-4">
          <h1 className={`text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r ${currentTheme.accent}`}>
          VidhiAI 
          </h1>
          <div className="flex space-x-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowHistory(!showHistory)}
              className={`${currentTheme.button} px-4 py-2 rounded-lg shadow-md font-medium`}
            >
              {showHistory ? 'Hide History' : 'Show History'}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={clearAll}
              className={`${currentTheme.button} px-4 py-2 rounded-lg shadow-md font-medium`}
            >
              Clear All
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={cycleTheme}
              className={`${currentTheme.button} px-4 py-2 rounded-lg shadow-md font-medium flex items-center`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
              Theme
            </motion.button>
          </div>
        </div>
      </motion.div>
      
      <div ref={containerRef} className="flex-grow px-4 pb-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full h-full">
          {/* Assistant Info Panel */}
          <motion.div
  initial={{ opacity: 0, x: -20 }}
  animate={{ opacity: 1, x: 0 }}
  transition={{ duration: 0.5, delay: 0.2 }}
  className={`${currentTheme.card} rounded-2xl shadow-xl p-6 flex flex-col h-full`}
  style={{ height: containerHeight > 0 ? `${containerHeight}px` : 'auto' }}
>
  <h2 className={`text-2xl font-semibold mb-4 ${currentTheme.text}`}>About This Legal Assistant</h2>
  <div className="flex-grow overflow-y-auto">
    <div className="prose prose-lg max-w-none">
      <p className={`${currentTheme.text} mb-4`}>
        This AI Legal Assistant uses a Retrieval-Augmented Generation (RAG) model built on Indian legal documents to provide precise answers to legal queries.
      </p>
      <h3 className={`text-xl font-medium mt-6 mb-2 ${currentTheme.text}`}>How It Works</h3>
      <p className={`${currentTheme.text} mb-4`}>
        The assistant retrieves relevant sections from Indian laws, acts, and court rulings using a vector search engine, and generates a legally sound response using a language model.
      </p>
      <h3 className={`text-xl font-medium mt-6 mb-2 ${currentTheme.text}`}>Features</h3>
      <ul className={`list-disc pl-5 ${currentTheme.text} mb-4`}>
        <li>Accurate legal references from Indian law</li>
        <li>Smart context-based answers</li>
        <li>Answers backed by case laws or acts</li>
        <li>Works in real-time with your legal query</li>
      </ul>
      <h3 className={`text-xl font-medium mt-6 mb-2 ${currentTheme.text}`}>Tips</h3>
      <ul className={`list-disc pl-5 ${currentTheme.text} mb-4`}>
        <li>Ask questions related to Indian laws, acts, or court procedures</li>
        <li>Use specific legal terms when possible</li>
        <li>Mention the relevant domain (e.g., property, criminal, contract)</li>
        <li>Press Enter to submit your query and receive results from the legal database</li>
      </ul>
    </div>
  </div>
</motion.div>


          {/* Response Panel */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className={`lg:col-span-2 ${currentTheme.card} rounded-2xl shadow-xl p-6 flex flex-col h-full`}
            style={{ height: containerHeight > 0 ? `${containerHeight}px` : 'auto' }}
          >
            <h2 className={`text-2xl font-semibold mb-4 ${currentTheme.text}`}>Response</h2>
            <div 
              ref={responseRef}
              className={`flex-grow overflow-y-auto p-4 border rounded-xl ${currentTheme.response} mb-4`}
            >
              {response ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                  className="prose prose-lg max-w-none"
                >
                  <p className={`${currentTheme.text} whitespace-pre-wrap`}>{response}</p>
                </motion.div>
              ) : (
                <div className="h-full flex items-center justify-center text-gray-400">
                  <p className="text-lg">Your response will appear here</p>
                </div>
              )}
            </div>

            {/* Input at the bottom */}
            <div className="mt-auto">
              <form onSubmit={handleSubmit} className="relative">
                <textarea
                  ref={textareaRef}
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setCharCount(e.target.value.length);
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your question here... (Press Enter to send)"
                  className={`w-full p-4 border rounded-xl focus:ring-2 focus:border-transparent resize-none transition-all duration-200 ${currentTheme.input}`}
                  style={{ minHeight: '100px', maxHeight: '150px' }}
                />
                <div className="absolute bottom-4 left-4 text-sm text-gray-400">
                  {charCount} characters
                </div>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  type="submit"
                  disabled={isLoading || !query.trim()}
                  className={`absolute bottom-4 right-4 bg-gradient-to-r ${currentTheme.accent} text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed text-lg`}
                >
                  {isLoading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="w-6 h-6 border-2 border-white border-t-transparent rounded-full"
                    />
                  ) : (
                    'Send'
                  )}
                </motion.button>
              </form>
            </div>
          </motion.div>
        </div>

        <AnimatePresence>
          {showHistory && history.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className={`mt-6 ${currentTheme.card} rounded-2xl shadow-xl p-4 overflow-hidden`}
            >
              <h2 className={`text-2xl font-semibold mb-2 ${currentTheme.text}`}>History</h2>
              <div className="space-y-4 max-h-[300px] overflow-y-auto">
                {history.map((item) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className={`border rounded-xl p-4 cursor-pointer transition-colors ${currentTheme.history}`}
                    onClick={() => loadHistoryItem(item)}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-500">{item.timestamp}</span>
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        className={`text-sm font-medium ${currentTheme.text}`}
                      >
                        Load
                      </motion.button>
                    </div>
                    <p className={`font-medium ${currentTheme.text}`}>{item.query}</p>
                    {item.response && (
                      <p className="text-gray-500 text-sm mt-2 line-clamp-2">{item.response}</p>
                    )}
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default RagInterface;
