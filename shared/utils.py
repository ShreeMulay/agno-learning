"""
Common utility functions for Agno Learning Hub.

Provides helper functions used across multiple examples.
"""

import sys
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_sample_data_path(filename: str) -> Path:
    """
    Get the path to a sample data file.
    
    Args:
        filename: Name of the file in sample_data/
        
    Returns:
        Path to the sample data file
    """
    return get_project_root() / "sample_data" / filename


def print_header(title: str, width: int = 60) -> None:
    """
    Print a formatted header for example output.
    
    Args:
        title: Header text
        width: Total width of the header
    """
    print("\n" + "=" * width)
    print(f" {title}")
    print("=" * width + "\n")


def print_section(title: str, width: int = 60) -> None:
    """
    Print a formatted section separator.
    
    Args:
        title: Section title
        width: Total width of the separator
    """
    print("\n" + "-" * width)
    print(f" {title}")
    print("-" * width + "\n")


def print_response(response: Any, label: str = "Response") -> None:
    """
    Print an agent response in a formatted way.
    
    Args:
        response: The response object from agent.run()
        label: Label to show before the response
    """
    print(f"\n{label}:")
    print("-" * 40)
    
    if hasattr(response, "content"):
        print(response.content)
    else:
        print(response)
    
    print("-" * 40 + "\n")


def confirm_action(prompt: str = "Continue?") -> bool:
    """
    Ask user for confirmation.
    
    Args:
        prompt: The prompt to display
        
    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ("y", "yes")


def setup_path() -> None:
    """
    Add the project root to Python path for imports.
    
    Call this at the start of example scripts to enable
    imports from the shared module.
    """
    project_root = get_project_root()
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def check_openrouter_runcontext_error(provider: str) -> None:
    """
    Check if using OpenRouter with RunContext tools and warn user.
    
    OpenRouter has a known issue with tools that use RunContext,
    returning 500 errors. This function warns the user and suggests
    alternative providers.
    
    Args:
        provider: The current provider name
    """
    if provider == "openrouter":
        print("\n" + "=" * 60)
        print("  WARNING: OpenRouter + RunContext Tool Issue")
        print("=" * 60)
        print("""
  This example uses RunContext for stateful tools.
  OpenRouter has a known issue that causes 500 errors
  with these tools.
  
  WORKAROUND: Use a direct provider instead:
  
    python main.py --provider openai
    python main.py --provider anthropic  
    python main.py --provider google
    
  Press Enter to try anyway, or Ctrl+C to exit...
""")
        try:
            input()
        except KeyboardInterrupt:
            print("\n  Exiting. Try with --provider openai")
            import sys
            sys.exit(0)


def handle_openrouter_error(error: Exception, provider: str) -> bool:
    """
    Handle OpenRouter 500 errors gracefully.
    
    Args:
        error: The exception that was raised
        provider: The current provider name
        
    Returns:
        True if this was an OpenRouter error that was handled
    """
    error_str = str(error)
    if provider == "openrouter" and ("500" in error_str or "Internal Server Error" in error_str):
        print("\n" + "!" * 60)
        print("  OpenRouter Error Detected")
        print("!" * 60)
        print("""
  OpenRouter returned a 500 error. This is a known issue
  with RunContext-based tools.
  
  Please re-run with a direct provider:
  
    python main.py --provider openai
    python main.py --provider anthropic
    python main.py --provider google
""")
        return True
    return False


# Auto-setup path when this module is imported
setup_path()
