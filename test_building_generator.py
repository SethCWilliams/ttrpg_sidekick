#!/usr/bin/env python3
"""
Test script for the Building Generator
"""

import os
import sys
import time
from features.building_generator.agent import BuildingSpec, generate_building

def check_environment():
    """Check if required environment variables are set."""
    api_provider = os.getenv("API_PROVIDER", "openai").lower()
    
    print(f"API Provider: {api_provider.upper()}")

    if api_provider == "openai":
        if not os.getenv("OPENAI_API_KEY") or "your-api-key" in os.getenv("OPENAI_API_KEY"):
            print("❌ OPENAI_API_KEY is not set correctly in your .envrc file.")
            return False
    elif api_provider == "ollama":
        print("To use Ollama, ensure the Ollama application is running.")
    else:
        print(f"❌ Unknown API_PROVIDER: {api_provider}")
        return False
    
    return True

def main():
    print("🎲 TTRPG Sidekick - Building Generator Test")
    print("=" * 50)
    
    if not check_environment():
        sys.exit(1)
    
    print("✅ Environment variables loaded")
    
    # --- Example 1: Simple Prompt ---
    print("🎯 Example 1: Simple Prompt")
    print("=" * 50)
    simple_spec = BuildingSpec(
        world_name="Forgotten Realms",
        prompt="A seaside tavern called 'The Salty Siren'"
    )
    run_generation(simple_spec)
    
    # --- Example 2: Detailed Prompt ---
    print("\\n\\n🎯 Example 2: Detailed Prompt")
    print("=" * 50)
    detailed_spec = BuildingSpec(
        world_name="Forgotten Realms",
        prompt="An old, abandoned lighthouse on a cliff, rumored to be haunted by the ghost of its former keeper who was trying to signal a lost love."
    )
    run_generation(detailed_spec)


def run_generation(spec: BuildingSpec):
    """Helper function to run the generation and print results."""
    print(f"User Prompt: \"{spec.prompt}\"")
    print("-" * 50)
    
    try:
        start_time = time.perf_counter()
        building_sheet = generate_building(spec)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        print("\\n✨ Generated Building Sheet:\\n")
        print(building_sheet)
        print("-" * 50)
        print(f"⏱️ Time to generate: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Error generating building: {e}")

if __name__ == "__main__":
    main() 