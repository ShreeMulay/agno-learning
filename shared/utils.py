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


# Auto-setup path when this module is imported
setup_path()
