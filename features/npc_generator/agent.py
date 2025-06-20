"""
NPC Generator Agent

Generates detailed NPCs with names, races, classes, motives, secrets, and dialogue.
"""

import os
from pydantic import BaseModel, Field
from openai import OpenAI

NPC_TEMPLATE_FULL = """
🧾 NPC Template: (Full)

📌 1. Quick Overview (at-a-glance info for DMs)
  • Name:
  • Race / Species:
  • Age / Apparent Age:
  • Gender / Pronouns:
  • Occupation / Role:
  • Location / Where usually found:
  • Brief Personality Tagline:
  • Voice inspiration:

⸻

👀 2. Appearance & Vibe
  • Physical traits:
  • Clothing / Gear:
  • Smells like:
  • Posture / Mannerisms:

⸻

🧠 3. Personality & Social Profile
  • Core traits:
  • Values:
  • Quirks:
  • Motivations:
  • Fears:

⸻

🎲 4. Connections & Roleplay Hooks
  • Allies / Friends:
  • Rivals / Enemies:
  • How they view the party:
  • Rumor about them:
  • What they want from the party:
  • What the party can get from them:

⸻

🧩 5. Secrets & Depth
  • Secret they're hiding:
  • Regret / Past trauma:
  • Hidden strength or twist:
  • If cornered…

⸻

🗡️ 6. Combat & Mechanical (Optional)
  •	Combat style:
  • Special abilities or gear:
"""

NPC_TEMPLATE_BRIEF = """
🧾 NPC Template (Brief)

📌 1. Quick Overview
  •Name:
  •Race / Species:
  •Occupation / Role:
  •Brief Personality Tagline:
  •One interesting thing you know about them:
  •Voice inspiration:

⸻

👀 2. Appearance & Vibe
  •Physical traits:
  •Clothing / Gear:

⸻

🧠 3. Personality & Social Profile
  •Core traits:
  •Motivations:
  •Fears:
  •Quirks:
"""

def _clean_npc_sheet(raw_text: str) -> str:
    """
    Cleans up common artifacts and conversational filler from the model's raw output.
    """
    lines = raw_text.strip().split('\\n')
    
    # List of known filler phrases to remove from the output
    filler_phrases = [
        "Here is the NPC template filled out",
        "NPC Template Fully Spun",
        "An Elixir for Storycrafting",
        "Combat & Mechanical (Optional Crafting) Complete!",
        "Oh, behold the enigmatic"
    ]
    
    # Filter out lines containing any of the filler phrases
    cleaned_lines = [
        line for line in lines if not any(phrase in line for phrase in filler_phrases)
    ]
    
    # Re-join the lines and remove any leading/trailing whitespace
    return '\\n'.join(cleaned_lines).strip()


class NPCSpec(BaseModel):
    """Input specification for NPC generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the NPC.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class NPCGeneratorAgent:
    """Agent for generating detailed NPCs by filling out a template."""
    
    def __init__(self):
        api_provider = os.getenv("API_PROVIDER", "openai").lower()

        if api_provider == "ollama":
            print("🤖 Using Ollama provider")
            self.client = OpenAI(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama",  # required but unused
            )
            self.model = os.getenv("OLLAMA_MODEL", "llama3")
        else:
            print("☁️ Using OpenAI provider")
            self.client = OpenAI()
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    def generate_npc_sheet(self, input_spec: NPCSpec) -> str:
        """
        Generates a detailed NPC character sheet based on a freeform prompt.
        
        Args:
            input_spec: Specification for the NPC to generate.
            
        Returns:
            A formatted string containing the completed NPC template.
        """
        system_prompt = "You are a silent and efficient TTRPG assistant. Your only job is to fill out the provided character sheet template using the user's prompt. You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."
        
        # Choose the template based on the 'brief' flag
        template = NPC_TEMPLATE_BRIEF if input_spec.brief else NPC_TEMPLATE_FULL
        
        user_prompt = f"""
Please create an NPC based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the character come alive.

{template}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.75, # Lowered slightly for more predictable formatting
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = _clean_npc_sheet(raw_sheet)
        return cleaned_sheet


# Convenience function for direct usage
def generate_npc(input_spec: NPCSpec) -> str:
    """
    Generates an NPC character sheet using the NPC generator agent.
    """
    agent = NPCGeneratorAgent()
    return agent.generate_npc_sheet(input_spec) 