import os
import json
import re
from core.llm_service import llm_service

class Router:
    """
    The "brain" of the TTRPG Sidekick. It determines the user's intent
    and routes the request to the appropriate generator.
    """

    def __init__(self):
        # The client is now managed by the shared service
        self.client = llm_service.client
        self.model = llm_service.model

    def _parse_response(self, response_text: str) -> dict:
        """
        Parses the model's response to extract the JSON object.
        """
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return {} # Return empty dict if parsing fails

    def route_request(self, user_prompt: str) -> dict:
        """
        Classifies the user's prompt to determine the correct generator to use.

        Returns a dictionary containing the 'intent' and the original 'prompt'.
        """
        # Check for explicit qualifiers first
        qualifier_pattern = r'^/(\w+)\s+(.+)$'
        match = re.match(qualifier_pattern, user_prompt.strip())
        
        if match:
            qualifier = match.group(1).lower()
            actual_prompt = match.group(2).strip()
            
            # Map qualifiers to intents
            qualifier_map = {
                'npc': 'npc',
                'backstory': 'backstory', 
                'quest': 'quest',
                'building': 'building',
                'magic_item': 'magic_item',
                'battlefield': 'battlefield'
            }
            
            if qualifier in qualifier_map:
                return {
                    "intent": qualifier_map[qualifier],
                    "prompt": actual_prompt
                }
            else:
                # Unknown qualifier, fall back to AI classification
                print(f"⚠️  Unknown qualifier '/{qualifier}'. Using AI classification instead.")
        
        # If no qualifier or unknown qualifier, use AI classification
        system_prompt = """
You are the master router for a TTRPG content generation tool. Your job is to analyze the user's prompt and determine which generator they need.

CLASSIFY AS 'building' if the prompt:
- Contains building names (e.g., "The Dirty Clam", "Red Dragon Inn", "Wizard's Tower")
- Mentions locations, establishments, or venues (e.g., "tavern", "shop", "library", "guild hall", "temple")
- Describes a place or structure (e.g., "abandoned warehouse", "magical bookstore", "thief hideout")
- Uses words like: inn, tavern, shop, store, tower, castle, mansion, house, building, establishment, venue, location

CLASSIFY AS 'npc' if the prompt:
- Contains character names or descriptions (e.g., "Gandalf", "wise old wizard", "merchant")
- Mentions people, characters, or individuals (e.g., "villain", "hero", "merchant", "guard")
- Describes personality traits or roles (e.g., "charismatic leader", "shy apprentice", "brave warrior")
- Uses words like: person, character, individual, npc, merchant, wizard, warrior, rogue, etc.

CLASSIFY AS 'quest' if the prompt:
- Contains quest titles or mission names (e.g., "The Lost Artifact", "Rescue the Princess", "Clear the Dungeon")
- Mentions missions, tasks, or objectives (e.g., "find the missing", "rescue", "investigate", "retrieve", "finding", "searching", "looking for")
- Describes adventures or challenges (e.g., "dangerous journey", "mysterious disappearance", "ancient curse")
- Uses words like: quest, mission, adventure, task, objective, journey, rescue, find, investigate, retrieve, clear, defeat, search, locate, discover, hunt, track, pursue, etc.
- Contains phrases about searching, finding, or locating something (e.g., "finding the needle", "searching for treasure", "looking for clues")

CLASSIFY AS 'magic_item' if the prompt:
- Contains item names or descriptions (e.g., "Sword of Fire", "Ring of Invisibility", "Staff of Power")
- Mentions magical objects, weapons, armor, or artifacts (e.g., "magic sword", "enchanted ring", "cursed amulet", "legendary weapon")
- Describes magical properties or effects (e.g., "sword that shoots lightning", "ring that makes you invisible", "staff that controls weather")
- Uses words like: magic item, artifact, weapon, armor, ring, amulet, staff, wand, sword, dagger, bow, shield, etc.
- Contains phrases about magical abilities or enchantments (e.g., "item that grants flight", "weapon that deals extra damage", "armor that protects from fire")

CLASSIFY AS 'battlefield' if the prompt:
- Contains battlefield names or locations (e.g., "Battle of Helm's Deep", "The Bloody Plains", "Frostwind Pass")
- Mentions combat environments or war zones (e.g., "battlefield", "war zone", "combat arena", "fighting ground")
- Describes tactical situations or military engagements (e.g., "ambush site", "defensive position", "siege location", "skirmish area")
- Uses words like: battlefield, arena, battleground, war zone, combat zone, siege, ambush, skirmish, battle, fight, war, tactical, strategic, etc.
- Contains phrases about combat environments (e.g., "place where armies clash", "location for a battle", "tactical position", "defensive terrain")

CLASSIFY AS 'backstory' if the prompt:
- Contains character backstory elements (e.g., "orphaned at a young age", "trained by a master", "survived a tragedy")
- Mentions personal history or life events (e.g., "grew up in poverty", "lost their family", "discovered their powers")
- Describes character origins or background (e.g., "former soldier", "street urchin", "noble's child")
- Uses words like: backstory, background, history, past, origin, childhood, family, tragedy, loss, training, mentor, etc.
- Contains phrases about character development (e.g., "how they became who they are", "what shaped their personality", "their life before adventuring")

CLASSIFY AS 'unknown' only if the prompt is unclear or doesn't fit any category.

Your response MUST be a single, valid JSON object: {"intent": "your_classification"}
Do not add any other text, explanation, or markdown.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0, # We want a deterministic classification
            max_tokens=50, # Increased slightly for JSON structure
        )
        
        response_text = response.choices[0].message.content
        parsed_json = self._parse_response(response_text)
        intent = parsed_json.get("intent", "unknown").lower().strip()

        # Basic validation to ensure it's one of the expected intents
        if intent not in ['npc', 'building', 'quest', 'magic_item', 'battlefield', 'backstory']:
            intent = 'unknown'

        return {
            "intent": intent,
            "prompt": user_prompt
        }
