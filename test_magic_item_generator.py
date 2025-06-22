#!/usr/bin/env python3
"""
Test script for the Magic Item Generator
"""

from features.magic_items.agent import MagicItemSpec, generate_magic_item
from test_utils import run_generation_test

def main():
    """Runs the magic item generator test."""
    generator_name = "Magic Item"
    
    examples = [
        {
            "title": "Legendary Sword",
            "prompt": "A legendary sword that was forged by an ancient dragon and can control fire"
        },
        {
            "title": "Cursed Ring",
            "prompt": "A cursed ring that grants invisibility but slowly drives the wearer mad"
        },
        {
            "title": "Staff of Healing",
            "prompt": "A wooden staff carved with healing runes that can cure diseases"
        }
    ]
    
    run_generation_test(generator_name, generate_magic_item, MagicItemSpec, examples)

if __name__ == "__main__":
    main() 