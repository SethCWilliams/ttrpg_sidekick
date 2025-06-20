#!/usr/bin/env python3
"""
Test script for the NPC Generator
"""

import os
import sys
import time
from features.npc_generator.agent import NPCSpec, generate_npc
from core.memory import MemoryService


def check_environment():
    """Check if required environment variables are set."""
    api_provider = os.getenv("API_PROVIDER", "openai").lower()
    
    print(f"API Provider: {api_provider.upper()}")

    if api_provider == "openai":
        if not os.getenv("OPENAI_API_KEY") or "your-api-key" in os.getenv("OPENAI_API_KEY"):
            print("❌ OPENAI_API_KEY is not set correctly in your .envrc file.")
            print("\n💡 To fix this:")
            print("1. Edit your .envrc file.")
            print("2. Add your key: export OPENAI_API_KEY='sk-...'")
            print("3. Run 'direnv allow' to reload the environment.")
            return False
    elif api_provider == "ollama":
        print("To use Ollama, ensure the Ollama application is running and you have pulled a model.")
        print("Example: 'ollama run llama3'")
        # No specific key check needed for Ollama
    else:
        print(f"❌ Unknown API_PROVIDER: {api_provider}")
        return False
    
    return True


def main():
    print("🎲 TTRPG Sidekick - NPC Generator Test")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("✅ Environment variables loaded")
    
    # Initialize memory service
    memory_service = MemoryService()
    print(f"📁 Using data directory: {memory_service.data_dir}")
    
    # --- Example 1: Minimal Prompt ---
    print("\n\n🎯 Example 1: Minimalist Prompt")
    print("=" * 50)
    minimal_spec = NPCSpec(
        world_name="Forgotten Realms",
        prompt="A grumpy dwarf blacksmith named Borin"
    )
    run_generation(minimal_spec)
    
    # --- Example 2: Detailed Prompt ---
    print("\n\n🎯 Example 2: Detailed Prompt")
    print("=" * 50)
    detailed_spec = NPCSpec(
        world_name="Forgotten Realms",
        prompt="Create Osperado, the half-elf banker with a missing leg. He's secretly a member of the city's thieves' guild."
    )
    run_generation(detailed_spec)


def run_generation(spec: NPCSpec):
    """Helper function to run the generation and print results."""
    print(f"User Prompt: \"{spec.prompt}\"")
    print("-" * 50)
    
    try:
        # Start the timer
        start_time = time.perf_counter()

        # Generate the NPC sheet
        npc_sheet = generate_npc(spec)
        
        # Stop the timer
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # Display the results
        print("\n✨ Generated NPC Sheet:\n")
        print(npc_sheet)
        print("-" * 50)
        print(f"⏱️ Time to generate: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Error generating NPC: {e}")


if __name__ == "__main__":
    main() 