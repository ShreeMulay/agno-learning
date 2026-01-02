#!/usr/bin/env python3
"""Example #104: Code to Diagram Generator
Category: outskill_cohort3/code_analysis

DESCRIPTION:
Analyzes Python source code and generates UML diagrams (PlantUML or Mermaid format).
The agent reads code files, understands the structure (classes, functions, relationships),
and creates visual diagrams representing the code architecture.

PATTERNS:
- Tools (FileTools for file operations)
- Code Analysis (parsing and understanding code)
- Diagram Generation (PlantUML, Mermaid)

ARGUMENTS:
- file_path (str): Path to Python file to analyze. Default: "example.py"
- diagram_type (str): Type of diagram (class, sequence, flowchart). Default: "class"
- output_format (str): Output format (plantuml, mermaid). Default: "mermaid"
"""

import argparse
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "file_path": "",
    "diagram_type": "class",
    "output_format": "mermaid",
}

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.tools.file import FileTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_agent(model, base_dir: str):
    """Create the code to diagram agent."""
    return Agent(
        name="CodeToDiagramAgent",
        model=model,
        tools=[FileTools(base_dir=Path(base_dir))],
        instructions=[
            "You are an expert software architect and UML diagram specialist.",
            "When analyzing code:",
            "1. Read and understand the code structure",
            "2. Identify classes, functions, and their relationships",
            "3. Generate clean, readable diagrams",
            "4. Use proper UML notation",
            "For PlantUML: Start with @startuml and end with @enduml",
            "For Mermaid: Use appropriate diagram type declaration",
            "Always save the generated diagram to a file.",
        ],
        show_tool_calls=True,
        markdown=True,
    )


def get_agent(model=None):
    """Get agent instance for GUI integration."""
    if model is None:
        model = get_model()
    return create_agent(model, ".")


def build_diagram_prompt(file_path: str, diagram_type: str, output_format: str) -> str:
    """Build the diagram generation prompt."""
    format_instructions = {
        "plantuml": "Use PlantUML syntax. Start with @startuml and end with @enduml.",
        "mermaid": "Use Mermaid syntax. Start with the appropriate diagram declaration (classDiagram, sequenceDiagram, flowchart TD).",
    }
    
    diagram_instructions = {
        "class": """
Create a class diagram showing:
- All classes and their attributes/methods
- Inheritance relationships (--|>)
- Composition relationships (--*)
- Association relationships (--)
- Method visibility (+public, -private, #protected)
""",
        "sequence": """
Create a sequence diagram showing:
- Key function calls and their order
- Method invocations between objects
- Return values where relevant
- Focus on the main execution flow
""",
        "flowchart": """
Create a flowchart showing:
- Main program flow
- Decision points (if/else)
- Loops
- Function calls
- Start and end points
""",
    }
    
    output_file = f"diagram.{'puml' if output_format == 'plantuml' else 'md'}"
    
    return f"""
Read the file: {file_path}

Analyze the code and create a {diagram_type} diagram.

{format_instructions.get(output_format, format_instructions['mermaid'])}

{diagram_instructions.get(diagram_type, diagram_instructions['class'])}

Save the diagram to: {output_file}

After saving, display the diagram content.
"""


def create_example_file(base_dir: Path) -> Path:
    """Create an example Python file to analyze."""
    example_code = '''
class Animal:
    """Base class for animals."""
    def __init__(self, name: str):
        self.name = name
    
    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    """A dog that can bark."""
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed
    
    def speak(self) -> str:
        return "Woof!"
    
    def fetch(self, item: str) -> str:
        return f"{self.name} fetched the {item}"

class Cat(Animal):
    """A cat that can meow."""
    def __init__(self, name: str, color: str):
        super().__init__(name)
        self.color = color
    
    def speak(self) -> str:
        return "Meow!"
    
    def scratch(self) -> str:
        return f"{self.name} scratches furniture"

class Pet:
    """A pet with an owner."""
    def __init__(self, animal: Animal, owner: str):
        self.animal = animal
        self.owner = owner
    
    def introduce(self) -> str:
        return f"{self.owner}\\'s pet {self.animal.name} says {self.animal.speak()}"
'''
    
    example_file = base_dir / "example.py"
    example_file.write_text(example_code)
    return example_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate UML diagrams from Python source code"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--file-path",
        type=str,
        default=DEFAULT_CONFIG["file_path"],
        help="Path to Python file to analyze (uses example if not provided)"
    )
    parser.add_argument(
        "--diagram-type",
        type=str,
        choices=["class", "sequence", "flowchart"],
        default=DEFAULT_CONFIG["diagram_type"],
        help="Type of diagram to generate"
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=["plantuml", "mermaid"],
        default=DEFAULT_CONFIG["output_format"],
        help="Output format for the diagram"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming output"
    )
    
    args = parser.parse_args()
    
    print_header("Code to Diagram Generator")
    
    base_dir = Path(__file__).parent
    
    if args.file_path:
        file_path = Path(args.file_path)
        if not file_path.exists():
            print(f"  Error: File not found: {file_path}")
            sys.exit(1)
    else:
        print_section("Creating Example")
        file_path = create_example_file(base_dir)
        print(f"  Created: {file_path.name}")
    
    print_section("Configuration")
    print(f"  File: {file_path}")
    print(f"  Diagram: {args.diagram_type}")
    print(f"  Format: {args.output_format}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model, str(base_dir))
    
    prompt = build_diagram_prompt(
        str(file_path),
        args.diagram_type,
        args.output_format
    )
    
    print_section("Generating Diagram")
    
    try:
        if args.stream:
            response = agent.run(prompt, stream=True)
            for chunk in response:
                if hasattr(chunk, 'content') and chunk.content:
                    print(chunk.content, end="", flush=True)
            print()
        else:
            response = agent.run(prompt)
            print(response.content)
        
        output_ext = "puml" if args.output_format == "plantuml" else "md"
        output_file = base_dir / f"diagram.{output_ext}"
        if output_file.exists():
            print_section("Output File")
            print(f"  📄 {output_file}")
            
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
