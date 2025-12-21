import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface HistoryItem {
  id: string;
  agentId: string;
  query: string;
  content: string;
  metrics: any;
  timestamp: string;
  model: string;
}

interface DashboardState {
  theme: string;
  setTheme: (theme: string) => void;
  selectedAgentId: string | null;
  setSelectedAgentId: (id: string | null) => void;
  history: HistoryItem[];
  addHistory: (item: HistoryItem) => void;
  clearHistory: () => void;
  apiKeys: Record<string, string>;
  setApiKey: (provider: string, key: string) => void;
}

export const useStore = create<DashboardState>()(
  persist(
    (set) => ({
      theme: 'default',
      setTheme: (theme) => set({ theme }),
      selectedAgentId: null,
      setSelectedAgentId: (id) => set({ selectedAgentId: id }),
      history: [],
      addHistory: (item) => set((state) => ({ history: [item, ...state.history].slice(0, 50) })),
      clearHistory: () => set({ history: [] }),
      apiKeys: {},
      setApiKey: (provider, key) => set((state) => ({ 
        apiKeys: { ...state.apiKeys, [provider]: key } 
      })),
    }),
    {
      name: 'agno-dashboard-storage',
    }
  )
);
