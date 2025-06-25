"""
NPC Generator Agent

Generates detailed NPCs with names, races, classes, motives, secrets, and dialogue.
"""

import os
from pydantic import BaseModel, Field
from openai import OpenAI
from pathlib import Path
from core.llm_service import llm_service
from core.text_utils import clean_sheet

# Path to the directory containing prompts
PROMPT_DIR = Path(__file__).parent / "prompts"

# Load prompt templates from files
with open(PROMPT_DIR / "full.prompt", "r") as f:
    NPC_TEMPLATE_FULL = f.read()

with open(PROMPT_DIR / "brief.prompt", "r") as f:
    NPC_TEMPLATE_BRIEF = f.read()

# NPC-specific filler phrases to remove
NPC_FILLER_PHRASES = [
    "Here is the NPC template filled out",
    "NPC Template Fully Spun",
    "An Elixir for Storycrafting",
    "Combat & Mechanical (Optional Crafting) Complete!",
    "Oh, behold the enigmatic"
]

class NPCSpec(BaseModel):
    """Input specification for NPC generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the NPC.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class NPCGeneratorAgent:
    """Agent for generating detailed NPCs by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_npc_sheet(self, input_spec: NPCSpec) -> str:
        """
        Generates a detailed NPC character sheet based on a freeform prompt.
        
        Args:
            input_spec: Specification for the NPC to generate.
            
        Returns:
            A formatted string containing the completed NPC template.
        """
        system_prompt = """You are a creative and imaginative TTRPG assistant. Your job is to fill out the provided character sheet template using the user's prompt.

IMPORTANT CREATIVITY GUIDELINES:
- Be unexpected and avoid common tropes and stereotypes
- Create unique, memorable characters that surprise and delight
- Don't rely on typical fantasy clichés - subvert expectations
- Make each character feel distinct and original
- Add unexpected quirks, motivations, or background elements
- Think outside the box while still making the character believable

You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."""
        
        # Choose the template based on the 'brief' flag
        template = NPC_TEMPLATE_BRIEF if input_spec.brief else NPC_TEMPLATE_FULL
        
        user_prompt = f"""
Please create an NPC based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

CREATIVITY CHALLENGE: Make this character truly unique and memorable. Avoid obvious tropes and create something that will surprise players. Think about what would make this character stand out in a world full of fantasy characters.

Now, take that idea and fill out this template completely. Be creative and make the character come alive.

{template}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9, # Increased for more creative and diverse outputs
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = clean_sheet(raw_sheet, NPC_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_npc(input_spec: NPCSpec) -> str:
    """
    Generates an NPC character sheet using the NPC generator agent.
    """
    agent = NPCGeneratorAgent()
    return agent.generate_npc_sheet(input_spec) 