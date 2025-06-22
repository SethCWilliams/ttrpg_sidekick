#!/usr/bin/env python3
"""
Shared utilities for test scripts.
"""

import os
import sys
import time

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

def run_generation_test(generator_name: str, generation_func, spec, examples: list):
    """
    Runs a standardized test for a given generator.

    Args:
        generator_name (str): The name of the generator being tested.
        generation_func: The function that runs the generation (e.g., generate_npc).
        spec: The Pydantic model for the generator's spec (e.g., NPCSpec).
        examples (list): A list of dictionaries, each with 'title' and 'prompt'.
    """
    print(f"🎲 TTRPG Sidekick - {generator_name} Test")
    print("=" * 50)

    if not check_environment():
        sys.exit(1)
    
    print("✅ Environment variables loaded")

    for i, example in enumerate(examples):
        print(f"\n\n🎯 Example {i+1}: {example['title']}")
        print("=" * 50)
        
        spec_instance = spec(
            world_name="Forgotten Realms",
            prompt=example['prompt']
        )
        
        print(f"User Prompt: \"{spec_instance.prompt}\"")
        print("-" * 50)
        
        try:
            start_time = time.perf_counter()
            result = generation_func(spec_instance)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            print(f"\n✨ Generated {generator_name}:\n")
            print(result)
            print("-" * 50)
            print(f"⏱️ Time to generate: {elapsed_time:.2f} seconds")

        except Exception as e:
            print(f"❌ Error generating {generator_name}: {e}") 