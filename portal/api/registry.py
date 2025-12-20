import os
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent

class LessonRegistry:
    def __init__(self):
        self.lessons = {}
        self.modules = []
        self.scan_lessons()

    def scan_lessons(self):
        """Scan the project for modules and lessons."""
        module_patterns = sorted(list(PROJECT_ROOT.glob("0*")))
        
        for module_path in module_patterns:
            if not module_path.is_dir():
                continue
            
            module_name = module_path.name
            lessons_in_module = []
            
            lesson_patterns = sorted(list(module_path.glob("0*")))
            for lesson_path in lesson_patterns:
                if not lesson_path.is_dir():
                    continue
                
                lesson_id = lesson_path.name
                main_py = lesson_path / "main.py"
                readme_md = lesson_path / "README.md"
                
                if main_py.exists():
                    lesson_key = f"{module_name}/{lesson_id}"
                    lesson_data = {
                        "id": lesson_id,
                        "module": module_name,
                        "key": lesson_key,
                        "path": str(lesson_path.relative_to(PROJECT_ROOT)),
                        "title": self._extract_title(readme_md) or lesson_id,
                        "description": self._extract_description(readme_md),
                        "has_readme": readme_md.exists()
                    }
                    self.lessons[lesson_key] = lesson_data
                    lessons_in_module.append(lesson_data)
            
            if lessons_in_module:
                self.modules.append({
                    "id": module_name,
                    "title": module_name.split("_", 1)[1].replace("_", " ").title() if "_" in module_name else module_name,
                    "lessons": lessons_in_module
                })

    def _extract_title(self, readme_path: Path) -> Optional[str]:
        if not readme_path.exists():
            return None
        content = readme_path.read_text()
        match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
        return match.group(1) if match else None

    def _extract_description(self, readme_path: Path) -> str:
        if not readme_path.exists():
            return ""
        content = readme_path.read_text()
        # Get first paragraph after title
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("# "):
                # Find next non-empty line
                for next_line in lines[i+1:]:
                    if next_line.strip() and not next_line.startswith("#"):
                        return next_line.strip()
        return ""

    def get_agent_instance(self, module: str, lesson: str, provider: str = None, model: str = None):
        """Dynamically import and return the agent instance."""
        lesson_key = f"{module}/{lesson}"
        if lesson_key not in self.lessons:
            raise ValueError(f"Lesson {lesson_key} not found")
        
        main_py = PROJECT_ROOT / module / lesson / "main.py"
        
        # Performance: Import and call get_agent
        spec = importlib.util.spec_from_file_location(f"lesson_{lesson}", str(main_py))
        module_obj = importlib.util.module_from_spec(spec)
        
        # Add parent to path for relative imports in main.py
        sys.path.insert(0, str(PROJECT_ROOT))
        
        try:
            spec.loader.exec_module(module_obj)
            if hasattr(module_obj, "get_agent"):
                from shared.model_config import get_model
                llm_model = get_model(provider=provider, model=model) if provider else None
                return module_obj.get_agent(model=llm_model)
            else:
                raise AttributeError(f"Lesson {lesson_key} has no get_agent() function")
        finally:
            if str(PROJECT_ROOT) in sys.path:
                sys.path.remove(str(PROJECT_ROOT))

import re
registry = LessonRegistry()
