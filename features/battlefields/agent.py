"""
Battlefield Generator Agent

Generates detailed battlefield descriptions with terrain, hazards, and tactical considerations.
"""

import os
from pydantic import BaseModel, Field
from openai import OpenAI
from core.llm_service import llm_service
from core.text_utils import clean_sheet

BATTLEFIELD_TEMPLATE_FULL = """
⚔️ Battlefield Profile: A Comprehensive Combat Environment Guide

📌 1. At a Glance (Quick DM Info)
  • Battlefield Name:
  • Location: (Region, City, Specific Area)
  • Size: (Small, Medium, Large, Massive)
  • Terrain Type: (Forest, Mountain, Urban, Desert, etc.)
  • Weather Conditions: (Current weather and its impact)
  • Time of Day: (Dawn, Day, Dusk, Night)
⸻
🗺️ 2. Physical Layout & Terrain
  • Overall Shape: (Circular, rectangular, irregular, etc.)
  • Key Features: (Hills, rivers, buildings, ruins, etc.)
  • Elevation Changes: (High ground, low areas, cliffs)
  • Cover Options: (Rocks, trees, walls, debris)
  • Movement Restrictions: (Difficult terrain, obstacles, barriers)
⸻
🌿 3. Environmental Hazards
  • Natural Hazards: (Lava, quicksand, unstable ground, etc.)
  • Weather Hazards: (Lightning, strong winds, fog, etc.)
  • Magical Hazards: (Wild magic zones, cursed areas, etc.)
  • Traps & Ambushes: (Hidden dangers, trigger conditions)
  • Environmental Damage: (What can hurt players?)
⸻
⚔️ 4. Tactical Considerations
  • High Ground: (Where is it and what advantage does it provide?)
  • Chokepoints: (Narrow passages, bridges, doorways)
  • Flanking Routes: (Ways to get around enemies)
  • Escape Routes: (How to retreat or flee)
  • Line of Sight: (What blocks vision and how?)
⸻
🎯 5. Combat Zones & Objectives
  • Primary Objective: (What are they fighting for?)
  • Secondary Objectives: (Bonus goals or side missions)
  • Control Points: (Strategic locations to hold)
  • Resource Locations: (Weapons, healing, supplies)
  • Victory Conditions: (How to win the battle)
⸻
👥 6. Forces & Deployment
  • Friendly Forces: (Allies, their positions, capabilities)
  • Enemy Forces: (Opponents, their positions, tactics)
  • Neutral Parties: (Civilians, wildlife, other threats)
  • Reinforcements: (Who might arrive and when?)
  • Special Units: (Elite troops, spellcasters, monsters)
⸻
🌙 7. Dynamic Elements
  • Changing Conditions: (How the battlefield evolves)
  • Time Pressure: (Urgency, deadlines, consequences)
  • Moral Choices: (Ethical decisions during combat)
  • Environmental Storytelling: (What the battlefield reveals)
  • Aftermath: (What happens after the battle?)
⸻
📊 8. Game Mechanics
  • Initiative Modifiers: (Advantage/disadvantage sources)
  • Movement Costs: (How terrain affects movement)
  • Cover Bonuses: (AC and saving throw modifiers)
  • Special Actions: (Unique tactical options)
  • Difficulty Rating: (How challenging is this battlefield?)
"""

BATTLEFIELD_TEMPLATE_BRIEF = """
⚔️ Battlefield Profile (Brief)

📌 1. At a Glance
  • Battlefield Name:
  • Location:
  • Size:
  • Terrain Type:
  • Weather Conditions:
⸻
🗺️ 2. Physical Layout & Terrain
  • Key Features:
  • Cover Options:
  • Movement Restrictions:
⸻
🌿 3. Environmental Hazards
  • Natural Hazards:
  • Magical Hazards:
⸻
⚔️ 4. Tactical Considerations
  • High Ground:
  • Chokepoints:
  • Line of Sight:
⸻
🎯 5. Combat Zones & Objectives
  • Primary Objective:
  • Control Points:
  • Victory Conditions:
"""

# Battlefield-specific filler phrases to remove
BATTLEFIELD_FILLER_PHRASES = [
    "Here is the battlefield profile",
    "Battlefield Profile: A Comprehensive Combat Environment Guide",
    "Here is the filled-out battlefield template",
    "Of course, here is the battlefield",
    "Behold the battlefield"
]

class BattlefieldSpec(BaseModel):
    """Input specification for battlefield generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the battlefield.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class BattlefieldGeneratorAgent:
    """Agent for generating detailed battlefields by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_battlefield_sheet(self, input_spec: BattlefieldSpec) -> str:
        """
        Generates a detailed battlefield sheet based on a freeform prompt.
        
        Args:
            input_spec: Specification for the battlefield to generate.
            
        Returns:
            A formatted string containing the completed battlefield template.
        """
        system_prompt = "You are a silent and efficient TTRPG assistant. Your only job is to fill out the provided battlefield sheet template using the user's prompt. You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."
        
        # Choose the template based on the 'brief' flag
        template = BATTLEFIELD_TEMPLATE_BRIEF if input_spec.brief else BATTLEFIELD_TEMPLATE_FULL
        
        user_prompt = f"""
Please create a battlefield based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the battlefield come alive with tactical depth and environmental storytelling.

{template}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.75, # Good balance for creativity and tactical thinking
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = clean_sheet(raw_sheet, BATTLEFIELD_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_battlefield(input_spec: BattlefieldSpec) -> str:
    """
    Generates a battlefield sheet using the BattlefieldGeneratorAgent.
    """
    agent = BattlefieldGeneratorAgent()
    return agent.generate_battlefield_sheet(input_spec) 