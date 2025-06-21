#!/usr/bin/env python3
"""
Test script for the Quest Generator Agent.
"""

import os
import sys
from features.quest_generator.agent import QuestSpec, generate_quest

def test_quest_generation():
    """Test the quest generator with various prompts."""
    
    # Test cases
    test_cases = [
        {
            "name": "Rescue Mission",
            "prompt": "A princess has been kidnapped by a dragon and taken to a mountain lair",
            "world": "Forgotten Realms"
        },
        {
            "name": "Investigation Quest", 
            "prompt": "A series of mysterious disappearances in a small village",
            "world": "Eberron"
        },
        {
            "name": "Fetch Quest",
            "prompt": "Retrieve a rare magical artifact from an ancient temple",
            "world": "Greyhawk"
        },
        {
            "name": "Brief Quest",
            "prompt": "Clear goblins from a local mine",
            "world": "Forgotten Realms",
            "brief": True
        }
    ]
    
    print("🧪 Testing Quest Generator")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        # Create the spec
        spec = QuestSpec(
            world_name=test_case["world"],
            prompt=test_case["prompt"],
            brief=test_case.get("brief", False)
        )
        
        try:
            # Generate the quest
            result = generate_quest(spec)
            
            # Print the result
            print(f"World: {test_case['world']}")
            print(f"Prompt: {test_case['prompt']}")
            if test_case.get("brief"):
                print("Mode: Brief")
            print("\nGenerated Quest:")
            print(result)
            
        except Exception as e:
            print(f"❌ Error generating quest: {e}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_quest_generation() 