#!/usr/bin/env python3
"""
Test script for the NPC Generator
"""

from features.npc_generator.agent import NPCSpec, generate_npc
from test_utils import run_generation_test

def main():
    """Runs the NPC generator test."""
    generator_name = "NPC"
    
    examples = [
        {
            "title": "Minimalist Prompt",
            "prompt": "A grumpy dwarf blacksmith named Borin"
        },
        {
            "title": "Detailed Prompt",
            "prompt": "Create Osperado, the half-elf banker with a missing leg. He's secretly a member of the city's thieves' guild."
        }
    ]
    
    run_generation_test(generator_name, generate_npc, NPCSpec, examples)

if __name__ == "__main__":
    main() 