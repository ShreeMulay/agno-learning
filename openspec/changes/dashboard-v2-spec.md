# OpenSpec Proposal: Dashboard GUI Improvements v2

## Summary
Four enhancements to the Agno Learning Master Dashboard to improve the learning experience:
1. **Source Code Viewer**: Tabbed view to see Python implementation.
2. **Dynamic Model Selection**: Provider/Model combined picker with dynamic backend fetching.
3. **Hybrid Token Metrics**: Agno metrics + tiktoken estimation fallback.
4. **Multi-View Sidebar**: 5 clickable organization modes with tooltips.

---

## 1. Source Code Viewer
**Goal**: Allow learners to inspect the Python code directly in the GUI.

### Backend Requirements
- **Endpoint**: `GET /agent/{agent_id}/source`
- **Logic**: 
  1. Find agent path in catalog by ID.
  2. Read file content.
  3. Return as JSON: `{"content": "..."}`.

### Frontend Requirements
- **Component**: Add `Tabs` to the results panel: `[Output]` and `[Source Code]`.
- **Syntax Highlighting**: Use **Shiki** for server-rendered, VS Code quality highlighting.
- **Theme**: Follow the active dashboard theme (Default/Midnight/Cyberpunk).

---

## 2. Dynamic Model Selection
**Goal**: Support multiple providers with live-fetched model lists.

### Backend Requirements ✅ COMPLETE
- **Providers supported**: OpenRouter, OpenAI, Anthropic, Cerebras, Groq, Google, Ollama, HuggingFace.
- **Model Config**: Updated `shared/model_config.py` with all providers.
- **Endpoints**:
  - `GET /providers`: List available providers and their connection status.
  - `GET /models/{provider}`: Fetch current model list for a specific provider.
  - `GET /models/reload`: Force refresh of cached model lists.

### Updated Default Models
| Provider | Default Model |
|----------|---------------|
| openrouter | `anthropic/claude-haiku-4.5` |
| anthropic | `claude-sonnet-4-5` |
| openai | `gpt-4o` |
| google | `gemini-2.5-flash` |
| cerebras | `zai-glm-4.6` |
| groq | `llama-3.3-70b-versatile` |
| ollama | `llama3.2` |
| huggingface | `meta-llama/Llama-3.3-70B-Instruct` |

### Frontend Requirements - TWO DROPDOWNS (Updated)
**Important**: Use two separate dropdowns, NOT a combined dropdown.

**Reason**: HuggingFace has thousands of models. A combined dropdown would be unusable.

```
┌─────────────────────────────────────────────────────────────────┐
│  Provider: [OpenRouter ▼]    Model: [🔍 claude-haiku-4.5 ▼]  🔄 │
└─────────────────────────────────────────────────────────────────┘
```

**UI Components**:
1. **Provider Dropdown** (left)
   - Shows all 8 providers
   - Indicates active status (has API key) with ✓ or dimmed
   - On change → fetch models for that provider

2. **Model Dropdown** (right) 
   - Type-to-filter search input at top
   - Default model pinned with ⭐ icon
   - Shows loading spinner while fetching
   - Lazy-loads only when provider selected

3. **Reload Button** (🔄 icon)
   - Clears cache and refetches models
   - Shows brief "Refreshed!" toast

**Behavior**: 
1. On mount: Load saved provider/model from localStorage, or use defaults.
2. Provider change → Clear model dropdown, show loading, fetch models.
3. Model dropdown → Type-to-filter client-side.
4. Persist selection in localStorage.
5. Manual reload button clears cache via `GET /models/reload`.

---

## 3. Hybrid Token Metrics
**Goal**: Show accurate or estimated token counts for all runs.

### Strategy (Option C: Hybrid)
1. **Agno Metrics**: Always try to extract metadata from Agno's `chunk.metrics`.
2. **Fallbacks**:
   - If output tokens is 0, use `tiktoken` (cl100k_base) on backend to count characters -> tokens.
3. **Frontend Indicator**: Show values with a marker if they are estimated (e.g., `~420 (est.)`).

### Implementation
- **Backend**: Add `tiktoken` to dependencies. 
- **Response**: Add `estimated: true/false` to the metrics object in the streaming completion event.

---

## 4. Multi-View Sidebar
**Goal**: Organize 243+ agents in flexible ways.

### View Modes
| Mode | Icon | Description |
| :--- | :--- | :--- |
| **Directory** | 🗂️ | Mirrors folder structure (`07_real_world/business/sales/...`). |
| **Category** | 📁 | Groups by high-level category (Root, Business, etc.). |
| **Tools** | 🔧 | Groups by tool badges (Web, RAG, Teams, Structured). |
| **A-Z** | 🔤 | Flat alphabetical list. |
| **Search** | 🔍 | Active search results (auto-activates on type). |

### UI Requirements
- **Toggle Row**: 5 icons at the top of the sidebar.
- **Tooltips**: Show mode name on hover (e.g., "📁 By Category").
- **State**: Persist preferred mode in localStorage.

---

## Technical Dependencies
- **Backend**: `tiktoken`, `httpx` (already in use), `agno` (v2.3.18+).
- **Frontend**: `shiki`, `framer-motion` (already in use), `lucide-react`.

## Status
- **Phase 1 (Backend APIs)**: ✅ COMPLETE
  - Source code endpoint working
  - Dynamic model fetching for all 8 providers
  - Hybrid token metrics with tiktoken fallback
  - Discovery script updated with path_parts
- **Phase 2 (Frontend UI Updates)**: ✅ COMPLETE
  - Two-dropdown provider/model selector
  - Source code viewer with Shiki
  - Multi-view sidebar with icon toggle
  - HUD update for estimated metrics
