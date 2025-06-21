"""
Magic Item Generator Agent

Generates detailed magic items with properties, lore, and mechanics.
"""

import os
from pydantic import BaseModel, Field
from openai import OpenAI
from core.llm_service import llm_service
from core.text_utils import clean_sheet

MAGIC_ITEM_TEMPLATE_FULL = """
⚔️ Magic Item Profile: A Comprehensive Artifact Guide

📌 1. At a Glance (Quick DM Info)
  • Item Name:
  • Item Type: (Weapon, Armor, Wondrous Item, Ring, etc.)
  • Rarity: (Common, Uncommon, Rare, Very Rare, Legendary)
  • Attunement: (Yes/No - if yes, by whom)
  • Estimated Value: (Gold pieces or "Priceless")
⸻
✨ 2. Physical Description
  • Appearance: (What does it look like?)
  • Materials: (What is it made of?)
  • Size & Weight: (How big/heavy is it?)
  • Visual Effects: (Does it glow, shimmer, etc.?)
⸻
🔮 3. Magical Properties
  • Primary Ability: (Main magical effect)
  • Secondary Abilities: (Additional powers)
  • Activation: (How is it used? Command word, attunement, etc.)
  • Duration: (How long do effects last?)
  • Charges/Limitations: (Any restrictions or costs?)
⸻
⚔️ 4. Combat & Mechanics
  • Combat Bonuses: (Attack, damage, AC, etc.)
  • Special Actions: (Unique combat abilities)
  • Saving Throws: (Any saves it grants or requires)
  • Damage Types: (What kind of damage does it deal/resist?)
⸻
📖 5. Lore & History
  • Creator: (Who made it? When? Why?)
  • Previous Owners: (Famous wielders or owners)
  • Legendary Deeds: (What has it accomplished?)
  • Current Location: (Where might it be found?)
⸻
🎭 6. Roleplay & Story Hooks
  • Personality: (Does it have a mind of its own?)
  • Quirks: (Any strange behaviors or requirements?)
  • Curses: (Any negative side effects?)
  • Quest Potential: (What stories could it inspire?)
⸻
⚖️ 7. Balance & Game Impact
  • Power Level: (How strong is it for its tier?)
  • Party Impact: (How will it affect gameplay?)
  • Recommended Level: (When should players get this?)
  • Variants: (Alternative versions or modifications)
"""

MAGIC_ITEM_TEMPLATE_BRIEF = """
⚔️ Magic Item Profile (Brief)

📌 1. At a Glance
  • Item Name:
  • Item Type:
  • Rarity:
  • Attunement:
⸻
✨ 2. Physical Description
  • Appearance:
  • Visual Effects:
⸻
🔮 3. Magical Properties
  • Primary Ability:
  • Activation:
  • Charges/Limitations:
⸻
📖 4. Lore & History
  • Creator:
  • Legendary Deeds:
⸻
🎭 5. Roleplay & Story Hooks
  • Personality:
  • Quest Potential:
"""

# Magic item-specific filler phrases to remove
MAGIC_ITEM_FILLER_PHRASES = [
    "Here is the magic item profile",
    "Magic Item Profile: A Comprehensive Artifact Guide",
    "Here is the filled-out magic item template",
    "Of course, here is the magic item",
    "Behold the magical artifact"
]

class MagicItemSpec(BaseModel):
    """Input specification for magic item generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the magic item.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class MagicItemGeneratorAgent:
    """Agent for generating detailed magic items by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_magic_item_sheet(self, input_spec: MagicItemSpec) -> str:
        """
        Generates a detailed magic item sheet based on a freeform prompt.
        
        Args:
            input_spec: Specification for the magic item to generate.
            
        Returns:
            A formatted string containing the completed magic item template.
        """
        system_prompt = "You are a silent and efficient TTRPG assistant. Your only job is to fill out the provided magic item sheet template using the user's prompt. You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."
        
        # Choose the template based on the 'brief' flag
        template = MAGIC_ITEM_TEMPLATE_BRIEF if input_spec.brief else MAGIC_ITEM_TEMPLATE_FULL
        
        user_prompt = f"""
Please create a magic item based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the magic item come alive with interesting properties and lore.

{template}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.75, # Good balance for creativity and consistency
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = clean_sheet(raw_sheet, MAGIC_ITEM_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_magic_item(input_spec: MagicItemSpec) -> str:
    """
    Generates a magic item sheet using the MagicItemGeneratorAgent.
    """
    agent = MagicItemGeneratorAgent()
    return agent.generate_magic_item_sheet(input_spec) 