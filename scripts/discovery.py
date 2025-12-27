#!/usr/bin/env python3
"""Agent Discovery Script - Enhanced metadata extraction.

Scans 07_real_world/ directory for agent examples and extracts:
- Basic info (name, description, path)
- Category/subcategory from path
- Parameters from argparse AND DEFAULT_CONFIG
- Tools used (web, rag, memory, structured, teams)
- Patterns declared in docstring
- Output schema (Pydantic models)
- Dependencies/imports

Run with:
    python scripts/discovery.py
"""

import os
import re
import json
import ast
import logging
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def extract_docstring_metadata(docstring: str) -> dict:
    """Extract structured metadata from new-style docstrings.
    
    Parses format:
        Example #XXX: Name
        Category: category/subcategory
        
        DESCRIPTION:
        ...
        
        PATTERNS:
        - Pattern 1
        - Pattern 2
        
        ARGUMENTS:
        - arg1 (type): Description. Default: value
    """
    result = {
        "example_number": None,
        "docstring_name": None,
        "docstring_category": None,
        "doc_description": "",
        "patterns": [],
        "doc_arguments": [],
    }
    
    if not docstring:
        return result
    
    lines = docstring.strip().split('\n')
    
    # Parse first line: "Example #XXX: Name"
    if lines:
        first_line = lines[0].strip()
        example_match = re.match(r'Example\s*#?(\d+):\s*(.+)', first_line, re.I)
        if example_match:
            result["example_number"] = int(example_match.group(1))
            result["docstring_name"] = example_match.group(2).strip()
    
    # Parse Category line
    for line in lines[1:5]:  # Check first few lines
        cat_match = re.match(r'Category:\s*(.+)', line.strip(), re.I)
        if cat_match:
            result["docstring_category"] = cat_match.group(1).strip()
            break
    
    # Parse sections using regex
    full_text = '\n'.join(lines)
    
    # DESCRIPTION section
    desc_match = re.search(r'DESCRIPTION:\s*\n(.*?)(?=\n\s*(?:PATTERNS|ARGUMENTS|$))', 
                           full_text, re.S | re.I)
    if desc_match:
        result["doc_description"] = desc_match.group(1).strip()
    
    # PATTERNS section
    patterns_match = re.search(r'PATTERNS:\s*\n(.*?)(?=\n\s*(?:ARGUMENTS|$))', 
                               full_text, re.S | re.I)
    if patterns_match:
        pattern_lines = patterns_match.group(1).strip().split('\n')
        for line in pattern_lines:
            line = line.strip()
            if line.startswith('-'):
                # Extract pattern name (before parentheses)
                pattern = line[1:].strip()
                # Get just the pattern name, not the parenthetical
                pattern_name = re.match(r'([^(]+)', pattern)
                if pattern_name:
                    result["patterns"].append(pattern_name.group(1).strip())
    
    # ARGUMENTS section
    args_match = re.search(r'ARGUMENTS:\s*\n(.*?)(?=\n\s*"""|\Z)', 
                           full_text, re.S | re.I)
    if args_match:
        arg_lines = args_match.group(1).strip().split('\n')
        for line in arg_lines:
            line = line.strip()
            if line.startswith('-'):
                # Parse: "- arg_name (type): Description. Default: value"
                arg_match = re.match(
                    r'-\s*(\w+)\s*\(([^)]+)\):\s*(.+?)(?:Default:\s*(.+))?$',
                    line
                )
                if arg_match:
                    arg_name = arg_match.group(1)
                    arg_type = arg_match.group(2).strip()
                    arg_desc = arg_match.group(3).strip().rstrip('.')
                    arg_default = arg_match.group(4).strip() if arg_match.group(4) else ""
                    
                    # Clean up default value (remove quotes)
                    if arg_default.startswith('"') and arg_default.endswith('"'):
                        arg_default = arg_default[1:-1]
                    elif arg_default.startswith("'") and arg_default.endswith("'"):
                        arg_default = arg_default[1:-1]
                    
                    result["doc_arguments"].append({
                        "name": arg_name,
                        "type": arg_type,
                        "description": arg_desc,
                        "default": arg_default,
                    })
    
    return result


def extract_default_config(content: str) -> dict:
    """Extract DEFAULT_CONFIG dictionary from source code."""
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'DEFAULT_CONFIG':
                        # Evaluate the dict literal
                        if isinstance(node.value, ast.Dict):
                            config = {}
                            for key, val in zip(node.value.keys, node.value.values):
                                if isinstance(key, ast.Constant):
                                    key_str = key.value
                                    # Handle different value types
                                    if isinstance(val, ast.Constant):
                                        config[key_str] = val.value
                                    elif isinstance(val, ast.List):
                                        config[key_str] = []
                                    elif isinstance(val, ast.Dict):
                                        config[key_str] = {}
                                    else:
                                        config[key_str] = str(ast.unparse(val))
                            return config
    except Exception as e:
        logger.debug(f"Could not parse DEFAULT_CONFIG: {e}")
    return {}


