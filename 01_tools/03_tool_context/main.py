#!/usr/bin/env python3
"""
Lesson 03: Tool Context

Concepts covered:
- Using RunContext to access agent state
- session_state for persistent storage
- Building stateful tools
- Tracking data across tool calls

Run: python main.py --shop
     python main.py --notes
     python main.py --counter
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.run.context import RunContext

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# =============================================================================
# Shopping Cart Tools (Stateful)
# =============================================================================

def add_to_cart(run_context: RunContext, item: str, quantity: int = 1) -> str:
    """
    Add an item to the shopping cart.
    
    Args:
        item: Name of the item to add
        quantity: Number of items to add (default: 1)
        
    Returns:
        Confirmation message with current cart contents
    """
    # Initialize cart if not exists
    if "cart" not in run_context.session_state:
        run_context.session_state["cart"] = []
    
    # Add item
    run_context.session_state["cart"].append({
        "item": item,
        "quantity": quantity,
        "added_at": datetime.now().isoformat(),
    })
    
    cart = run_context.session_state["cart"]
    total_items = sum(i["quantity"] for i in cart)
    
    return f"Added {quantity}x {item}. Cart now has {total_items} items."


def view_cart(run_context: RunContext) -> str:
    """
    View all items in the shopping cart.
    
    Returns:
        List of all items in the cart with quantities
    """
    cart = run_context.session_state.get("cart", [])
    
    if not cart:
        return "Cart is empty."
    
    lines = ["Shopping Cart:"]
    for i, item in enumerate(cart, 1):
        lines.append(f"  {i}. {item['quantity']}x {item['item']}")
    
    total = sum(i["quantity"] for i in cart)
    lines.append(f"\nTotal items: {total}")
    
    return "\n".join(lines)


def clear_cart(run_context: RunContext) -> str:
    """
    Clear all items from the shopping cart.
    
    Returns:
        Confirmation message
    """
    run_context.session_state["cart"] = []
    return "Cart has been cleared."


# =============================================================================
# Note-Taking Tools (Stateful)
# =============================================================================

def add_note(run_context: RunContext, content: str, category: str = "general") -> str:
    """
    Add a note to the notebook.
    
    Args:
        content: The note content
        category: Category for the note (default: general)
        
    Returns:
        Confirmation with note ID
    """
    if "notes" not in run_context.session_state:
        run_context.session_state["notes"] = []
        run_context.session_state["note_counter"] = 0
    
    run_context.session_state["note_counter"] += 1
    note_id = run_context.session_state["note_counter"]
    
    run_context.session_state["notes"].append({
        "id": note_id,
        "content": content,
        "category": category,
        "created_at": datetime.now().isoformat(),
    })
    
    return f"Note #{note_id} added to '{category}' category."


def list_notes(run_context: RunContext, category: str = None) -> str:
    """
    List all notes, optionally filtered by category.
    
    Args:
        category: Optional category to filter by
        
    Returns:
        List of notes
    """
    notes = run_context.session_state.get("notes", [])
    
    if category:
        notes = [n for n in notes if n["category"] == category]
    
    if not notes:
        return "No notes found."
    
    lines = ["Notes:"]
    for note in notes:
        lines.append(f"  [{note['id']}] ({note['category']}) {note['content'][:50]}")
    
    return "\n".join(lines)


def delete_note(run_context: RunContext, note_id: int) -> str:
    """
    Delete a note by its ID.
    
    Args:
        note_id: The ID of the note to delete
        
    Returns:
        Confirmation message
    """
    notes = run_context.session_state.get("notes", [])
    original_len = len(notes)
    
    run_context.session_state["notes"] = [n for n in notes if n["id"] != note_id]
    
    if len(run_context.session_state["notes"]) < original_len:
        return f"Note #{note_id} deleted."
    return f"Note #{note_id} not found."


# =============================================================================
# Counter/Quota Tools (Stateful)
# =============================================================================

def track_api_call(run_context: RunContext, api_name: str) -> str:
    """
    Track an API call (demonstrates quota management).
    
    Args:
        api_name: Name of the API being called
        
    Returns:
        Current count and remaining quota
    """
    if "api_calls" not in run_context.session_state:
        run_context.session_state["api_calls"] = {}
    
    calls = run_context.session_state["api_calls"]
    calls[api_name] = calls.get(api_name, 0) + 1
    
    max_calls = 5  # Example quota
    remaining = max(0, max_calls - calls[api_name])
    
    return f"API '{api_name}' called {calls[api_name]} times. Remaining quota: {remaining}"


def get_usage_stats(run_context: RunContext) -> str:
    """
    Get usage statistics for all tracked APIs.
    
    Returns:
        Summary of all API call counts
    """
    calls = run_context.session_state.get("api_calls", {})
    
    if not calls:
        return "No API calls tracked yet."
    
    lines = ["API Usage Stats:"]
    total = 0
    for api, count in sorted(calls.items()):
        lines.append(f"  {api}: {count} calls")
        total += count
    lines.append(f"\nTotal calls: {total}")
    
    return "\n".join(lines)


# =============================================================================
# Agent Creation
# =============================================================================

def create_shopping_agent(model):
    """Create a shopping assistant agent."""
    return Agent(
        model=model,
        tools=[add_to_cart, view_cart, clear_cart],
        session_state={"cart": []},  # Initialize state
        instructions=[
            "You are a shopping assistant.",
            "Help users add items to their cart and manage their shopping.",
            "Always confirm what was added and show the current cart status.",
        ],
        show_tool_calls=True,
        markdown=True,
    )


def create_notes_agent(model):
    """Create a note-taking assistant agent."""
    return Agent(
        model=model,
        tools=[add_note, list_notes, delete_note],
        session_state={"notes": [], "note_counter": 0},
        instructions=[
            "You are a note-taking assistant.",
            "Help users create, organize, and manage their notes.",
            "Use categories to keep notes organized.",
        ],
        show_tool_calls=True,
        markdown=True,
    )


def create_counter_agent(model):
    """Create an agent that demonstrates quota tracking."""
    return Agent(
        model=model,
        tools=[track_api_call, get_usage_stats],
        session_state={"api_calls": {}},
        instructions=[
            "You are an API usage tracker.",
            "Track API calls and report on usage statistics.",
            "Warn when approaching quota limits.",
        ],
        show_tool_calls=True,
        markdown=True,
    )



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_shopping_agent(model)


def main():
    """Demonstrate tool context and state management."""
    parser = argparse.ArgumentParser(
        description="Tool context and state demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument("--shop", action="store_true", help="Shopping cart demo")
    parser.add_argument("--notes", action="store_true", help="Note-taking demo")
    parser.add_argument("--counter", action="store_true", help="API counter demo")
    args = parser.parse_args()

    # Default to shopping demo
    if not any([args.shop, args.notes, args.counter]):
        args.shop = True

    print_header("Lesson 03: Tool Context")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.shop:
        print_section("Shopping Cart Demo")
        agent = create_shopping_agent(model)
        
        # Simulate a shopping session
        queries = [
            "Add 2 apples and 3 bananas to my cart",
            "Also add a loaf of bread",
            "What's in my cart?",
        ]
        
        for query in queries:
            print(f"\nUser: {query}")
            print("-" * 40)
            agent.print_response(query)
            print()

    if args.notes:
        print_section("Note-Taking Demo")
        agent = create_notes_agent(model)
        
        queries = [
            "Add a note: Remember to buy milk. Category: shopping",
            "Add a note: Meeting at 3pm tomorrow. Category: work",
            "List all my notes",
            "Delete note 1",
            "List notes again",
        ]
        
        for query in queries:
            print(f"\nUser: {query}")
            print("-" * 40)
            agent.print_response(query)
            print()

    if args.counter:
        print_section("API Counter Demo")
        agent = create_counter_agent(model)
        
        queries = [
            "Track a call to the weather API",
            "Track another call to weather API",
            "Track a call to the maps API",
            "Show me the usage stats",
        ]
        
        for query in queries:
            print(f"\nUser: {query}")
            print("-" * 40)
            agent.print_response(query)
            print()

    print_section("Key Takeaways")
    print("  1. RunContext gives tools access to agent state")
    print("  2. session_state persists across tool calls")
    print("  3. Initialize state with session_state={} in Agent")
    print("  4. The LLM doesn't see RunContext - it's injected automatically")


if __name__ == "__main__":
    main()
