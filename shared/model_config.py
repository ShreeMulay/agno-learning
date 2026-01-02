"""
Unified LLM Configuration for Agno Learning Hub.

Supports: OpenRouter, OpenAI, Anthropic, Google, Cerebras, Groq, Ollama, HuggingFace

Usage:
    from shared.model_config import get_model, list_providers
    
    model = get_model()                      # Default (OpenRouter)
    model = get_model("anthropic")           # Specific provider
    model = get_model("openrouter", "deepseek/deepseek-chat-v3")  # Custom model
"""

import os
from pathlib import Path
from typing import Optional


def load_bash_secrets() -> int:
    """
    Load API keys from ~/.bash_secrets if not already in environment.
    
    This is the preferred way to manage API keys - they're loaded once
    at module import and available to all examples.
    
    File format (standard bash exports):
        export OPENROUTER_API_KEY="sk-or-v1-..."
        export ANTHROPIC_API_KEY="sk-ant-..."
    
    Returns:
        Number of keys loaded
    """
    secrets_file = Path.home() / ".bash_secrets"
    loaded = 0
    
    if not secrets_file.exists():
        return 0
    
    try:
        for line in secrets_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith("export "):
                key_val = line[7:].split("=", 1)
                if len(key_val) == 2:
                    key = key_val[0].strip()
                    val = key_val[1].strip()
                    if (val.startswith('"') and val.endswith('"')) or \
                       (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    if key and key not in os.environ:
                        os.environ[key] = val
                        loaded += 1
    except Exception:
        pass
    
    return loaded


_secrets_loaded = load_bash_secrets()
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Default provider - OpenRouter provides access to all models
DEFAULT_PROVIDER = "openrouter"

# Provider capability flags
# - tools: Supports function calling / tool use
# - structured_output: Supports response_format for JSON schema
# - streaming: Supports streaming responses
# - vision: Supports image inputs

# Provider configurations
PROVIDER_CONFIGS = {
    "openrouter": {
        "module": "agno.models.openrouter",
        "class": "OpenRouter",
        "default_model": "anthropic/claude-haiku-4.5",
        "api_key_env": "OPENROUTER_API_KEY",
        "description": "Multi-model access - Claude, GPT, Llama via OpenRouter",
        "capabilities": ["tools", "structured_output", "streaming", "vision"],
    },
    "openai": {
        "module": "agno.models.openai",
        "class": "OpenAIChat",
        "default_model": "gpt-4o",
        "api_key_env": "OPENAI_API_KEY",
        "description": "OpenAI GPT models",
        "capabilities": ["tools", "structured_output", "streaming", "vision"],
    },
    "anthropic": {
        "module": "agno.models.anthropic",
        "class": "Claude",
        "default_model": "claude-sonnet-4-5",
        "api_key_env": "ANTHROPIC_API_KEY",
        "description": "Anthropic Claude models",
        "capabilities": ["tools", "structured_output", "streaming", "vision"],
    },
    "google": {
        "module": "agno.models.google",
        "class": "Gemini",
        "default_model": "gemini-2.5-flash",
        "api_key_env": "GOOGLE_AI_API_KEY",
        "description": "Google Gemini models",
        "capabilities": ["tools", "structured_output", "streaming", "vision"],
    },
    "cerebras": {
        "module": "agno.models.cerebras",
        "class": "Cerebras",
        "default_model": "llama-3.3-70b",
        "api_key_env": "CEREBRAS_API_KEY",
        "description": "Ultra-fast inference (chat only, no tools)",
        "capabilities": ["streaming"],  # No tools or structured_output support
        "warning": "Cerebras only supports basic chat. Agents with tools will fail.",
    },
    "groq": {
        "module": "agno.models.groq",
        "class": "Groq",
        "default_model": "llama-3.3-70b-versatile",
        "api_key_env": "GROQ_API_KEY",
        "description": "Fast inference via Groq",
        "capabilities": ["tools", "streaming"],  # Tools yes, structured_output limited
    },
    "ollama": {
        "module": "agno.models.ollama",
        "class": "Ollama",
        "default_model": "llama3.2",
        "api_key_env": "OLLAMA_HOST",  # Not really a key, but connection info
        "description": "Local models via Ollama",
        "capabilities": ["tools", "streaming"],  # Depends on model
    },
    "huggingface": {
        "module": "agno.models.huggingface",
        "class": "HuggingFace",
        "default_model": "meta-llama/Llama-3.3-70B-Instruct",
        "api_key_env": "HUGGINGFACE_API_KEY",
        "description": "Open-source models via HuggingFace",
        "capabilities": ["streaming"],  # Most HF models don't support tools natively
        "warning": "Tool support varies by model. Basic chat recommended.",
    },
}

# Export for use in argparse choices
SUPPORTED_PROVIDERS = list(PROVIDER_CONFIGS.keys())


def list_providers() -> dict[str, str]:
    """Return dict of provider names to descriptions."""
    return {name: cfg["description"] for name, cfg in PROVIDER_CONFIGS.items()}


def check_api_key(provider: str) -> tuple[bool, str]:
    """
    Check if API key is available for a provider.
    
    Returns:
        Tuple of (is_available, env_var_name)
    """
    config = PROVIDER_CONFIGS.get(provider)
    if not config:
        return False, ""
    
    env_var = config["api_key_env"]
    return bool(os.getenv(env_var)), env_var


def get_model(
    provider: str = DEFAULT_PROVIDER,
    model: Optional[str] = None,
    **kwargs,
):
    """
    Get an LLM model instance for the specified provider.
    
    Args:
        provider: Provider name (openrouter, openai, anthropic, google, groq, ollama)
        model: Override default model ID
        **kwargs: Additional model arguments (temperature, etc.)
        
    Returns:
        Configured Agno model instance
        
    Raises:
        ValueError: Unknown provider
        EnvironmentError: Missing API key
        ImportError: Agno or provider module not installed
        
    Example:
        >>> model = get_model()  # OpenRouter with Claude 3.5 Sonnet
        >>> model = get_model("openai", "gpt-4o-mini")
        >>> model = get_model("anthropic", temperature=0.7)
    """
    provider = provider.lower().strip()
    
    if provider not in PROVIDER_CONFIGS:
        available = ", ".join(SUPPORTED_PROVIDERS)
        raise ValueError(f"Unknown provider: '{provider}'. Available: {available}")
    
    config = PROVIDER_CONFIGS[provider]
    
    # Check API key (except for Ollama which uses host)
    if provider != "ollama":
        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise EnvironmentError(
                f"API key not found for {provider}. "
                f"Set {config['api_key_env']} in your environment or .env file."
            )
    
    # Dynamically import the model class
    try:
        import importlib
        module = importlib.import_module(config["module"])
        model_class = getattr(module, config["class"])
    except ImportError as e:
        raise ImportError(
            f"Failed to import {provider} model. "
            f"Make sure agno is installed: uv pip install agno"
        ) from e
    
    # Build model kwargs
    model_id = model or config["default_model"]
    model_kwargs = {"id": model_id, **kwargs}
    
    # For Ollama, add host if specified
    if provider == "ollama":
        host = os.getenv("OLLAMA_HOST")
        if host:
            model_kwargs["host"] = host
    
    return model_class(**model_kwargs)


def add_model_args(parser) -> None:
    """
    Add common model arguments to an argparse parser.
    
    Args:
        parser: argparse.ArgumentParser instance
        
    Usage:
        parser = argparse.ArgumentParser()
        add_model_args(parser)
        args = parser.parse_args()
        model = get_model(args.provider, args.model, temperature=args.temperature)
    """
    parser.add_argument(
        "--provider", "-p",
        type=str,
        choices=SUPPORTED_PROVIDERS,
        default=DEFAULT_PROVIDER,
        help=f"LLM provider to use (default: {DEFAULT_PROVIDER})",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="Model ID to use (provider-specific, uses default if not specified)",
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Model temperature (0.0-1.0, default: 0.7)",
    )


if __name__ == "__main__":
    # Print provider info when run directly
    print("\n" + "=" * 60)
    print("Agno Learning Hub - Available LLM Providers")
    print("=" * 60 + "\n")
    
    for name, desc in list_providers().items():
        has_key, env_var = check_api_key(name)
        status = "[+]" if has_key else "[-]"
        print(f"  {status} {name:12} - {desc}")
        if not has_key:
            print(f"      Set: {env_var}")
    
    print(f"\n  Default provider: {DEFAULT_PROVIDER}")
    print(f"  Default model: {PROVIDER_CONFIGS[DEFAULT_PROVIDER]['default_model']}")
    print("\n" + "=" * 60 + "\n")
