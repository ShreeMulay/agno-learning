import os
import importlib.util
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent

class LessonRegistry:
    def __init__(self):
        self.lessons = {}
        self.modules = []
        self.scan_lessons()

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
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("# "):
                for next_line in lines[i+1:]:
                    if next_line.strip() and not next_line.startswith("#"):
                        return next_line.strip()
        return ""

    def _extract_default_message(self, content: str) -> str:
        """Extract the default message from argparse in main.py."""
        # Try different argument names
        patterns = [
            r'--message".*?default="([^"]+)"',
            r"--message'.*?default='([^']+)'",
            r'--query".*?default="([^"]+)"',
            r"--query'.*?default='([^']+)'",
            r'--search".*?default="([^"]+)"',
            r"--search'.*?default='([^']+)'",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1)
        return "Hello!"

    def scan_lessons(self):
        """Scan the project for modules and lessons."""
        module_paths = sorted([p for p in PROJECT_ROOT.glob("0*") if p.is_dir()])
        
        for module_path in module_paths:
            module_name = module_path.name
            lessons_in_module = []
            
            lesson_paths = sorted([p for p in module_path.glob("0*") if p.is_dir()])
            for lesson_path in lesson_paths:
                lesson_id = lesson_path.name
                main_py = lesson_path / "main.py"
                readme_md = lesson_path / "README.md"
                
                if main_py.exists():
                    lesson_key = f"{module_name}/{lesson_id}"
                    main_content = main_py.read_text()
                    lesson_data = {
                        "id": lesson_id,
                        "module": module_name,
                        "key": lesson_key,
                        "path": str(lesson_path.relative_to(PROJECT_ROOT)),
                        "title": self._extract_title(readme_md) or lesson_id,
                        "description": self._extract_description(readme_md),
                        "has_readme": readme_md.exists(),
                        "default_message": self._extract_default_message(main_content)
                    }
                    self.lessons[lesson_key] = lesson_data
                    lessons_in_module.append(lesson_data)
            
            if lessons_in_module:
                self.modules.append({
                    "id": module_name,
                    "title": module_name.split("_", 1)[1].replace("_", " ").title() if "_" in module_name else module_name,
                    "lessons": lessons_in_module
                })

    def get_agent_instance(self, module: str, lesson: str, provider: str = None, model: str = None, temperature: float = None):
        """Dynamically import and return the agent instance."""
        lesson_key = f"{module}/{lesson}"
        if lesson_key not in self.lessons:
            raise ValueError(f"Lesson {lesson_key} not found")
        
        main_py = PROJECT_ROOT / module / lesson / "main.py"
        
        spec = importlib.util.spec_from_file_location(f"lesson_{lesson}", str(main_py))
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module for {lesson_key}")
            
        module_obj = importlib.util.module_from_spec(spec)
        
        sys.path.insert(0, str(PROJECT_ROOT))
        try:
            spec.loader.exec_module(module_obj)
            if hasattr(module_obj, "get_agent"):
                from shared.model_config import get_model
                llm_kwargs = {}
                if provider: llm_kwargs["provider"] = provider
                if model: llm_kwargs["model"] = model
                if temperature is not None: llm_kwargs["temperature"] = float(temperature)
                
                llm_model = get_model(**llm_kwargs) if llm_kwargs else None
                return module_obj.get_agent(model=llm_model)
            else:
                raise AttributeError(f"Lesson {lesson_key} has no get_agent() function")
        finally:
            if str(PROJECT_ROOT) in sys.path:
                sys.path.remove(str(PROJECT_ROOT))

registry = LessonRegistry()
