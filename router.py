import os
from openai import OpenAI

class Router:
    """
    The "brain" of the TTRPG Sidekick. It determines the user's intent
    and routes the request to the appropriate generator.
    """

    def __init__(self):
        api_provider = os.getenv("API_PROVIDER", "openai").lower()

        if api_provider == "ollama":
            self.client = OpenAI(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama",
            )
            self.model = os.getenv("OLLAMA_MODEL", "llama3")
        else:
            self.client = OpenAI()
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

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
