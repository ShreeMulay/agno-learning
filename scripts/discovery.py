import os
import re
import json
import ast
from pathlib import Path

def parse_main_py(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract Docstring
    docstring = ""
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree) or ""
    except:
        pass
    
    # Extract relative path and info
    rel_path = os.path.relpath(file_path, os.getcwd())
    parts = rel_path.split(os.sep)
    
    # Category extraction from path
    category = "General"
    subcategory = None
    if len(parts) >= 4:
        category = parts[1].replace('_', ' ').capitalize()
        subcategory = parts[2].replace('_', ' ').capitalize()
    elif len(parts) == 3:
        category = "Root"
    
    # Find parameters in argparse with DEFAULTS
    params = []
    
    # Identify positional args (usually query or topic)
    # Match: add_argument("query", default="...", help="...")
    pos_matches = re.finditer(r'add_argument\s*\(\s*["\'](?P<name>[^-]\w+)["\'](?P<args>[^)]*)\)', content)
    for match in pos_matches:
        arg_name = match.group('name')
        args_text = match.group('args')
        
        default_val = ""
        default_match = re.search(r'default\s*=\s*["\'](?P<val>[^"\']+)["\']', args_text)
        if default_match:
            default_val = default_match.group('val')
            
        params.append({
            "name": arg_name,
            "type": "string",
            "required": True,
            "is_positional": True,
            "default": default_val
        })

    # Identify optional flags
    # Match: add_argument("--pdf", default="...", help="...")
    arg_matches = re.finditer(r'add_argument\s*\(\s*["\']-?-(?P<name>[\w-]+)["\'](?P<args>[^)]*)\)', content)
    for match in arg_matches:
        arg_name = match.group('name').replace('-', '_')
        args_text = match.group('args')
        if arg_name not in ['provider', 'model', 'temperature', 'help']:
            default_val = ""
            default_match = re.search(r'default\s*=\s*(?P<val>[^,)]+)', args_text)
            if default_match:
                default_val = default_match.group('val').strip(' "\'')
                if default_val == "None": default_val = ""
                
            params.append({
                "name": arg_name,
                "type": "string", 
                "required": False,
                "is_positional": False,
                "default": default_val
            })

    # Tool detection
    tools = []
    if "DuckDuckGoTools" in content: tools.append("web")
    if "LanceDb" in content or "knowledge" in content: tools.append("rag")
    if "Team(" in content: tools.append("team")
    if "Structured" in content.lower() or "output_schema" in content: tools.append("structured")

    # Final UI Enrichment
    for p in params:
        name = p["name"].lower()
        if "pdf" in name: p["ui_type"] = "file_pdf"
        elif "url" in name: p["ui_type"] = "url"
        elif "file" in name or "path" in name: p["ui_type"] = "file_any"
        elif "query" in name or "topic" in name or "content" in name: p["ui_type"] = "textarea"
        else: p["ui_type"] = "text"

    # Check if get_agent returns Agent or Team
    agent_type = "Agent"
    if "Team(" in content:
        agent_type = "Team"

    return {
        "id": rel_path.replace(os.sep, "__").replace(".py", ""),
        "name": docstring.split("\n")[0].split(":")[1].strip() if ":" in docstring.split("\n")[0] else parts[-2].replace('_', ' ').title(),
        "category": category,
        "subcategory": subcategory,
        "description": "\n".join(docstring.split("\n")[1:]).strip(),
        "path": rel_path,
        "dir": os.path.dirname(rel_path),
        "params": params,
        "type": agent_type,
        "tools": tools
    }

def main():
    root_dir = "07_real_world"
    catalog = []
    
    for root, dirs, files in os.walk(root_dir):
        if "main.py" in files:
            file_path = os.path.join(root, "main.py")
            if "_template" in file_path: continue
            try:
                info = parse_main_py(file_path)
                catalog.append(info)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
                
    # Save Catalog to Backend
    os.makedirs("gui/backend/data", exist_ok=True)
    with open("gui/backend/data/agent_catalog.json", "w") as f:
        json.dump(catalog, f, indent=2)
    
    print(f"Catalog generated with {len(catalog)} agents in gui/backend/data/")

if __name__ == "__main__":
    main()
