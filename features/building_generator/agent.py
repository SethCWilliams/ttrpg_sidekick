from typing import Optional
import os
from pydantic import BaseModel, Field
from openai import OpenAI
from core.llm_service import llm_service

# A detailed template for generating buildings
BUILDING_TEMPLATE = """
🏰 Building Profile: A Comprehensive Location Guide

📌 1. At a Glance (Quick DM Info)
  •	Building Name:
  •	Primary Function: (e.g., Tavern, Library, Blacksmith, Wizard's Tower)
  •	Location: (Neighborhood, City, Region)
  •	Key Figure / Proprietor: (Name and brief title)
  •	General Vibe: (e.g., "Cozy and welcoming," "Ominous and decaying," "Bustling and chaotic")

⸻

👀 2. Sensory Details (Bringing the Place to Life)
  •	First Impression (What you see): (e.g., "A crooked, three-story timber building leaning precariously," "A pristine white marble facade with glowing runes")
  •	Dominant Smells: (e.g., "Roasting meat, spilled ale, and damp wool," "Old parchment, arcane dust, and ozone")
  •	Ambient Sounds: (e.g., "The din of a cheerful crowd, clinking glasses, and a bard's off-key singing," "Whispering winds, the scratching of quills, a magical hum")
  •	Notable Textures/Temperatures: (e.g., "Sticky floors, a roaring hearth," "Cold stone walls, a constant magical chill")

⸻

🗺️ 3. Layout & Key Areas
  •	Main Floor / Common Area: (Description of the primary space)
  •	Upstairs / Private Quarters: (What's on the other floors?)
  •	Basement / Cellar: (What's hidden below?)
  •	Unique Feature or Room: (e.g., "A hidden fighting pit," "An observatory with a celestial telescope," "A secret alchemy lab")

⸻

🎲 4. Inhabitants & Roleplay Hooks
  •	The Proprietor: (Brief personality sketch of the owner/manager)
  •	Regulars / Staff: (Who is always here?)
  •	Potential Quests / Jobs: (What opportunities exist here?)
  •	Rumors about the place: (e.g., "It's built on an old cemetery," "The owner won the deed in a game of cards with a devil")
  •	What the party can get here: (e.g., "Rare ingredients," "A safe place to rest," "Information on a bounty," "A powerful enemy")

⸻

🧩 5. Secrets & History
  •	Hidden Secret: (e.g., "It's a front for a thieves' guild," "The basement contains a portal to another plane," "The proprietor is a retired adventurer")
  •	Brief History: (How did this place come to be?)
  •	What's *really* going on here?: (The underlying truth of the location)
"""

def _clean_building_sheet(raw_text: str) -> str:
    """Cleans up common artifacts and conversational filler from the model's raw output."""
    lines = raw_text.strip().split('\\n')
    cleaned_lines = [line for line in lines if "Here is the" not in line and "template filled out" not in line]
    return '\\n'.join(cleaned_lines).strip()


class BuildingSpec(BaseModel):
    """Input specification for building generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the building.")


class BuildingGeneratorAgent:
    """Agent for generating detailed buildings by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_building_sheet(self, input_spec: BuildingSpec) -> str:
        """Generates a detailed building sheet based on a freeform prompt."""
        system_prompt = "You are a master TTRPG storyteller and worldbuilder. Your task is to take a user's prompt and creatively fill out a detailed location sheet. Embellish and invent details where the user has been sparse. The goal is a rich, interesting, and usable location for a game master. Your response should only contain the filled-out template."
        
        user_prompt = f"""
Please create a building based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the location come alive.

{BUILDING_TEMPLATE}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8, # Slightly lower temp for more coherent structure
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = _clean_building_sheet(raw_sheet)
        return cleaned_sheet


# Convenience function for direct usage
def generate_building(input_spec: BuildingSpec) -> str:
    """Generates a building sheet using the BuildingGeneratorAgent."""
    agent = BuildingGeneratorAgent()
    return agent.generate_building_sheet(input_spec) 