def extract_output_schemas(content: str) -> list[dict]:
    """Extract Pydantic model schemas from source code."""
    schemas = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it inherits from BaseModel
                base_names = [
                    b.id if isinstance(b, ast.Name) else 
                    b.attr if isinstance(b, ast.Attribute) else None
                    for b in node.bases
                ]
                if 'BaseModel' in base_names:
                    schema = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "fields": []
                    }
                    
                    # Extract fields (class attributes with annotations)
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            field_name = item.target.id
                            field_type = ast.unparse(item.annotation) if item.annotation else "Any"
                            
                            # Try to extract Field description
                            field_desc = ""
                            if item.value and isinstance(item.value, ast.Call):
                                if hasattr(item.value, 'keywords'):
                                    for kw in item.value.keywords:
                                        if kw.arg == 'description' and isinstance(kw.value, ast.Constant):
                                            field_desc = kw.value.value
                            
                            schema["fields"].append({
                                "name": field_name,
                                "type": field_type,
                                "description": field_desc,
                            })
                    
                    schemas.append(schema)
    except Exception as e:
        logger.debug(f"Could not parse output schemas: {e}")
    return schemas


def extract_imports(content: str) -> dict:
    """Extract imports to determine dependencies and features."""
    imports = {
        "agno_features": [],
        "tools": [],
        "external": [],
    }
    
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports["external"].append(alias.name.split('.')[0])
                    
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                
                if module.startswith('agno'):
                    # Agno imports
                    if 'tools' in module:
                        for alias in node.names:
                            imports["tools"].append(alias.name)
                    else:
                        for alias in node.names:
                            imports["agno_features"].append(alias.name)
                elif module.startswith('pydantic'):
                    imports["agno_features"].append("pydantic")
                else:
                    imports["external"].append(module.split('.')[0])
    except Exception as e:
        logger.debug(f"Could not parse imports: {e}")
    
    # Deduplicate
    imports["agno_features"] = list(set(imports["agno_features"]))
    imports["tools"] = list(set(imports["tools"]))
    imports["external"] = list(set(imports["external"]))
    
    return imports


def detect_tools_from_content(content: str) -> list[str]:
    """Detect tool categories from source code analysis."""
    tools = []
    
    # Web search tools
    if any(x in content for x in ["DuckDuckGoTools", "TavilyTools", "SerpApiTools", "EXATools"]):
        tools.append("web")
    
    # RAG/Knowledge tools
    if any(x in content for x in ["LanceDb", "Pinecone", "Qdrant", "Knowledge(", "knowledge="]):
        tools.append("rag")
    
    # Memory/persistence
    if any(x in content for x in ["SqliteDb", "PostgresDb", "enable_user_memories", "add_history_to_context"]):
        tools.append("memory")
    
    # Structured output
    if any(x in content for x in ["response_model=", "output_schema=", "BaseModel"]):
        tools.append("structured")
    
    # Teams/multi-agent
    if any(x in content for x in ["Team(", "from agno.team"]):
        tools.append("team")
    
    # Reasoning
    if any(x in content for x in ["reasoning=True", "Reasoner("]):
        tools.append("reasoning")
    
    # File handling
    if any(x in content for x in ["FileTools", "PDFTools", "CsvTools"]):
        tools.append("files")
    
    # Code execution
    if any(x in content for x in ["PythonTools", "ShellTools", "CodeInterpreter"]):
        tools.append("code")
    
    # API/HTTP
    if any(x in content for x in ["ApiTools", "requests.", "httpx."]):
        tools.append("api")
    
    return list(set(tools))


