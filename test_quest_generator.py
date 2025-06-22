#!/usr/bin/env python3
"""
Test script for the Quest Generator
"""

from features.quest_generator.agent import QuestSpec, generate_quest
from test_utils import run_generation_test

def main():
    """Runs the quest generator test."""
    generator_name = "Quest"
    
    examples = [
        {
            "title": "Simple Quest",
            "prompt": "The players must find the missing crown of the ancient king, which was stolen from the royal vault."
        },
        {
            "title": "Complex Quest",
            "prompt": "A plague is sweeping through the city, and the players must find a rare flower from the top of a dangerous mountain to create a cure. The mountain is guarded by a territorial griffin, and a rival faction of alchemists is also trying to get the flower first."
        }
    ]
    
    run_generation_test(generator_name, generate_quest, QuestSpec, examples)

if __name__ == "__main__":
    main() 