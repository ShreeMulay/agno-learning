import React, { useState, useEffect } from 'react'
import { 
  BookOpen, 
  Play, 
  Settings, 
  Search, 
  ChevronRight, 
  Terminal,
  MessageSquare,
  Cpu,
  Layers,
  Code,
  Moon,
  Sun,
  X,
  RotateCcw,
  Zap,
  Info
} from 'lucide-react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const API_BASE = 'http://localhost:8000/api/v1'

const PROVIDERS = [
  { id: 'openrouter', name: 'OpenRouter', defaultModel: 'anthropic/claude-3.5-sonnet' },
  { id: 'openai', name: 'OpenAI', defaultModel: 'gpt-4o' },
  { id: 'anthropic', name: 'Anthropic', defaultModel: 'claude-3-5-sonnet-latest' },
  { id: 'google', name: 'Google Gemini', defaultModel: 'gemini-2.0-flash' },
  { id: 'groq', name: 'Groq', defaultModel: 'llama-3.3-70b-versatile' },
  { id: 'ollama', name: 'Ollama (Local)', defaultModel: 'llama3.2' },
]

export default function App() {
  const [modules, setModules] = useState([])
  const [activeLesson, setActiveLesson] = useState(null)
  const [lessonDetails, setLessonDetails] = useState(null)
  const [loading, setLoading] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [activeTab, setActiveTab] = useState('docs') // docs, playground
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark')
  const [showSettings, setShowSettings] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  
  // Settings state
  const [config, setConfig] = useState({
    provider: 'openrouter',
    model: '',
    temperature: 0.7,
  })

  useEffect(() => {
    fetchModules()
    applyTheme(theme)
  }, [])

  const applyTheme = (t) => {
    if (t === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('theme', t)
  }

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
    applyTheme(newTheme)
  }

  const fetchModules = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/modules`)
      setModules(resp.data)
    } catch (err) {
      console.error("Failed to fetch modules", err)
    }
  }

  const selectLesson = async (lesson) => {
    setActiveLesson(lesson)
    setLoading(true)
    try {
      const resp = await axios.get(`${API_BASE}/lessons/${lesson.module}/${lesson.id}`)
      setLessonDetails(resp.data)
      setChatMessages([])
      setActiveTab('docs')
    } catch (err) {
      console.error("Failed to fetch lesson details", err)
    } finally {
      setLoading(false)
    }
  }

  const runDemo = () => {
    setInputMessage(lessonDetails.default_message || 'Hello!')
    setActiveTab('playground')
  }

  const sendMessage = (customMsg = null) => {
    const messageToSend = customMsg || inputMessage
    if (!messageToSend.trim() || isStreaming) return

    const userMsg = { role: 'user', content: messageToSend }
    setChatMessages(prev => [...prev, userMsg])
    setInputMessage('')
    setIsStreaming(true)

    const wsProvider = `ws://localhost:8000/ws/api/v1/agents/${activeLesson.module}/${activeLesson.id}/run`
    const socket = new WebSocket(wsProvider)

    const agentMsg = { role: 'assistant', content: '' }
    setChatMessages(prev => [...prev, agentMsg])

    socket.onopen = () => {
      socket.send(JSON.stringify({
        message: messageToSend,
        provider: config.provider,
        model: config.model || undefined,
        temperature: config.temperature
      }))
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'content') {
        setChatMessages(prev => {
          const last = prev[prev.length - 1]
          const updated = { ...last, content: last.content + data.content }
          return [...prev.slice(0, -1), updated]
        })
      } else if (data.type === 'done') {
        setIsStreaming(false)
        socket.close()
      } else if (data.type === 'error') {
        setChatMessages(prev => {
          const last = prev[prev.length - 1]
          const updated = { ...last, content: last.content + `\n\n**Error:** ${data.content}` }
          return [...prev.slice(0, -1), updated]
        })
        setIsStreaming(false)
        socket.close()
      }
    }

    socket.onerror = (err) => {
      console.error("WebSocket error", err)
      setIsStreaming(false)
    }
  }

  const resetChat = () => {
    setChatMessages([])
    setIsStreaming(false)
  }

  const filteredModules = modules.map(mod => ({
    ...mod,
    lessons: mod.lessons.filter(l => 
      l.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
      mod.title.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter(mod => mod.lessons.length > 0)

  return (
    <div className={`flex h-screen overflow-hidden font-sans transition-colors duration-300 ${theme === 'dark' ? 'bg-[#0f172a] text-slate-200' : 'bg-slate-50 text-slate-900'}`}>
      {/* Sidebar */}
      <aside className={`w-72 border-r flex flex-col transition-colors duration-300 ${theme === 'dark' ? 'bg-[#1e293b] border-slate-800' : 'bg-white border-slate-200'}`}>
        <div className="p-6 border-b border-inherit flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-teal-600 rounded-lg flex items-center justify-center shadow-lg shadow-teal-600/20">
              <Cpu className="text-white" size={24} />
            </div>
            <h1 className="text-xl font-bold tracking-tight">Agno Portal</h1>
          </div>
          <button 
            onClick={toggleTheme}
            className={`p-2 rounded-full transition-colors ${theme === 'dark' ? 'hover:bg-slate-700 text-yellow-400' : 'hover:bg-slate-100 text-slate-600'}`}
          >
            {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
          <div className="relative mb-6">
            <Search className={`absolute left-3 top-1/2 -translate-y-1/2 ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`} size={16} />
            <input 
              type="text" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search lessons..." 
              className={`w-full border rounded-md py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 transition-all ${
                theme === 'dark' ? 'bg-[#0f172a] border-slate-700' : 'bg-slate-50 border-slate-200'
              }`}
            />
          </div>

          <nav className="space-y-6">
            {filteredModules.map(mod => (
              <div key={mod.id} className="space-y-2">
                <h3 className={`text-xs font-semibold uppercase tracking-wider flex items-center gap-2 ${theme === 'dark' ? 'text-slate-500' : 'text-slate-400'}`}>
                  <Layers size={14} />
                  {mod.title}
                </h3>
                <div className="space-y-1">
                  {mod.lessons.map(lesson => (
                    <button
                      key={lesson.key}
                      onClick={() => selectLesson(lesson)}
                      className={`w-full text-left px-3 py-2 rounded-md text-sm transition-all flex items-center justify-between group ${
                        activeLesson?.key === lesson.key 
                          ? 'bg-teal-600/20 text-teal-500 font-semibold border border-teal-600/30' 
                          : `hover:bg-opacity-50 ${theme === 'dark' ? 'text-slate-400 hover:bg-slate-800 hover:text-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'}`
                      }`}
                    >
                      <span className="truncate">{lesson.title}</span>
                      <ChevronRight size={14} className={`opacity-0 group-hover:opacity-100 transition-opacity ${activeLesson?.key === lesson.key ? 'opacity-100' : ''}`} />
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </nav>
        </div>

        <div className={`p-4 border-t border-inherit`}>
          <button 
            onClick={() => setShowSettings(!showSettings)}
            className={`flex items-center gap-3 w-full px-3 py-2 rounded-md transition-colors text-sm font-medium ${
              showSettings ? 'bg-teal-600 text-white' : `${theme === 'dark' ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'}`
            }`}
          >
            <Settings size={18} />
            Settings
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative">
        {activeLesson ? (
          <>
            {/* Header */}
            <header className={`h-16 border-b flex items-center justify-between px-8 backdrop-blur-md sticky top-0 z-10 ${theme === 'dark' ? 'bg-[#0f172a]/80 border-slate-800' : 'bg-white/80 border-slate-200'}`}>
              <div className="flex items-center gap-6">
                <h2 className="text-lg font-bold">{activeLesson.title}</h2>
                <div className={`flex p-1 rounded-lg ${theme === 'dark' ? 'bg-[#1e293b]' : 'bg-slate-100 border border-slate-200'}`}>
                  <button 
                    onClick={() => setActiveTab('docs')}
                    className={`px-4 py-1.5 rounded-md text-sm font-semibold transition-all flex items-center gap-2 ${activeTab === 'docs' ? 'bg-teal-600 text-white shadow-lg' : `${theme === 'dark' ? 'text-slate-400 hover:text-slate-200' : 'text-slate-500 hover:text-slate-900'}`}`}
                  >
                    <BookOpen size={16} /> Docs
                  </button>
                  <button 
                    onClick={() => setActiveTab('playground')}
                    className={`px-4 py-1.5 rounded-md text-sm font-semibold transition-all flex items-center gap-2 ${activeTab === 'playground' ? 'bg-teal-600 text-white shadow-lg' : `${theme === 'dark' ? 'text-slate-400 hover:text-slate-200' : 'text-slate-500 hover:text-slate-900'}`}`}
                  >
                    <Play size={16} /> Playground
                  </button>
                </div>
              </div>
              
              <div className="flex items-center gap-4">
                {activeTab === 'docs' && (
                  <button 
                    onClick={runDemo}
                    className="flex items-center gap-2 px-4 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded-full text-xs font-bold transition-all shadow-lg shadow-teal-600/20"
                  >
                    <Zap size={14} /> Run Example
                  </button>
                )}
                {activeTab === 'playground' && (
                  <button 
                    onClick={resetChat}
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${theme === 'dark' ? 'bg-slate-800 hover:bg-slate-700 text-slate-300' : 'bg-slate-200 hover:bg-slate-300 text-slate-700'}`}
                  >
                    <RotateCcw size={14} /> Reset
                  </button>
                )}
                <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${theme === 'dark' ? 'bg-slate-800 text-green-400 border border-green-400/20' : 'bg-green-50 text-green-600 border border-green-200'}`}>
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
                  Online
                </div>
              </div>
            </header>

            {/* Content Area */}
            <div className="flex-1 overflow-hidden flex flex-col p-8 lg:p-12">
              {activeTab === 'docs' ? (
                <div className={`max-w-4xl mx-auto w-full rounded-2xl border shadow-2xl p-10 lg:p-16 overflow-y-auto custom-scrollbar animate-in slide-in-from-bottom-4 duration-500 ${
                  theme === 'dark' ? 'bg-[#1e293b] border-slate-800 prose-invert prose-teal' : 'bg-white border-slate-200 prose-slate'
                } prose max-w-none`}>
                  <div className="flex items-center gap-2 mb-8 px-4 py-2 bg-teal-600/10 text-teal-600 rounded-lg w-fit text-sm font-bold border border-teal-600/20">
                    <Info size={16} /> 
                    Module {activeLesson.module.split('_')[0]} • Lesson {activeLesson.id.split('_')[0]}
                  </div>
                  <ReactMarkdown>{lessonDetails?.readme || 'No documentation found.'}</ReactMarkdown>
                </div>
              ) : (
                <div className={`flex-1 max-w-5xl mx-auto w-full flex flex-col rounded-2xl border shadow-2xl overflow-hidden animate-in slide-in-from-bottom-4 duration-500 ${
                  theme === 'dark' ? 'bg-[#1e293b] border-slate-800' : 'bg-white border-slate-200'
                }`}>
                  {/* Chat Messages */}
                  <div className={`flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar ${theme === 'dark' ? '' : 'bg-slate-50/50'}`}>
                    {chatMessages.length === 0 && (
                      <div className="h-full flex flex-col items-center justify-center text-center space-y-6 opacity-50">
                        <div className="w-20 h-20 bg-teal-600/10 rounded-full flex items-center justify-center">
                          <MessageSquare size={40} className="text-teal-500" />
                        </div>
                        <div className="space-y-2">
                          <h3 className="text-2xl font-bold">Agent Playground</h3>
                          <p className="max-w-md mx-auto text-sm leading-relaxed">
                            Interact with the <strong>{activeLesson.title}</strong> agent.<br/>
                            Config: {config.provider} • {config.model || 'Default'} • Temp {config.temperature}
                          </p>
                        </div>
                        <button 
                          onClick={() => sendMessage(lessonDetails?.default_message || 'Hello!')}
                          className="px-6 py-2 bg-teal-600 hover:bg-teal-500 text-white rounded-full text-sm font-bold transition-all shadow-lg shadow-teal-600/20 flex items-center gap-2"
                        >
                          <Zap size={16} /> Start Lesson Demo
                        </button>
                      </div>
                    )}
                    {chatMessages.map((msg, i) => (
                      <div key={i} className={`flex animate-in fade-in slide-in-from-bottom-2 duration-300 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[85%] rounded-2xl px-6 py-4 shadow-xl border ${
                          msg.role === 'user' 
                            ? 'bg-teal-600 text-white border-teal-500 rounded-tr-none' 
                            : `${theme === 'dark' ? 'bg-[#0f172a] border-slate-800' : 'bg-white border-slate-200 text-slate-800'} rounded-tl-none`
                        }`}>
                          <div className={`text-[10px] font-black mb-2 opacity-50 uppercase tracking-[0.2em] flex items-center gap-2 ${msg.role === 'user' ? 'justify-end' : ''}`}>
                            {msg.role === 'user' ? (
                              <>You <div className="w-1.5 h-1.5 rounded-full bg-white/50"></div></>
                            ) : (
                              <><div className="w-1.5 h-1.5 rounded-full bg-teal-500"></div> Agent</>
                            )}
                          </div>
                          <div className={`prose prose-sm max-w-none ${msg.role === 'user' ? 'prose-invert text-white' : theme === 'dark' ? 'prose-invert' : 'prose-slate'}`}>
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                          </div>
                        </div>
                      </div>
                    ))}
                    {isStreaming && (
                      <div className="flex justify-start">
                        <div className={`flex gap-3 items-center px-6 py-3 rounded-full font-bold text-xs shadow-lg animate-pulse ${
                          theme === 'dark' ? 'bg-[#0f172a] border border-slate-800 text-teal-400' : 'bg-white border border-slate-200 text-teal-600'
                        }`}>
                          <div className="flex gap-1">
                            <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce"></span>
                            <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                            <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                          </div>
                          Agent is thinking...
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Input Bar */}
                  <div className={`p-8 border-t transition-colors duration-300 ${theme === 'dark' ? 'bg-[#0f172a]/50 border-slate-800' : 'bg-white border-slate-200'}`}>
                    <div className="relative max-w-4xl mx-auto">
                      <input 
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder={`Message ${activeLesson.title}...`}
                        className={`w-full border rounded-2xl py-5 pl-8 pr-20 focus:outline-none focus:ring-4 focus:ring-teal-500/20 transition-all font-medium text-lg leading-relaxed shadow-inner ${
                          theme === 'dark' 
                            ? 'bg-[#0f172a] border-slate-700 placeholder:text-slate-600' 
                            : 'bg-slate-50 border-slate-200 placeholder:text-slate-400'
                        }`}
                      />
                      <button 
                        onClick={() => sendMessage()}
                        disabled={isStreaming || !inputMessage.trim()}
                        className="absolute right-3 top-1/2 -translate-y-1/2 w-12 h-12 bg-teal-600 hover:bg-teal-500 disabled:opacity-50 disabled:hover:bg-teal-600 text-white rounded-xl flex items-center justify-center transition-all shadow-xl shadow-teal-600/30 active:scale-95"
                      >
                        <Play size={24} className="ml-1" />
                      </button>
                    </div>
                    <div className="mt-4 flex justify-center gap-8 text-[10px] uppercase font-black tracking-[0.2em] opacity-40">
                      <span className="flex items-center gap-2"><Terminal size={12} className="text-teal-500"/> WebSocket API</span>
                      <span className="flex items-center gap-2"><Cpu size={12} className="text-teal-500"/> {config.provider}</span>
                      <span className="flex items-center gap-2"><Zap size={12} className="text-teal-500"/> Streaming</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center space-y-12 animate-in fade-in duration-1000">
            <div className="relative">
              <div className="absolute -inset-12 bg-teal-500/20 blur-3xl rounded-full animate-pulse"></div>
              <Cpu size={140} className="text-teal-500 relative animate-float" />
            </div>
            <div className="space-y-4 max-w-xl">
              <h1 className="text-6xl font-black tracking-tighter bg-gradient-to-br from-white to-teal-500 bg-clip-text text-transparent">Agno Learning Hub</h1>
              <p className={`text-xl font-medium leading-relaxed ${theme === 'dark' ? 'text-slate-400' : 'text-slate-500'}`}>
                Explore the frontier of AI agent architecture. <br/>Interactive modules for every Agno capability.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl px-4">
              {[
                { label: "Core Concepts", desc: "Build foundation with Agents & Tools", icon: Cpu, color: 'text-teal-500' },
                { label: "Production Ops", desc: "FastAPI, Observability, Persistence", icon: Terminal, color: 'text-blue-500' },
                { label: "State Mastery", desc: "Persistent memory & Human-in-the-loop", icon: Layers, color: 'text-purple-500' },
                { label: "Team Dynamics", desc: "Multi-agent orchestration & Routing", icon: MessageSquare, color: 'text-orange-500' }
              ].map((item, i) => (
                <div key={i} className={`p-8 rounded-3xl border transition-all hover:scale-[1.02] cursor-default group ${
                  theme === 'dark' ? 'bg-[#1e293b] border-slate-800 hover:border-teal-500/50' : 'bg-white border-slate-200 hover:border-teal-500 shadow-sm hover:shadow-xl'
                }`}>
                  <item.icon className={`${item.color} mb-6 transition-transform group-hover:scale-110`} size={40} />
                  <h4 className="text-lg font-bold mb-2 uppercase tracking-tight">{item.label}</h4>
                  <p className={`text-sm leading-relaxed ${theme === 'dark' ? 'text-slate-500' : 'text-slate-500'}`}>{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Settings Overlay */}
        {showSettings && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
            <div className={`w-full max-w-md rounded-3xl shadow-2xl p-8 border animate-in zoom-in-95 duration-300 ${
              theme === 'dark' ? 'bg-[#1e293b] border-slate-700' : 'bg-white border-slate-200 text-slate-900'
            }`}>
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-2xl font-black tracking-tight">System Config</h3>
                <button onClick={() => setShowSettings(false)} className={`p-2 rounded-full ${theme === 'dark' ? 'hover:bg-slate-800' : 'hover:bg-slate-100'}`}>
                  <X size={24} />
                </button>
              </div>

              <div className="space-y-8">
                <div className="space-y-3">
                  <label className="text-xs font-black uppercase tracking-widest opacity-50">LLM Provider</label>
                  <div className="grid grid-cols-2 gap-2">
                    {PROVIDERS.map(p => (
                      <button
                        key={p.id}
                        onClick={() => setConfig({...config, provider: p.id})}
                        className={`px-4 py-2.5 rounded-xl text-xs font-bold border transition-all ${
                          config.provider === p.id 
                            ? 'bg-teal-600 text-white border-teal-500 shadow-lg shadow-teal-600/20' 
                            : `${theme === 'dark' ? 'bg-[#0f172a] border-slate-800 text-slate-400 hover:border-slate-600' : 'bg-slate-50 border-slate-200 text-slate-600 hover:border-slate-300'}`
                        }`}
                      >
                        {p.name}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <label className="text-xs font-black uppercase tracking-widest opacity-50">Model Name (Optional)</label>
                  <input 
                    type="text" 
                    value={config.model}
                    onChange={(e) => setConfig({...config, model: e.target.value})}
                    placeholder={PROVIDERS.find(p => p.id === config.provider)?.defaultModel}
                    className={`w-full border rounded-xl py-3 px-4 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-teal-500 transition-all ${
                      theme === 'dark' ? 'bg-[#0f172a] border-slate-700' : 'bg-slate-50 border-slate-200'
                    }`}
                  />
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-black uppercase tracking-widest opacity-50">Temperature</label>
                    <span className="text-sm font-bold text-teal-500">{config.temperature}</span>
                  </div>
                  <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    value={config.temperature}
                    onChange={(e) => setConfig({...config, temperature: parseFloat(e.target.value)})}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-teal-500"
                  />
                </div>

                <button 
                  onClick={() => setShowSettings(false)}
                  className="w-full py-4 bg-teal-600 hover:bg-teal-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-teal-600/30"
                >
                  Save Configuration
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: ${theme === 'dark' ? '#334155' : '#cbd5e1'};
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: ${theme === 'dark' ? '#475569' : '#94a3b8'};
        }
        pre {
          background: ${theme === 'dark' ? '#0f172a' : '#f8fafc'} !important;
          padding: 1.5rem !important;
          border-radius: 1rem !important;
          border: 1px solid ${theme === 'dark' ? '#1e293b' : '#e2e8f0'} !important;
          font-family: 'JetBrains Mono', monospace !important;
          overflow-x: auto;
        }
        code {
          font-family: 'JetBrains Mono', monospace !important;
        }
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
      `}</style>
    </div>
  )
}
