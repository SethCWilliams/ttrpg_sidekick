#!/usr/bin/env python3
"""
Test script for the Building Generator
"""

from features.building_generator.agent import BuildingSpec, generate_building
from test_utils import run_generation_test

def main():
    """Runs the building generator test."""
    generator_name = "Building"
    
    examples = [
        {
            "title": "Tavern",
            "prompt": "A cozy, welcoming tavern called The Salty Siren, located in a bustling port city."
        },
        {
            "title": "Wizard's Tower",
            "prompt": "A mysterious, isolated wizard's tower rumored to be filled with magical artifacts and dangerous traps."
        },
        {
            "title": "Underground Lair",
            "prompt": "A dark and treacherous underground lair belonging to a notorious goblin king, filled with crude traps and stolen treasures."
        }
    ]
    
    run_generation_test(generator_name, generate_building, BuildingSpec, examples)

if __name__ == "__main__":
    main() 