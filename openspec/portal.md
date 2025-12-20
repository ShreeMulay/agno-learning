# OpenSpec: Agno Learning Portal

## 1. Overview
The Agno Learning Portal is a full-stack dashboard for exploring and interacting with Agno framework lessons. It provides a bridge between the CLI-based lessons and a modern web interface.

## 2. System Architecture

### 2.1 Backend (FastAPI + AgentOS)
- **Engine**: FastAPI 0.115+
- **Registry**: Dynamic module loader that imports `get_agent()` from module files.
- **Endpoints**:
  - `GET /api/v1/modules`: List all modules and lessons.
  - `GET /api/v1/lessons/{module}/{lesson}`: Get lesson details (README, metadata).
  - `GET /api/v1/lessons/{module}/{lesson}/code`: Get source code of the lesson.
  - `POST /api/v1/agents/{module}/{lesson}/run`: Execute agent (streaming via SSE/WebSockets).
  - `GET /api/v1/sessions`: List past sessions.

### 2.2 Frontend (React 19)
- **Framework**: React 19 (Server Components where applicable).
- **Styling**: Tailwind CSS v4.
- **Components**: Shadcn/ui v4.
- **State**: Zustand for navigation and basic config.
- **Communication**: TanStack Query for data fetching, WebSockets for chat.

## 3. Component Specification

### 3.1 Sidebar (Navigation)
- Collapsible sections for each Module (00-07).
- Search bar for filtering lessons.
- Progress indicators.

### 3.2 Documentation Viewer
- Render `README.md` using `react-markdown`.
- Syntax highlighting for code blocks.
- Link to playground.

### 3.3 Chat Playground
- Message list with Markdown support.
- Input bar with multi-line support.
- **Trace Panel**: Collapsible panel showing:
  - Tool calls and results.
  - Model parameters used.
  - Token consumption and duration.

### 3.4 Settings
- Selection of Model Provider (OpenRouter default).
- API Key management (session storage).
- Temperature and Max Tokens sliders.

## 4. Automation & Quality
- **Inngest**: Background sync job triggers on file changes to update the lesson registry.
- **Tests**: Vitest for frontend, Pytest for backend API.

## 5. Security
- API keys are handled in-memory or session storage; never persisted on the backend unless explicitly configured in `.env`.
- CORS restricted to the development environment.
