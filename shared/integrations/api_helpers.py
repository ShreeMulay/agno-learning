"""
API Helper Functions for Agno Learning Hub.

Provides common patterns for working with external APIs:
- API key management
- Rate limiting
- Response caching
- Graceful fallbacks
"""

import functools
import os
import time
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


# =============================================================================
# API Key Management
# =============================================================================

# Map of service names to environment variable names
API_KEY_MAP = {
    # LLM Providers
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_AI_API_KEY",
    "groq": "GROQ_API_KEY",
    
    # Search & Data
    "duckduckgo": None,  # Free, no key needed
    "newsapi": "NEWSAPI_KEY",
    "serper": "SERPER_API_KEY",
    "exa": "EXA_API_KEY",
    
    # Finance
    "alphavantage": "ALPHAVANTAGE_API_KEY",
    "polygon": "POLYGON_API_KEY",
    
    # Weather
    "openweather": "OPENWEATHER_API_KEY",
    
    # Communication
    "slack": "SLACK_BOT_TOKEN",
    "twilio": "TWILIO_AUTH_TOKEN",
    "sendgrid": "SENDGRID_API_KEY",
    
    # Productivity
    "gmail": "GMAIL_CREDENTIALS_PATH",
    "gcalendar": "GCALENDAR_CREDENTIALS_PATH",
    "notion": "NOTION_API_KEY",
    
    # Development
    "github": "GITHUB_TOKEN",
    "linear": "LINEAR_API_KEY",
    "jira": "JIRA_API_TOKEN",
    
    # CRM
    "hubspot": "HUBSPOT_API_KEY",
    "salesforce": "SALESFORCE_ACCESS_TOKEN",
    
    # Database
    "postgres": "DATABASE_URL",
    "supabase": "SUPABASE_URL",
    
    # Storage
    "s3": "AWS_ACCESS_KEY_ID",
    "gcs": "GOOGLE_CLOUD_CREDENTIALS",
}


def get_api_key(service: str, required: bool = True) -> Optional[str]:
    """
    Get API key for a service from environment.
    
    Args:
        service: Service name (e.g., "openrouter", "github")
        required: If True, raises ValueError when key missing
        
    Returns:
        API key string or None if not required and missing
        
    Raises:
        ValueError: If required and key is missing
    """
    service = service.lower()
    
    if service not in API_KEY_MAP:
        if required:
            raise ValueError(f"Unknown service: {service}")
        return None
    
    env_var = API_KEY_MAP[service]
    
    # Some services don't need keys
    if env_var is None:
        return ""
    
    key = os.getenv(env_var)
    
    if not key and required:
        raise ValueError(
            f"API key not found for {service}. "
            f"Set {env_var} in your .env file."
        )
    
    return key


def check_api_available(service: str) -> tuple[bool, str]:
    """
    Check if an API is available (has credentials).
    
    Args:
        service: Service name
        
    Returns:
        Tuple of (is_available, env_var_name)
    """
    service = service.lower()
    
    if service not in API_KEY_MAP:
        return False, f"Unknown: {service}"
    
    env_var = API_KEY_MAP[service]
    
    if env_var is None:
        return True, "No key needed"
    
    return bool(os.getenv(env_var)), env_var


def list_available_apis() -> dict[str, bool]:
    """
    List all known APIs and their availability.
    
    Returns:
        Dict of service name -> is_available
    """
    return {
        service: check_api_available(service)[0]
        for service in API_KEY_MAP
    }


# =============================================================================
# Rate Limiting
# =============================================================================

def with_rate_limit(
    calls_per_second: float = 1.0,
    burst: int = 1,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to rate limit function calls.
    
    Args:
        calls_per_second: Max calls per second
        burst: Allow this many immediate calls
        
    Example:
        @with_rate_limit(calls_per_second=2)
        def call_api(query):
            return api.search(query)
    """
    min_interval = 1.0 / calls_per_second
    last_called: list[float] = []
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            now = time.time()
            
            # Clean up old timestamps
            while last_called and now - last_called[0] > 1.0:
                last_called.pop(0)
            
            # Check if we need to wait
            if len(last_called) >= burst:
                elapsed = now - last_called[-1]
                if elapsed < min_interval:
                    time.sleep(min_interval - elapsed)
            
            last_called.append(time.time())
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# =============================================================================
# Response Caching
# =============================================================================

# Simple in-memory cache
_cache: dict[str, tuple[Any, float]] = {}


def cache_response(
    ttl_seconds: int = 300,
    max_size: int = 100,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator to cache function responses.
    
    Args:
        ttl_seconds: Cache TTL in seconds (default: 5 minutes)
        max_size: Maximum cache entries
        
    Example:
        @cache_response(ttl_seconds=3600)
        def fetch_weather(city):
            return api.get_weather(city)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{args}:{sorted(kwargs.items())}"
            now = time.time()
            
            # Check cache
            if key in _cache:
                value, timestamp = _cache[key]
                if now - timestamp < ttl_seconds:
                    return value
            
            # Call function
            result = func(*args, **kwargs)
            
            # Store in cache
            _cache[key] = (result, now)
            
            # Cleanup if cache too large
            if len(_cache) > max_size:
                # Remove oldest entries
                sorted_keys = sorted(
                    _cache.keys(),
                    key=lambda k: _cache[k][1]
                )
                for old_key in sorted_keys[:len(_cache) - max_size]:
                    del _cache[old_key]
            
            return result
        
        # Allow manual cache clearing
        def clear_cache() -> None:
            keys_to_remove = [k for k in _cache if k.startswith(func.__name__)]
            for k in keys_to_remove:
                del _cache[k]
        
        wrapper.clear_cache = clear_cache  # type: ignore
        return wrapper
    
    return decorator


def clear_all_caches() -> None:
    """Clear all cached responses."""
    _cache.clear()


# =============================================================================
# Demo Data Helpers
# =============================================================================

def load_demo_data(filename: str) -> Optional[str]:
    """
    Load demo/mock data from the sample_data directory.
    
    Args:
        filename: Name of the file in sample_data/
        
    Returns:
        File contents or None if not found
    """
    # Find project root
    current = Path(__file__).parent
    while current != current.parent:
        sample_data = current / "sample_data"
        if sample_data.exists():
            data_file = sample_data / filename
            if data_file.exists():
                return data_file.read_text()
        current = current.parent
    
    return None


def get_fallback_response(service: str, query: str) -> dict[str, Any]:
    """
    Get a fallback response when API is unavailable.
    
    Useful for demos when credentials aren't set.
    
    Args:
        service: Service name
        query: The query that was attempted
        
    Returns:
        Mock response dict
    """
    return {
        "status": "demo_mode",
        "service": service,
        "query": query,
        "message": f"Running in demo mode. Set {API_KEY_MAP.get(service, 'API_KEY')} for live data.",
        "data": [],
    }