def parse_argparse_params(content: str) -> list[dict]:
    """Extract parameters from argparse add_argument calls."""
    params = []
    
    # Positional arguments: add_argument("query", ...)
    pos_pattern = r'add_argument\s*\(\s*["\'](?P<name>[^-"\'][^"\']*)["\'](?P<args>[^)]*)\)'
    for match in re.finditer(pos_pattern, content):
        arg_name = match.group('name')
        args_text = match.group('args')
        
        if arg_name in ['help', 'h']:
            continue
            
        default_val = ""
        default_match = re.search(r'default\s*=\s*["\']([^"\']*)["\']', args_text)
        if default_match:
            default_val = default_match.group(1)
        
        help_text = ""
        help_match = re.search(r'help\s*=\s*["\']([^"\']*)["\']', args_text)
        if help_match:
            help_text = help_match.group(1)
        
        params.append({
            "name": arg_name,
            "type": "string",
            "required": True,
            "is_positional": True,
            "default": default_val,
            "description": help_text,
        })
    
    # Optional flags: add_argument("--flag", ...)
    opt_pattern = r'add_argument\s*\(\s*["\']--(?P<name>[\w-]+)["\'](?P<args>[^)]*)\)'
    for match in re.finditer(opt_pattern, content):
        arg_name = match.group('name').replace('-', '_')
        args_text = match.group('args')
        
        # Skip standard model args
        if arg_name in ['provider', 'model', 'temperature', 'help', 'version']:
            continue
        
        # Detect type
        arg_type = "string"
        if 'action="store_true"' in args_text or "action='store_true'" in args_text:
            arg_type = "boolean"
        elif 'type=int' in args_text:
            arg_type = "integer"
        elif 'type=float' in args_text:
            arg_type = "float"
        
        # Extract default
        default_val = ""
        default_match = re.search(r'default\s*=\s*(?P<val>[^,)]+)', args_text)
        if default_match:
            val = default_match.group('val').strip(' "\'')
            # Skip DEFAULT_CONFIG references - we'll get these from the dict itself
            if 'DEFAULT_CONFIG' in val:
                default_val = ""
            elif val not in ['None', 'False', 'True']:
                default_val = val
            elif val == 'True':
                default_val = "true"
            elif val == 'False':
                default_val = "false"
        
        # Extract help text
        help_text = ""
        help_match = re.search(r'help\s*=\s*["\']([^"\']*)["\']', args_text)
        if help_match:
            help_text = help_match.group(1)
        
        params.append({
            "name": arg_name,
            "type": arg_type,
            "required": False,
            "is_positional": False,
            "default": default_val,
            "description": help_text,
        })
    
    return params


def infer_ui_type(param: dict) -> str:
    """Infer the best UI input type for a parameter."""
    name = param.get("name", "").lower()
    desc = param.get("description", "").lower()
    param_type = param.get("type", "string")
    
    if param_type == "boolean":
        return "checkbox"
    if param_type == "integer" or param_type == "float":
        return "number"
    
    # File types
    if "pdf" in name or "pdf" in desc:
        return "file_pdf"
    if "csv" in name or "csv" in desc:
        return "file_csv"
    if "file" in name or "path" in name:
        return "file_any"
    
    # URL
    if "url" in name or "link" in name:
        return "url"
    
    # Email
    if "email" in name:
        return "email"
    
    # Long text
    if any(x in name for x in ["query", "topic", "content", "message", "description", "text", "prompt"]):
        return "textarea"
    
    # Select/enum (if description mentions options)
    if ":" in desc and "/" in desc:
        return "select"
    
    return "text"


