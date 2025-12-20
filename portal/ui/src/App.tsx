import React, { useState, useEffect } from 'react'
import { 
  BookOpen, 
  Play, 
  Settings, 
  Search, 
  ChevronRight, 
  ChevronDown,
  Terminal,
  MessageSquare,
  Cpu,
  Layers,
  Code
} from 'lucide-react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const API_BASE = 'http://localhost:8000/api/v1'

export default function App() {
  const [modules, setModules] = useState([])
  const [activeLesson, setActiveLesson] = useState(null)
  const [lessonDetails, setLessonDetails] = useState(null)
  const [loading, setLoading] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [activeTab, setActiveTab] = useState('docs') // docs, playground, code

  useEffect(() => {
    fetchModules()
  }, [])

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

  const sendMessage = () => {
    if (!inputMessage.trim() || isStreaming) return

    const userMsg = { role: 'user', content: inputMessage }
    setChatMessages(prev => [...prev, userMsg])
    setInputMessage('')
    setIsStreaming(true)

    const wsProvider = `ws://localhost:8000/ws/api/v1/agents/${activeLesson.module}/${activeLesson.id}/run`
    const socket = new WebSocket(wsProvider)

    const agentMsg = { role: 'assistant', content: '' }
    setChatMessages(prev => [...prev, agentMsg])

    socket.onopen = () => {
      socket.send(JSON.stringify({
        message: inputMessage,
        provider: 'openrouter' // Default
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
        console.error("Agent error", data.content)
        setIsStreaming(false)
        socket.close()
      }
    }

    socket.onerror = (err) => {
      console.error("WebSocket error", err)
      setIsStreaming(false)
    }
  }

  return (
    <div className="flex h-screen bg-[#0f172a] text-slate-200 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-72 bg-[#1e293b] border-r border-slate-800 flex flex-col">
        <div className="p-6 border-bottom border-slate-800 flex items-center gap-3">
          <div className="w-10 h-10 bg-teal-600 rounded-lg flex items-center justify-center">
            <Cpu className="text-white" size={24} />
          </div>
          <h1 className="text-xl font-bold tracking-tight">Agno Portal</h1>
        </div>

        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
          <div className="relative mb-6">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
            <input 
              type="text" 
              placeholder="Search lessons..." 
              className="w-full bg-[#0f172a] border border-slate-700 rounded-md py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all"
            />
          </div>

          <nav className="space-y-6">
            {modules.map(mod => (
              <div key={mod.id} className="space-y-2">
                <h3 className="text-xs font-semibold uppercase text-slate-500 tracking-wider flex items-center gap-2">
                  <Layers size={14} />
                  {mod.title}
                </h3>
                <div className="space-y-1">
                  {mod.lessons.map(lesson => (
                    <button
                      key={lesson.key}
                      onClick={() => selectLesson(lesson)}
                      className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors flex items-center justify-between group ${
                        activeLesson?.key === lesson.key 
                          ? 'bg-teal-600/20 text-teal-400 font-medium border border-teal-600/30' 
                          : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
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

        <div className="p-4 border-t border-slate-800">
          <button className="flex items-center gap-3 w-full px-3 py-2 text-slate-400 hover:text-white transition-colors text-sm">
            <Settings size={18} />
            Settings
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative bg-[#0f172a]">
        {activeLesson ? (
          <>
            {/* Header */}
            <header className="h-16 border-b border-slate-800 flex items-center justify-between px-8 bg-[#0f172a]/80 backdrop-blur-md sticky top-0 z-10">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold">{activeLesson.title}</h2>
                <div className="flex bg-[#1e293b] p-1 rounded-md">
                  <button 
                    onClick={() => setActiveTab('docs')}
                    className={`px-4 py-1.5 rounded-md text-sm transition-all flex items-center gap-2 ${activeTab === 'docs' ? 'bg-teal-600 text-white shadow-lg' : 'text-slate-400 hover:text-slate-200'}`}
                  >
                    <BookOpen size={16} /> Docs
                  </button>
                  <button 
                    onClick={() => setActiveTab('playground')}
                    className={`px-4 py-1.5 rounded-md text-sm transition-all flex items-center gap-2 ${activeTab === 'playground' ? 'bg-teal-600 text-white shadow-lg' : 'text-slate-400 hover:text-slate-200'}`}
                  >
                    <Play size={16} /> Playground
                  </button>
                </div>
              </div>
              
              <div className="flex items-center gap-4 text-xs text-slate-500">
                <div className="flex items-center gap-2 px-3 py-1 bg-slate-800 rounded-full">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  API Online
                </div>
              </div>
            </header>

            {/* Content Area */}
            <div className="flex-1 overflow-hidden flex flex-col p-8">
              {activeTab === 'docs' ? (
                <div className="max-w-4xl mx-auto w-full bg-[#1e293b] rounded-xl border border-slate-800 shadow-2xl p-10 overflow-y-auto custom-scrollbar prose prose-invert prose-teal">
                  <ReactMarkdown>{lessonDetails?.readme || 'No documentation found.'}</ReactMarkdown>
                </div>
              ) : (
                <div className="flex-1 max-w-5xl mx-auto w-full flex flex-col bg-[#1e293b] rounded-xl border border-slate-800 shadow-2xl overflow-hidden">
                  {/* Chat Messages */}
                  <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                    {chatMessages.length === 0 && (
                      <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-50">
                        <MessageSquare size={48} className="text-teal-500 mb-2" />
                        <h3 className="text-xl font-medium">Agent Playground</h3>
                        <p className="max-w-xs mx-auto text-sm">Send a message to interact with the {activeLesson.title} agent in real-time.</p>
                      </div>
                    )}
                    {chatMessages.map((msg, i) => (
                      <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-2xl px-5 py-3 shadow-lg ${
                          msg.role === 'user' 
                            ? 'bg-teal-600 text-white rounded-tr-none' 
                            : 'bg-[#0f172a] border border-slate-800 rounded-tl-none'
                        }`}>
                          <div className="text-xs font-bold mb-1 opacity-50 uppercase tracking-tighter">
                            {msg.role === 'user' ? 'You' : 'Agent'}
                          </div>
                          <div className="prose prose-sm prose-invert max-w-none">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                          </div>
                        </div>
                      </div>
                    ))}
                    {isStreaming && (
                      <div className="flex justify-start">
                        <div className="flex gap-1 items-center px-4 py-2 bg-[#0f172a] border border-slate-800 rounded-full italic text-xs text-slate-500">
                          <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce"></span>
                          <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                          <span className="w-1.5 h-1.5 bg-teal-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                          Agent is thinking...
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Input Bar */}
                  <div className="p-6 bg-[#0f172a]/50 border-t border-slate-800">
                    <div className="relative">
                      <input 
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder={`Talk to ${activeLesson.title}...`}
                        className="w-full bg-[#0f172a] border border-slate-700 rounded-full py-4 pl-6 pr-16 focus:outline-none focus:ring-2 focus:ring-teal-500 transition-all font-medium placeholder:text-slate-600"
                      />
                      <button 
                        onClick={sendMessage}
                        disabled={isStreaming || !inputMessage.trim()}
                        className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 bg-teal-600 hover:bg-teal-500 disabled:opacity-50 disabled:hover:bg-teal-600 text-white rounded-full flex items-center justify-center transition-all shadow-lg"
                      >
                        <Play size={18} className="ml-0.5" />
                      </button>
                    </div>
                    <div className="mt-3 flex justify-center gap-6 text-[10px] text-slate-500 uppercase font-bold tracking-widest">
                      <span className="flex items-center gap-1.5"><Terminal size={12} className="text-teal-600"/> Streaming Active</span>
                      <span className="flex items-center gap-1.5"><Code size={12} className="text-teal-600"/> Agent Ready</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center space-y-8 animate-in fade-in duration-700">
            <div className="relative">
              <div className="absolute -inset-4 bg-teal-500/20 blur-2xl rounded-full"></div>
              <Cpu size={120} className="text-teal-500 relative" />
            </div>
            <div className="space-y-4 max-w-lg">
              <h1 className="text-5xl font-black text-white tracking-tight">Agno Learning Hub</h1>
              <p className="text-xl text-slate-400 font-medium">Select a module from the explorer to begin your agentic journey.</p>
            </div>
            <div className="grid grid-cols-2 gap-4 w-full max-w-2xl px-4">
              {[
                { label: "Core Concepts", desc: "Agents, Tools, Memory", icon: Cpu },
                { label: "Production Ready", desc: "FastAPI, Monitoring, DBs", icon: Terminal },
                { label: "Workflow Eng", desc: "Human-in-the-loop, States", icon: Layers },
                { label: "Multi-Agent", desc: "Teams, Roleplay, Routing", icon: MessageSquare }
              ].map((item, i) => (
                <div key={i} className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800 text-left hover:border-teal-500/50 transition-all group">
                  <item.icon className="text-teal-500 mb-4 group-hover:scale-110 transition-transform" size={32} />
                  <h4 className="font-bold text-white mb-1">{item.label}</h4>
                  <p className="text-sm text-slate-500">{item.desc}</p>
                </div>
              ))}
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
          background: #334155;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #475569;
        }
        pre {
          background: #0f172a !important;
          padding: 1.5rem !important;
          border-radius: 0.75rem !important;
          border: 1px solid #1e293b !important;
        }
      `}</style>
    </div>
  )
}
