#!/usr/bin/env python3
"""Example #103: EDA Visualization Agent
Category: outskill_cohort3/data_analysis

DESCRIPTION:
Performs exploratory data analysis (EDA) on datasets and creates visualizations.
The agent can write and execute Python code to analyze data, generate statistics,
and create charts using matplotlib, seaborn, or plotly.

PATTERNS:
- Tools (PythonTools for code execution)
- Code Generation (writes analysis scripts)
- Data Visualization (generates charts)

ARGUMENTS:
- dataset_url (str): URL to a CSV dataset. Default: IMDB movie dataset
- analysis_type (str): Type of analysis (overview, distribution, correlation). Default: "overview"
- output_dir (str): Directory to save generated plots. Default: "./output"
"""

import argparse
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "dataset_url": "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
    "analysis_type": "overview",
    "output_dir": "./output",
}

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.tools.python import PythonTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_agent(model, output_dir: str):
    """Create the EDA visualization agent."""
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    return Agent(
        name="EDAVisualizationAgent",
        model=model,
        tools=[PythonTools(
            base_dir=base_dir,
            run_code=True,
            pip_install=True,
        )],
        instructions=[
            "You are an expert data analyst specializing in exploratory data analysis.",
            "When analyzing data:",
            "1. First load the data and show basic info (shape, columns, dtypes)",
            "2. Check for missing values and data quality issues",
            "3. Generate descriptive statistics for numeric columns",
            "4. Create appropriate visualizations based on the analysis type",
            "5. Save all plots to the output directory",
            "Use pandas, matplotlib, and seaborn for analysis.",
            "Always provide clear interpretations of your findings.",
        ],
        markdown=True,
    )


def get_agent(model=None):
    """Get agent instance for GUI integration."""
    if model is None:
        model = get_model()
    return create_agent(model, DEFAULT_CONFIG["output_dir"])


def build_analysis_prompt(dataset_url: str, analysis_type: str, output_dir: str) -> str:
    """Build the analysis prompt based on type."""
    base_prompt = f"""
Analyze the dataset at: {dataset_url}

Save all visualizations to: {output_dir}
"""
    
    prompts = {
        "overview": base_prompt + """
Perform a data overview analysis:
1. Load data and show shape, columns, data types
2. Display first few rows
3. Show missing value counts
4. Generate descriptive statistics
5. Create a correlation heatmap for numeric columns
6. Save the heatmap as 'correlation_heatmap.png'
""",
        "distribution": base_prompt + """
Analyze data distributions:
1. Load the data
2. For each numeric column, create a histogram
3. Create box plots for detecting outliers
4. Save plots as 'distributions.png'
5. Identify and report any outliers
""",
        "correlation": base_prompt + """
Perform correlation analysis:
1. Load the data
2. Calculate correlation matrix for numeric columns
3. Create an annotated heatmap
4. Identify top 5 strongest correlations (positive and negative)
5. Create scatter plots for the top correlations
6. Save as 'correlation_analysis.png'
""",
    }
    
    return prompts.get(analysis_type, prompts["overview"])


def main():
    parser = argparse.ArgumentParser(
        description="Perform EDA and create visualizations with AI"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--dataset-url",
        type=str,
        default=DEFAULT_CONFIG["dataset_url"],
        help="URL to CSV dataset"
    )
    parser.add_argument(
        "--analysis-type",
        type=str,
        choices=["overview", "distribution", "correlation"],
        default=DEFAULT_CONFIG["analysis_type"],
        help="Type of analysis to perform"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_CONFIG["output_dir"],
        help="Directory to save generated visualizations"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming output"
    )
    
    args = parser.parse_args()
    
    print_header("EDA Visualization Agent")
    
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print_section("Configuration")
    print(f"  Dataset: {args.dataset_url.split('/')[-1]}")
    print(f"  Analysis: {args.analysis_type}")
    print(f"  Output: {output_path.absolute()}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model, str(output_path))
    
    prompt = build_analysis_prompt(
        args.dataset_url, 
        args.analysis_type, 
        str(output_path.absolute())
    )
    
    print_section("Running Analysis")
    
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
        
        generated_files = list(output_path.glob("*.png"))
        if generated_files:
            print_section("Generated Files")
            for f in generated_files:
                print(f"  📊 {f.name}")
                
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