def parse_main_py(file_path: str) -> dict:
    """Parse a main.py file and extract all metadata."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Basic path info
    rel_path = os.path.relpath(file_path, os.getcwd())
    parts = Path(rel_path).parent.parts
    path_parts = list(parts)
    
    # Extract docstring
    docstring = ""
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree) or ""
    except Exception as e:
        logger.warning(f"Could not parse AST for {file_path}: {e}")
    
    # Parse docstring metadata (new format)
    doc_meta = extract_docstring_metadata(docstring)
    
    # Extract DEFAULT_CONFIG
    default_config = extract_default_config(content)
    
    # Extract output schemas
    output_schemas = extract_output_schemas(content)
    
    # Extract imports
    imports = extract_imports(content)
    
    # Detect tools from content analysis
    detected_tools = detect_tools_from_content(content)
    
    # Parse argparse parameters (old format)
    argparse_params = parse_argparse_params(content)
    
    # Merge parameters: prefer docstring args, fallback to argparse, enrich with DEFAULT_CONFIG
    params = []
    seen_params = set()
    
    # First, add docstring arguments
    for arg in doc_meta.get("doc_arguments", []):
        param = {
            "name": arg["name"],
            "type": arg["type"],
            "required": False,  # Docstring args usually have defaults
            "is_positional": False,
            "default": arg.get("default", default_config.get(arg["name"], "")),
            "description": arg.get("description", ""),
        }
        param["ui_type"] = infer_ui_type(param)
        params.append(param)
        seen_params.add(arg["name"])
    
    # Add argparse params not in docstring
    # Skip argparse params that are CLI aliases for DEFAULT_CONFIG keys
    # (when docstring has documented the proper names)
    has_docstring_args = bool(doc_meta.get("doc_arguments"))
    for arg in argparse_params:
        if arg["name"] not in seen_params:
            # If docstring documented args, skip argparse params without defaults
            # (they're likely CLI aliases like --company for company_name)
            if has_docstring_args and not arg.get("default"):
                # Check if this is a CLI alias for a DEFAULT_CONFIG key
                if any(arg["name"] in key or key in arg["name"] for key in default_config):
                    continue
            arg["default"] = arg.get("default") or str(default_config.get(arg["name"], ""))
            arg["ui_type"] = infer_ui_type(arg)
            params.append(arg)
            seen_params.add(arg["name"])
    
    # Add DEFAULT_CONFIG params not yet seen
    for key, val in default_config.items():
        if key not in seen_params:
            param = {
                "name": key,
                "type": "integer" if isinstance(val, int) else "string",
                "required": False,
                "is_positional": False,
                "default": str(val) if val is not None else "",
                "description": "",
            }
            param["ui_type"] = infer_ui_type(param)
            params.append(param)
    
    # Category extraction
    category = "General"
    subcategory = None
    
    # Prefer docstring category
    if doc_meta.get("docstring_category"):
        cat_parts = doc_meta["docstring_category"].split('/')
        category = cat_parts[0].strip().replace('_', ' ').title()
        if len(cat_parts) > 1:
            subcategory = cat_parts[1].strip().replace('_', ' ').title()
    elif len(path_parts) >= 3:
        category = path_parts[1].replace('_', ' ').title()
        subcategory = path_parts[2].replace('_', ' ').title()
    elif len(path_parts) == 2:
        category = "Root"
    
    # Determine name
    name = doc_meta.get("docstring_name") or ""
    if not name:
        # Fallback: parse old-style docstring "Example XX: Name - Description"
        first_line = docstring.split('\n')[0] if docstring else ""
        if ":" in first_line:
            name = first_line.split(":", 1)[1].strip()
        else:
            name = Path(file_path).parent.name.replace('_', ' ').title()
    
    # Determine description
    description = doc_meta.get("doc_description") or ""
    if not description and docstring:
        # Fallback: everything after first line
        lines = docstring.split('\n')
        description = '\n'.join(lines[1:]).strip()
        # Remove "Run with:" section
        if "Run with:" in description:
            description = description.split("Run with:")[0].strip()
    
    # Agent type detection
    agent_type = "Agent"
    if "Team(" in content:
        agent_type = "Team"
    
    # Combine patterns from docstring and detected tools
    patterns = doc_meta.get("patterns", [])
    
    # Normalize pattern names to tool categories
    pattern_to_tool = {
        "tools": "web",
        "duckduckgo": "web",
        "web": "web",
        "knowledge": "rag",
        "rag": "rag",
        "memory": "memory",
        "structured": "structured",
        "structured output": "structured",
        "team": "team",
        "teams": "team",
        "reasoning": "reasoning",
    }
    
    # Merge pattern-declared tools with detected tools
    all_tools = set(detected_tools)
    for pattern in patterns:
        pattern_lower = pattern.lower()
        for key, tool in pattern_to_tool.items():
            if key in pattern_lower:
                all_tools.add(tool)
    
    return {
        "id": rel_path.replace(os.sep, "__").replace(".py", ""),
        "name": name,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "path": rel_path,
        "dir": os.path.dirname(rel_path),
        "path_parts": path_parts,
        "params": params,
        "type": agent_type,
        "tools": sorted(list(all_tools)),
        "patterns": patterns,
        "output_schemas": output_schemas,
        "imports": imports,
        "example_number": doc_meta.get("example_number"),
    }


def main():
    """Run discovery and generate catalog."""
    root_dir = "07_real_world"
    catalog = []
    errors = []
    
    for root, dirs, files in os.walk(root_dir):
        if "main.py" in files:
            file_path = os.path.join(root, "main.py")
            if "_template" in file_path:
                continue
            try:
                info = parse_main_py(file_path)
                catalog.append(info)
                logger.info(f"Parsed: {info['name']} ({len(info['params'])} params, {len(info['tools'])} tools)")
            except Exception as e:
                logger.error(f"Error parsing {file_path}: {e}")
                errors.append({"path": file_path, "error": str(e)})
    
    # Sort by example number if available, then by path
    catalog.sort(key=lambda x: (x.get("example_number") or 999, x["path"]))
    
    # Save catalog
    os.makedirs("gui/backend/data", exist_ok=True)
    with open("gui/backend/data/agent_catalog.json", "w") as f:
        json.dump(catalog, f, indent=2)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Discovery Complete")
    print(f"{'='*60}")
    print(f"Agents found: {len(catalog)}")
    print(f"Errors: {len(errors)}")
    
    # Stats
    tool_counts = {}
    for agent in catalog:
        for tool in agent.get("tools", []):
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
    
    print(f"\nTool Distribution:")
    for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
        print(f"  {tool}: {count}")
    
    category_counts = {}
    for agent in catalog:
        cat = agent.get("category", "Unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print(f"\nCategory Distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    
    print(f"\nCatalog saved to: gui/backend/data/agent_catalog.json")
    
    if errors:
        print(f"\nErrors:")
        for err in errors:
            print(f"  {err['path']}: {err['error']}")


if __name__ == "__main__":
    main()
