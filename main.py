#!/usr/bin/env python3
"""
TTRPG Sidekick: Your AI-powered assistant for tabletop role-playing games.
"""

import argparse
import sys
import os
from router import Router
from features.npc_generator.agent import NPCSpec, generate_npc
from features.building_generator.agent import BuildingSpec, generate_building
from features.quest_generator.agent import QuestSpec, generate_quest
from features.magic_items.agent import MagicItemSpec, generate_magic_item
from features.battlefields.agent import BattlefieldSpec, generate_battlefield
from features.backstories.agent import BackstorySpec, generate_backstory

def check_environment():
    """Checks for the necessary environment variables."""
    api_provider = os.getenv("API_PROVIDER", "openai").lower()
    if api_provider == "openai" and (not os.getenv("OPENAI_API_KEY") or "your-api-key" in os.getenv("OPENAI_API_KEY")):
        print("❌ API_PROVIDER is set to 'openai', but OPENAI_API_KEY is not configured in .envrc.")
        return False
    elif api_provider == "ollama":
        print("✅ Using Ollama. Ensure the Ollama application is running.")
    return True

def main():
    """Main entry point for the TTRPG Sidekick application."""
    if not check_environment():
        sys.exit(1)

    parser = argparse.ArgumentParser(description="AI-powered assistant for TTRPGs.")
    parser.add_argument("prompt", type=str, help="Your creative prompt for what you want to generate.")
    parser.add_argument("--world", type=str, default="Forgotten Realms", help="The name of the campaign world for context.")
    parser.add_argument("--brief", action="store_true", help="Generate a brief, slimmed-down version of the output.")
    
    args = parser.parse_args()

    print("🧠 Thinking...")
    
    # 1. Route the request
    router = Router()
    routed_request = router.route_request(args.prompt)
    intent = routed_request.get("intent")

    print(f"🔎 Intent Detected: {intent.upper()}")
    if args.brief:
        print("📜 Brief mode enabled")

    # 2. Call the appropriate generator
    if intent == "npc":
        spec = NPCSpec(world_name=args.world, prompt=args.prompt, brief=args.brief)
        result = generate_npc(spec)
    elif intent == "building":
        spec = BuildingSpec(world_name=args.world, prompt=args.prompt, brief=args.brief)
        result = generate_building(spec)
    elif intent == "quest":
        spec = QuestSpec(world_name=args.world, prompt=args.prompt, brief=args.brief)
        result = generate_quest(spec)
    elif intent == "magic_item":
        spec = MagicItemSpec(world_name=args.world, prompt=args.prompt, brief=args.brief)
        result = generate_magic_item(spec)
    elif intent == "battlefield":
        spec = BattlefieldSpec(world_name=args.world, prompt=args.prompt, brief=args.brief)
        result = generate_battlefield(spec)
    elif intent == "backstory":
        spec = BackstorySpec(world_name=args.world, prompt=args.prompt, brief=args.brief)
        result = generate_backstory(spec)
    else:
        result = f"Sorry, I'm not sure how to handle that request. I can currently generate 'npc', 'building', 'quest', 'magic_item', 'battlefield', or 'backstory'."

    # 3. Print the result
    print("-" * 50)
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    main()
