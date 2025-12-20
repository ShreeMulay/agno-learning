#!/bin/bash
# Sync API keys from ~/.bash_secrets to .env
# Usage: ./scripts/sync-env.sh

set -e
cd "$(dirname "$0")/.."

if [[ ! -f ~/.bash_secrets ]]; then
  echo "Error: ~/.bash_secrets not found"
  exit 1
fi

source ~/.bash_secrets

cat > .env << EOF
# Agno Learning Hub - API Keys (synced from ~/.bash_secrets)
# Generated: $(date)

# OpenRouter (RECOMMENDED)
OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-}

# Direct Provider Keys
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY:-}
GEMINI_API_KEY=${GEMINI_API_KEY:-}
GROQ_API_KEY=${GROQ_API_KEY:-}

# Additional Providers
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:-}
MISTRAL_API_KEY=${MISTRAL_API_KEY:-}
COHERE_API_KEY=${COHERE_API_KEY:-}
TOGETHER_API_KEY=${TOGETHER_API_KEY:-}
FIREWORKS_API_KEY=${FIREWORKS_API_KEY:-}
CEREBRAS_API_KEY=${CEREBRAS_API_KEY:-}
PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY:-}

# Search & Tools
EXA_API_KEY=${EXA_API_KEY:-}
SERPER_API_KEY=${SERPER_API_KEY:-}

# Local Models
OLLAMA_HOST=http://localhost:11434
EOF

echo "✓ Synced API keys to .env"
