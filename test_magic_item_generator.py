#!/usr/bin/env python3
"""
Test script for the Magic Item Generator
"""

import os
import sys
from features.magic_items.agent import MagicItemSpec, generate_magic_item

def test_magic_item_generator():
    """Test the magic item generator with various prompts."""
    
    test_cases = [
        {
            "name": "Legendary Sword",
            "prompt": "A legendary sword that was forged by an ancient dragon and can control fire",
            "world": "Forgotten Realms"
        },
        {
            "name": "Cursed Ring",
            "prompt": "A cursed ring that grants invisibility but slowly drives the wearer mad",
            "world": "Ravenloft"
        },
        {
            "name": "Staff of Healing",
            "prompt": "A wooden staff carved with healing runes that can cure diseases",
            "world": "Eberron"
        },
        {
            "name": "Brief Magic Item",
            "prompt": "A simple magic dagger that glows in the dark",
            "world": "Forgotten Realms",
            "brief": True
        }
    ]
    
    print("🧪 Testing Magic Item Generator")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        spec = MagicItemSpec(
            world_name=test_case['world'],
            prompt=test_case['prompt'],
            brief=test_case.get('brief', False)
        )
        
        try:
            result = generate_magic_item(spec)
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    # Check if we have the necessary environment setup
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("API_PROVIDER") == "ollama":
        print("❌ Please set up your API credentials in .envrc first.")
        print("   Run: cp .envrc.example .envrc")
        print("   Then edit .envrc with your API key or set API_PROVIDER=ollama")
        sys.exit(1)
    
    test_magic_item_generator() 