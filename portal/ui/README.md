# Agno Learning Portal UI

A React 19 frontend for exploring and interacting with Agno agents.

## Features

- **Module Explorer**: Browse all curriculum modules and lessons.
- **Interactive Playground**: Chat with agents in real-time with streaming support.
- **Documentation Viewer**: Read lesson READMEs with full markdown support.
- **Theme Switching**: Toggle between premium Light and Dark modes.
- **Auto-run**: Instantly launch lesson examples in the playground.
- **Live Config**: Adjust Model Provider, Temperature, and Tokens on the fly.

## Development

```bash
# Install dependencies
bun install

# Start development server
bun run dev
```

## Tech Stack

- **Framework**: React 19
- **Styling**: Tailwind CSS v4
- **Components**: Shadcn/ui v4 (custom implementations)
- **Icons**: Lucide React
- **API**: Axios + TanStack Query
- **Real-time**: WebSockets
