#!/usr/bin/env python3
"""
Test script for the Character Backstory Generator
"""

import os
import sys
from features.backstories.agent import BackstorySpec, generate_backstory

def test_backstory_generator():
    """Test the backstory generator with various prompts."""
    
    test_cases = [
        {
            "name": "Orphaned Wizard",
            "prompt": "A young wizard who was orphaned at a young age and discovered magical powers while living on the streets",
            "world": "Forgotten Realms"
        },
        {
            "name": "Former Soldier",
            "prompt": "A retired soldier who lost their family in war and now seeks redemption through adventuring",
            "world": "Eberron"
        },
        {
            "name": "Noble's Child",
            "prompt": "A noble's child who ran away from home to escape arranged marriage and discovered their true calling",
            "world": "Ravenloft"
        },
        {
            "name": "Brief Backstory",
            "prompt": "A simple farmer who found a magical sword and became an adventurer",
            "world": "Forgotten Realms",
            "brief": True
        }
    ]
    
    print("📖 Testing Character Backstory Generator")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        spec = BackstorySpec(
            world_name=test_case['world'],
            prompt=test_case['prompt'],
            brief=test_case.get('brief', False)
        )
        
        try:
            result = generate_backstory(spec)
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
    
    test_backstory_generator() 