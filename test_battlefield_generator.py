#!/usr/bin/env python3
"""
Test script for the Battlefield Generator
"""

from features.battlefields.agent import BattlefieldSpec, generate_battlefield
from test_utils import run_generation_test

def main():
    """Runs the battlefield generator test."""
    generator_name = "Battlefield"
    
    examples = [
        {
            "title": "Mountain Pass",
            "prompt": "A narrow, treacherous mountain pass where two armies are about to clash. The weather is snowy and visibility is poor."
        },
        {
            "title": "Ancient Ruins",
            "prompt": "The crumbling ruins of an ancient city, filled with crumbling walls, overgrown courtyards, and a collapsed library that provides tactical advantages."
        }
    ]
    
    run_generation_test(generator_name, generate_battlefield, BattlefieldSpec, examples)

if __name__ == "__main__":
    main() 