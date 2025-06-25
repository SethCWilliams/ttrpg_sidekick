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
        Checks for explicit qualifiers to determine the correct generator to use.

        Returns a dictionary containing the 'intent' and the original 'prompt'.
        """
        # Check for explicit qualifiers only
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
                # Unknown qualifier
                return {
                    "intent": "unknown_qualifier",
                    "prompt": user_prompt,
                    "unknown_qualifier": qualifier
                }
        
        # No qualifier found - this should be handled by conversational chat
        return {
            "intent": "conversational",
            "prompt": user_prompt
        }
