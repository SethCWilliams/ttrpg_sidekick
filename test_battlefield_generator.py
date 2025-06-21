#!/usr/bin/env python3
"""
Test script for the Battlefield Generator
"""

import os
import sys
from features.battlefields.agent import BattlefieldSpec, generate_battlefield

def test_battlefield_generator():
    """Test the battlefield generator with various prompts."""
    
    test_cases = [
        {
            "name": "Mountain Pass Battlefield",
            "prompt": "A narrow mountain pass where two armies must clash, with steep cliffs on both sides",
            "world": "Forgotten Realms"
        },
        {
            "name": "Urban Siege",
            "prompt": "A city under siege with crumbling walls, burning buildings, and desperate defenders",
            "world": "Eberron"
        },
        {
            "name": "Forest Ambush",
            "prompt": "A dense forest clearing where bandits ambush travelers, with fallen logs and thick underbrush",
            "world": "Ravenloft"
        },
        {
            "name": "Brief Battlefield",
            "prompt": "A simple arena for gladiatorial combat",
            "world": "Forgotten Realms",
            "brief": True
        }
    ]
    
    print("⚔️ Testing Battlefield Generator")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        spec = BattlefieldSpec(
            world_name=test_case['world'],
            prompt=test_case['prompt'],
            brief=test_case.get('brief', False)
        )
        
        try:
            result = generate_battlefield(spec)
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
    
    test_battlefield_generator() 