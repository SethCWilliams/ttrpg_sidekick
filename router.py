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

CLASSIFY AS 'unknown' only if the prompt is unclear or doesn't fit either category.

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
        if intent not in ['npc', 'building']:
            intent = 'unknown'

        return {
            "intent": intent,
            "prompt": user_prompt
        }
