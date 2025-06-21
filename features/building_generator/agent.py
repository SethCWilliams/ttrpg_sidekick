from typing import Optional
import os
from pydantic import BaseModel, Field
from openai import OpenAI
from core.llm_service import llm_service
from core.text_utils import clean_sheet

# A detailed template for generating buildings
BUILDING_TEMPLATE_FULL = """
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

# A new, brief version of the template
BUILDING_TEMPLATE_BRIEF = """
🏰 Building Profile (Brief)

📌 1. At a Glance
	•	Building Name:
	•	Primary Function:
	•	Location:
	•	Key Figure / Proprietor:
	•	General Vibe:
⸻
👀 2. Sensory Details
	•	First Impression (What you see):
	•	Dominant Smells:
	•	Ambient Sounds:
⸻
🎲 3. Inhabitants & Roleplay Hooks
	•	The Proprietor:
	•	Potential Quests / Jobs:
	•	What the party can get here:
"""

# Building-specific filler phrases to remove
BUILDING_FILLER_PHRASES = [
    "Here is the building profile",
    "Here is the building template filled out", 
    "Building Profile: A Comprehensive Location Guide",
    "Of course, here is the filled-out template"
]

class BuildingSpec(BaseModel):
    """Input specification for building generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the building.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class BuildingGeneratorAgent:
    """Agent for generating detailed buildings by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_building_sheet(self, input_spec: BuildingSpec) -> str:
        """Generates a detailed building sheet based on a freeform prompt."""
        system_prompt = "You are a silent and efficient TTRPG assistant. Your only job is to fill out the provided location sheet template using the user's prompt. You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."
        
        # Choose the template based on the 'brief' flag
        template = BUILDING_TEMPLATE_BRIEF if input_spec.brief else BUILDING_TEMPLATE_FULL

        user_prompt = f"""
Please create a building based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the location come alive.

{template}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = clean_sheet(raw_sheet, BUILDING_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_building(input_spec: BuildingSpec) -> str:
    """Generates a building sheet using the BuildingGeneratorAgent."""
    agent = BuildingGeneratorAgent()
    return agent.generate_building_sheet(input_spec) 