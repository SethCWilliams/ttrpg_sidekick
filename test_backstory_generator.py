#!/usr/bin/env python3
"""
Test script for the Backstory Generator
"""

from features.backstories.agent import BackstorySpec, generate_backstory
from test_utils import run_generation_test

def main():
    """Runs the backstory generator test."""
    generator_name = "Backstory"
    
    examples = [
        {
            "title": "Orphaned Wizard",
            "prompt": "A young wizard who was orphaned at a young age and grew up on the streets, discovering their magical powers by accident."
        },
        {
            "title": "Fallen Noble",
            "prompt": "A noble knight from a disgraced family who seeks to restore their family's honor by undertaking a perilous quest."
        }
    ]
    
    run_generation_test(generator_name, generate_backstory, BackstorySpec, examples)

if __name__ == "__main__":
    main() 