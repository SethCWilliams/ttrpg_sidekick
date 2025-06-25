"""
Magic Item Generator Agent

Generates detailed magic items with properties, lore, and mechanics.
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
    MAGIC_ITEM_TEMPLATE_FULL = f.read()

with open(PROMPT_DIR / "brief.prompt", "r") as f:
    MAGIC_ITEM_TEMPLATE_BRIEF = f.read()

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
        system_prompt = """You are a creative and imaginative TTRPG assistant. Your job is to fill out the provided magic item sheet template using the user's prompt.

IMPORTANT CREATIVITY GUIDELINES:
- Be unexpected and avoid common tropes and stereotypes
- Create unique, memorable magic items that surprise and delight
- Don't rely on typical fantasy clichés - subvert expectations
- Make each item feel distinct and original
- Add unexpected properties, lore, or unique mechanics
- Think outside the box while still making the item balanced and interesting

You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."""
        
        # Choose the template based on the 'brief' flag
        template = MAGIC_ITEM_TEMPLATE_BRIEF if input_spec.brief else MAGIC_ITEM_TEMPLATE_FULL
        
        user_prompt = f"""
Please create a magic item based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

CREATIVITY CHALLENGE: Make this magic item truly unique and memorable. Avoid obvious tropes and create something that will surprise players. Think about what would make this item stand out in a world full of fantasy artifacts.

Now, take that idea and fill out this template completely. Be creative and make the magic item come alive with interesting properties and lore.

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
        cleaned_sheet = clean_sheet(raw_sheet, MAGIC_ITEM_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_magic_item(input_spec: MagicItemSpec) -> str:
    """
    Generates a magic item sheet using the MagicItemGeneratorAgent.
    """
    agent = MagicItemGeneratorAgent()
    return agent.generate_magic_item_sheet(input_spec) 