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
You are the master router for a TTRPG content generation tool. Your only job is to analyze the user's prompt and determine which tool they need.
You must classify the user's request into one of the following categories: 'npc', 'building', or 'unknown'.
Your response MUST be a single, valid JSON object in the following format: {"intent": "your_classification"}
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
