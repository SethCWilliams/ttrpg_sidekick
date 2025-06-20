import os
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

    def route_request(self, user_prompt: str) -> dict:
        """
        Classifies the user's prompt to determine the correct generator to use.

        Returns a dictionary containing the 'intent' and the original 'prompt'.
        """
        system_prompt = """
You are the master router for a TTRPG content generation tool. Your job is to analyze the user's prompt and determine what kind of content they want to create.
You must classify the user's request into one of the following categories: 'npc', 'building', or 'unknown'.
Respond with a single word only.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0, # We want a deterministic classification
            max_tokens=10,
        )
        
        intent = response.choices[0].message.content.lower().strip()

        # Basic validation to ensure it's one of the expected intents
        if intent not in ['npc', 'building']:
            intent = 'unknown'

        return {
            "intent": intent,
            "prompt": user_prompt
        }
