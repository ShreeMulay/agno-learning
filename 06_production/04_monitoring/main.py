#!/usr/bin/env python3
"""Lesson 04: Monitoring and Logging - Production observability.

This example demonstrates configuring custom logging and
monitoring for production agent deployments.

Run with:
    python main.py
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.utils.log import configure_agno_logging, log_info

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def setup_logging(log_file: str = "tmp/agent.log") -> logging.Logger:
    """Set up custom logging configuration."""
    
    # Ensure log directory exists
    Path(log_file).parent.mkdir(exist_ok=True)
    
    # Create custom logger
    logger = logging.getLogger("agno")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    # Console handler with color formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    
    # File handler with detailed formatting
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Configure Agno to use this logger
    configure_agno_logging(custom_default_logger=logger)
    
    return logger


def setup_component_loggers(log_dir: str = "tmp"):
    """Set up separate loggers for agents, teams, workflows."""
    
    Path(log_dir).mkdir(exist_ok=True)
    
    configs = [
        ("agno", f"{log_dir}/agent.log"),
        ("agno-team", f"{log_dir}/team.log"),
        ("agno-workflow", f"{log_dir}/workflow.log"),
    ]
    
    loggers = {}
    for name, log_file in configs:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(handler)
        loggers[name] = logger
    
    return loggers


def main():
    parser = argparse.ArgumentParser(description="Monitoring Demo")
    add_model_args(parser)
    parser.add_argument(
        "--log-file", type=str, default="tmp/agent.log",
        help="Log file path"
    )
    parser.add_argument(
        "--no-telemetry", action="store_true",
        help="Disable telemetry"
    )
    args = parser.parse_args()

    print_header("Lesson 04: Monitoring and Logging")
    
    # Set up logging
    logger = setup_logging(args.log_file)
    
    print_section("Logging Configuration")
    print(f"  Log file: {args.log_file}")
    print(f"  Console: INFO level")
    print(f"  File: DEBUG level")
    
    # Log startup
    logger.info("=" * 50)
    logger.info("Agent session started")
    logger.info(f"Provider: {args.provider}")
    logger.info(f"Telemetry: {'disabled' if args.no_telemetry else 'enabled'}")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    # Create agent with telemetry control
    agent = Agent(
        name="MonitoredAgent",
        model=model,
        instructions=["You are a helpful assistant."],
        telemetry=not args.no_telemetry,  # Control telemetry
        markdown=True,
    )
    
    print_section("Agent Created")
    print(f"  Name: {agent.name}")
    print(f"  Telemetry: {'disabled' if args.no_telemetry else 'enabled'}")
    
    # Use Agno's logging utilities
    log_info("Agent ready for interaction")
    
    # Demo conversation with logging
    print_section("Demo Conversation")
    
    prompts = [
        "What is 2 + 2?",
        "What is the capital of France?",
    ]
    
    for prompt in prompts:
        logger.info(f"User query: {prompt}")
        start = datetime.now()
        
        response = agent.run(prompt)
        
        duration = (datetime.now() - start).total_seconds()
        logger.info(f"Response time: {duration:.2f}s")
        logger.debug(f"Full response: {response.content}")
        
        print(f"\nQ: {prompt}")
        print(f"A: {response.content[:100]}...")
        print(f"   (Logged in {duration:.2f}s)")
    
    logger.info("Session completed")
    
    print_section("Check Logs")
    print(f"  cat {args.log_file}")


if __name__ == "__main__":
    main()
