"""
Smoke Test Runner for Agno Learning Hub Examples.

Every example must pass these three tests:
1. Import Test - Module can be imported without errors
2. Agent Creation - get_agent() returns a valid Agent
3. Smoke Test - Basic query works (with demo/mock data)

Usage:
    # Test single example
    python -m shared.testing.smoke_test examples/07_real_world/business/sales/01_lead_qualifier
    
    # Test all examples in a category
    python -m shared.testing.smoke_test --category business
    
    # Test ALL examples
    python -m shared.testing.smoke_test --all
    
    # Dry run (import test only, no API calls)
    python -m shared.testing.smoke_test --all --dry-run
"""

import argparse
import importlib.util
import os
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TestResult:
    """Result of testing a single example."""
    
    example_path: str
    import_ok: bool = False
    agent_creation_ok: bool = False
    smoke_test_ok: bool = False
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    
    @property
    def passed(self) -> bool:
        """True if all tests passed."""
        return self.import_ok and self.agent_creation_ok and self.smoke_test_ok
    
    @property
    def status(self) -> str:
        """Human-readable status."""
        if self.passed:
            return "PASS"
        elif self.error_message:
            return "FAIL"
        else:
            return "SKIP"


def find_examples(base_path: Path, category: Optional[str] = None) -> list[Path]:
    """
    Find all example directories with main.py files.
    
    Args:
        base_path: Root path to search (e.g., examples/07_real_world)
        category: Optional category filter (e.g., "business", "healthcare")
        
    Returns:
        List of paths to example directories
    """
    examples = []
    
    if category:
        # Search only within the specified category
        search_paths = [base_path / category]
    else:
        # Search everything
        search_paths = [base_path]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
            
        for main_py in search_path.rglob("main.py"):
            # Skip __pycache__ and _template
            if "__pycache__" in str(main_py) or "_template" in str(main_py):
                continue
            examples.append(main_py.parent)
    
    return sorted(examples)


def run_smoke_test(
    example_path: Path,
    dry_run: bool = False,
    timeout: int = 30,
) -> TestResult:
    """
    Run smoke tests on a single example.
    
    Args:
        example_path: Path to example directory (containing main.py)
        dry_run: If True, only test import (no API calls)
        timeout: Max seconds for smoke test
        
    Returns:
        TestResult with pass/fail status
    """
    result = TestResult(example_path=str(example_path))
    start_time = time.time()
    
    main_py = example_path / "main.py"
    if not main_py.exists():
        result.error_message = "main.py not found"
        return result
    
    # Test 1: Import
    try:
        # Add example path to sys.path for relative imports
        sys.path.insert(0, str(example_path))
        
        spec = importlib.util.spec_from_file_location("main", main_py)
        if spec is None or spec.loader is None:
            result.error_message = "Failed to load module spec"
            return result
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        result.import_ok = True
    except Exception as e:
        result.error_message = f"Import failed: {e}"
        result.duration_seconds = time.time() - start_time
        return result
    finally:
        if str(example_path) in sys.path:
            sys.path.remove(str(example_path))
    
    # Test 2: Agent Creation
    try:
        if not hasattr(module, "get_agent"):
            result.error_message = "Missing get_agent() function"
            return result
        
        agent = module.get_agent()
        if agent is None:
            result.error_message = "get_agent() returned None"
            return result
            
        result.agent_creation_ok = True
    except Exception as e:
        result.error_message = f"Agent creation failed: {e}"
        result.duration_seconds = time.time() - start_time
        return result
    
    # Test 3: Smoke Test (skip if dry run)
    if dry_run:
        result.smoke_test_ok = True  # Assume pass for dry run
    else:
        try:
            # Use a simple test query
            response = agent.run("Hello, this is a smoke test. Respond briefly.")
            
            if response is None:
                result.error_message = "agent.run() returned None"
                return result
                
            # Check we got some content
            content = getattr(response, "content", str(response))
            if not content or len(content) < 5:
                result.error_message = f"Empty or too short response: {content}"
                return result
            
            result.smoke_test_ok = True
        except Exception as e:
            result.error_message = f"Smoke test failed: {e}"
    
    result.duration_seconds = time.time() - start_time
    return result


def run_all_smoke_tests(
    base_path: Path,
    category: Optional[str] = None,
    dry_run: bool = False,
    verbose: bool = True,
) -> list[TestResult]:
    """
    Run smoke tests on all examples.
    
    Args:
        base_path: Root path to examples
        category: Optional category filter
        dry_run: If True, only test imports
        verbose: Print progress
        
    Returns:
        List of TestResult objects
    """
    examples = find_examples(base_path, category)
    results = []
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"  Smoke Testing {len(examples)} Examples")
        if category:
            print(f"  Category: {category}")
        if dry_run:
            print(f"  Mode: DRY RUN (import only)")
        print(f"{'='*60}\n")
    
    for i, example_path in enumerate(examples, 1):
        if verbose:
            rel_path = example_path.relative_to(base_path)
            print(f"  [{i}/{len(examples)}] {rel_path}...", end=" ", flush=True)
        
        result = run_smoke_test(example_path, dry_run=dry_run)
        results.append(result)
        
        if verbose:
            if result.passed:
                print(f"PASS ({result.duration_seconds:.1f}s)")
            else:
                print(f"FAIL: {result.error_message}")
    
    # Summary
    if verbose:
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        print(f"\n{'='*60}")
        print(f"  Results: {passed} passed, {failed} failed")
        print(f"{'='*60}\n")
        
        if failed > 0:
            print("  Failed examples:")
            for r in results:
                if not r.passed:
                    print(f"    - {r.example_path}: {r.error_message}")
            print()
    
    return results


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Smoke test runner for Agno Learning Hub examples"
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        type=str,
        help="Path to single example directory to test",
    )
    parser.add_argument(
        "--category", "-c",
        type=str,
        help="Test all examples in a category (e.g., business, healthcare)",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Test all examples",
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Import test only, no API calls",
    )
    parser.add_argument(
        "--base-path", "-b",
        type=str,
        default="examples/07_real_world",
        help="Base path to examples directory",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output",
    )
    
    args = parser.parse_args()
    
    # Determine base path
    project_root = Path(__file__).parent.parent.parent
    base_path = project_root / args.base_path
    
    if args.path:
        # Test single example
        example_path = Path(args.path)
        if not example_path.is_absolute():
            example_path = project_root / args.path
        
        result = run_smoke_test(example_path, dry_run=args.dry_run)
        
        if not args.quiet:
            print(f"\nResult: {result.status}")
            if result.error_message:
                print(f"Error: {result.error_message}")
            print(f"Duration: {result.duration_seconds:.1f}s\n")
        
        sys.exit(0 if result.passed else 1)
    
    elif args.all or args.category:
        # Test multiple examples
        results = run_all_smoke_tests(
            base_path,
            category=args.category,
            dry_run=args.dry_run,
            verbose=not args.quiet,
        )
        
        failed = sum(1 for r in results if not r.passed)
        sys.exit(1 if failed > 0 else 0)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
