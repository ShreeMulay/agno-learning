'use client';

import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { useStore } from '../store/useStore';
import { 
  Search, 
  Settings2, 
  Terminal, 
  Zap, 
  LayoutDashboard, 
  ChevronRight, 
  ChevronDown,
  Activity,
  History as HistoryIcon,
  Palette,
  Play,
  Cpu,
  Globe,
  Database,
  Users,
  Box,
  Code
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

interface Agent {
  id: string;
  name: string;
  category: string;
  subcategory: string | null;
  description: string;
  params: any[];
  tools: string[];
  type: string;
}

export default function Dashboard() {
  const { theme, setTheme, selectedAgentId, setSelectedAgentId, addHistory } = useStore();
  const [catalog, setCatalog] = useState<Agent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [search, setSearch] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [streamedContent, setStreamedContent] = useState('');
  const [metrics, setMetrics] = useState<any>(null);
  const [params, setParams] = useState<Record<string, string>>({});
  const [expandedCategories, setCollapsedCategories] = useState<Record<string, boolean>>({});
  const [modelConfig, setModelConfig] = useState({
    provider: 'openrouter',
    model: 'anthropic/claude-3.5-sonnet',
    temperature: 0.7
  });

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    axios.get(`${API_BASE}/catalog`).then(res => {
      setCatalog(res.data);
      // Expand first few categories by default
      const cats: Record<string, boolean> = {};
      res.data.slice(0, 5).forEach((a: Agent) => cats[a.category] = true);
      setCollapsedCategories(cats);
    });
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    if (selectedAgentId) {
      const agent = catalog.find(a => a.id === selectedAgentId);
      if (agent) {
        setSelectedAgent(agent);
        // Reset params with DEFAULTS from catalog
        const initial: Record<string, string> = {};
        agent.params.forEach(p => initial[p.name] = p.default || '');
        setParams(initial);
        setStreamedContent('');
        setMetrics(null);
      }
    }
  }, [selectedAgentId, catalog]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [streamedContent]);

  const handleRun = async () => {
    if (!selectedAgent) return;
    setIsRunning(true);
    setStreamedContent('');
    setMetrics(null);

    try {
      const response = await fetch(`${API_BASE}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_id: selectedAgent.id,
          provider: modelConfig.provider,
          model: modelConfig.model,
          temperature: modelConfig.temperature,
          params
        })
      });

      const reader = response.body?.getReader();
      if (!reader) return;

      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += new TextDecoder().decode(value);
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.event === 'chunk') {
                setStreamedContent(prev => prev + data.content);
              } else if (data.event === 'complete') {
                setMetrics(data.metrics);
                addHistory({
                  id: Math.random().toString(36).substr(2, 9),
                  agentId: selectedAgent.id,
                  query: params.query || params.topic || 'Run',
                  content: data.content,
                  metrics: data.metrics,
                  timestamp: new Date().toISOString(),
                  model: modelConfig.model
                });
              } else if (data.event === 'error') {
                setStreamedContent(prev => prev + `\n\n❌ ERROR: ${data.message}`);
              }
            } catch (e) {
              console.error("Parse error", e);
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setStreamedContent(prev => prev + `\n\n❌ Connection Error: ${err}`);
    } finally {
      setIsRunning(false);
    }
  };

  const toggleCategory = (cat: string) => {
    setCollapsedCategories(prev => ({ ...prev, [cat]: !prev[cat] }));
  };

  const groupedCatalog = catalog.reduce((acc: any, agent) => {
    if (!acc[agent.category]) acc[agent.category] = [];
    acc[agent.category].push(agent);
    return acc;
  }, {});

  const filteredGroups = Object.keys(groupedCatalog).reduce((acc: any, cat) => {
    const matched = groupedCatalog[cat].filter((a: Agent) => 
      a.name.toLowerCase().includes(search.toLowerCase()) || 
      cat.toLowerCase().includes(search.toLowerCase())
    );
    if (matched.length > 0) acc[cat] = matched;
    return acc;
  }, {});

  const renderToolIcon = (tool: string) => {
    switch (tool) {
      case 'web': return <Globe size={10} className="text-blue-400" />;
      case 'rag': return <Database size={10} className="text-amber-400" />;
      case 'team': return <Users size={10} className="text-purple-400" />;
      case 'structured': return <Code size={10} className="text-green-400" />;
      default: return null;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden text-sm font-light">
      {/* Sidebar */}
      <div className="w-80 bg-muted/40 border-r border-border flex flex-col">
        <div className="p-6 border-b border-border">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center text-primary shadow-inner">
              <Zap size={20} />
            </div>
            <div>
              <h1 className="font-semibold text-lg leading-tight uppercase tracking-tight">Agno Hub</h1>
              <span className="text-primary text-[10px] uppercase font-bold tracking-[0.2em]">Master Console</span>
            </div>
          </div>
          
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input 
              type="text" 
              placeholder="Search catalog..." 
              className="w-full bg-background border border-border rounded-lg pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-primary transition-all"
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-3 scrollbar-hide space-y-2">
          {Object.keys(filteredGroups).sort().map(cat => (
            <div key={cat} className="space-y-1">
              <button 
                onClick={() => toggleCategory(cat)}
                className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-muted text-muted-foreground font-semibold text-[11px] uppercase tracking-widest transition-colors"
              >
                <span>{cat}</span>
                {expandedCategories[cat] ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              </button>
              
              <AnimatePresence initial={false}>
                {expandedCategories[cat] && (
                  <motion.div 
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="overflow-hidden space-y-0.5 ml-1 border-l border-border/50"
                  >
                    {filteredGroups[cat].map((agent: Agent) => (
                      <button
                        key={agent.id}
                        onClick={() => setSelectedAgentId(agent.id)}
                        className={`w-full text-left p-2.5 pl-4 rounded-lg transition-all flex items-center gap-2 group relative ${
                          selectedAgentId === agent.id ? 'bg-primary/15 text-primary' : 'hover:bg-muted/60 text-muted-foreground hover:text-foreground'
                        }`}
                      >
                        <div className="flex-1 min-w-0">
                          <div className="truncate font-medium text-xs">{agent.name}</div>
                        </div>
                        <div className="flex gap-1">
                          {agent.tools.map(t => (
                            <div key={t} title={t}>{renderToolIcon(t)}</div>
                          ))}
                        </div>
                        {selectedAgentId === agent.id && (
                          <motion.div layoutId="active-pill" className="absolute left-0 w-1 h-4 bg-primary rounded-full" />
                        )}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-border bg-background/40 flex items-center justify-between">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Box size={14} />
            <span className="text-[10px] font-bold uppercase tracking-wider">{catalog.length} Agents Loaded</span>
          </div>
          <button 
            onClick={() => setTheme(theme === 'midnight' ? 'default' : theme === 'default' ? 'cyberpunk' : 'midnight')} 
            className="p-2 hover:bg-muted rounded-lg transition-colors text-muted-foreground"
          >
            <Palette size={16} />
          </button>
        </div>
      </div>

      {/* Main Workspace */}
      <div className="flex-1 flex flex-col bg-background">
        {selectedAgent ? (
          <>
            <div className="h-16 border-b border-border flex items-center justify-between px-8 bg-background/50 backdrop-blur-md sticky top-0 z-10">
               <div className="flex items-center gap-4">
                  <div>
                    <h2 className="font-bold text-lg">{selectedAgent.name}</h2>
                    <div className="text-[10px] uppercase tracking-widest text-primary font-bold">
                      {selectedAgent.category} {selectedAgent.subcategory && `> ${selectedAgent.subcategory}`}
                    </div>
                  </div>
                  <div className="h-8 w-px bg-border mx-2"></div>
                  <div className="flex items-center gap-6">
                    <div className="flex flex-col">
                      <span className="text-[9px] text-muted-foreground uppercase font-bold tracking-tighter">LLM Provider</span>
                      <select 
                        className="bg-transparent text-xs font-semibold focus:outline-none text-primary cursor-pointer hover:underline"
                        value={modelConfig.provider}
                        onChange={e => setModelConfig({...modelConfig, provider: e.target.value})}
                      >
                        <option value="openrouter">OpenRouter</option>
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                        <option value="google">Google</option>
                      </select>
                    </div>
                  </div>
               </div>
               
               <button 
                onClick={handleRun}
                disabled={isRunning}
                className="bg-primary text-primary-foreground px-8 py-2.5 rounded-xl font-bold flex items-center gap-2 hover:brightness-110 active:scale-95 transition-all disabled:opacity-50 shadow-lg shadow-primary/25"
               >
                 {isRunning ? <Activity size={18} className="animate-spin" /> : <Play size={18} fill="currentColor" />}
                 {isRunning ? 'AGENT THINKING...' : 'RUN AGENT'}
               </button>
            </div>

            <div className="flex-1 overflow-hidden flex">
               {/* Controls */}
               <div className="w-96 border-r border-border p-8 overflow-y-auto bg-muted/10">
                  <div className="mb-10 p-5 bg-primary/5 border border-primary/10 rounded-2xl">
                    <div className="flex items-center gap-2 mb-3 text-primary text-xs font-bold uppercase tracking-widest">
                      <LayoutDashboard size={14} />
                      Mission Brief
                    </div>
                    <p className="text-muted-foreground text-xs leading-relaxed italic">{selectedAgent.description}</p>
                  </div>

                  <div className="space-y-8">
                    <div className="flex items-center justify-between border-b border-border pb-2">
                      <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-muted-foreground">Parameters</h3>
                      <Zap size={12} className="text-primary" />
                    </div>
                    {selectedAgent.params.map(param => (
                      <div key={param.name} className="space-y-3">
                        <div className="flex items-center justify-between">
                          <label className="text-[10px] font-bold text-foreground/80 uppercase tracking-widest">{param.name}</label>
                          {param.required && <span className="text-[8px] bg-primary/20 text-primary px-1.5 py-0.5 rounded uppercase font-black">Required</span>}
                        </div>
                        {param.ui_type === 'textarea' ? (
                          <textarea 
                            className="w-full bg-background border border-border rounded-xl p-4 text-xs min-h-[160px] focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all font-sans shadow-sm"
                            placeholder={`Enter ${param.name}...`}
                            value={params[param.name] || ''}
                            onChange={e => setParams({...params, [param.name]: e.target.value})}
                          />
                        ) : (
                          <input 
                            type="text"
                            className="w-full bg-background border border-border rounded-xl p-4 text-xs focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all shadow-sm"
                            placeholder={`Enter ${param.name}...`}
                            value={params[param.name] || ''}
                            onChange={e => setParams({...params, [param.name]: e.target.value})}
                          />
                        )}
                      </div>
                    ))}
                  </div>
               </div>

               {/* Console & Result */}
               <div className="flex-1 flex flex-col relative overflow-hidden">
                  <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,var(--primary),transparent)] opacity-[0.03] pointer-events-none"></div>
                  
                  <div ref={scrollRef} className="p-10 flex-1 overflow-y-auto space-y-8 custom-scrollbar">
                    {streamedContent || isRunning || metrics ? (
                      <div className="max-w-4xl mx-auto space-y-8">
                        {/* Streamed Output */}
                        <div className="bg-background border border-border rounded-3xl shadow-2xl overflow-hidden min-h-[400px] flex flex-col border-t-primary/20 border-t-2">
                           <div className="bg-muted/30 px-6 py-4 flex items-center justify-between border-b border-border">
                              <div className="flex items-center gap-3">
                                <Terminal size={16} className="text-primary" />
                                <span className="font-mono text-[10px] font-bold uppercase tracking-[0.3em]">Neural Link Status: {isRunning ? 'Receiving' : 'Complete'}</span>
                              </div>
                              <div className="flex gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-red-500/20"></div>
                                <div className="w-2.5 h-2.5 rounded-full bg-amber-500/20"></div>
                                <div className="w-2.5 h-2.5 rounded-full bg-green-500/20"></div>
                              </div>
                           </div>
                           <div className="p-10 prose prose-invert prose-indigo max-w-none flex-1">
                              <pre className="whitespace-pre-wrap font-sans text-[15px] leading-[1.8] text-foreground/90 font-light selection:bg-primary/30 antialiased">
                                {streamedContent}
                                {isRunning && (
                                  <motion.span 
                                    animate={{ opacity: [0, 1, 0] }}
                                    transition={{ repeat: Infinity, duration: 0.8 }}
                                    className="inline-block w-2.5 h-5 bg-primary ml-1 translate-y-1 rounded-sm"
                                  />
                                )}
                              </pre>
                           </div>
                        </div>

                        {/* Performance HUD */}
                        <AnimatePresence>
                          {metrics && (
                            <motion.div 
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              className="grid grid-cols-4 gap-6"
                            >
                              {[
                                { label: 'Response Time', value: `${metrics.duration.toFixed(2)}s`, icon: Activity, color: 'text-blue-400' },
                                { label: 'Inference Velocity', value: `${metrics.tps.toFixed(1)} T/S`, icon: Cpu, color: 'text-emerald-400' },
                                { label: 'Compute Usage', value: `${metrics.output_tokens} TOKENS`, icon: Terminal, color: 'text-indigo-400' },
                                { label: 'Resource Cost', value: `$${metrics.cost.toFixed(5)}`, icon: Zap, color: 'text-amber-400' }
                              ].map(m => (
                                <div key={m.label} className="bg-background/80 backdrop-blur border border-border p-5 rounded-2xl flex flex-col gap-3 shadow-xl">
                                  <div className={`p-2 w-fit bg-muted rounded-xl ${m.color}`}><m.icon size={18} /></div>
                                  <div>
                                    <div className="text-[9px] uppercase text-muted-foreground font-black tracking-[0.2em] mb-1">{m.label}</div>
                                    <div className="text-lg font-bold tabular-nums tracking-tight">{m.value}</div>
                                  </div>
                                </div>
                              ))}
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center text-muted-foreground/20 gap-6">
                        <div className="relative group">
                          <LayoutDashboard size={120} className="group-hover:text-primary/20 transition-colors" />
                          <motion.div 
                            animate={{ rotate: 360 }}
                            transition={{ repeat: Infinity, duration: 10, ease: "linear" }}
                            className="absolute -inset-4 border-2 border-dashed border-primary/10 rounded-full"
                          />
                        </div>
                        <p className="tracking-[0.5em] uppercase text-xs font-black">System Ready for Linkage</p>
                      </div>
                    )}
                  </div>
               </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center gap-8 relative overflow-hidden">
             <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--primary),transparent)] opacity-[0.05]"></div>
             
             <motion.div 
               animate={{ 
                 y: [0, -10, 0],
                 rotate: [0, 2, -2, 0]
               }}
               transition={{ repeat: Infinity, duration: 6 }}
               className="w-32 h-32 rounded-[2.5rem] bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center border border-primary/20 shadow-2xl backdrop-blur-sm"
             >
                <Zap size={64} className="text-primary drop-shadow-[0_0_15px_rgba(var(--primary-rgb),0.5)]" />
             </motion.div>
             <div className="text-center space-y-3 z-10">
               <h2 className="text-2xl font-black uppercase tracking-[0.3em] text-foreground">Agno Master Intelligence</h2>
               <p className="text-muted-foreground/60 text-xs uppercase tracking-[0.5em] font-bold">Select Interface from Catalog to Begin Operational Sequence</p>
             </div>
          </div>
        )}
      </div>
    </div>
  );
}
