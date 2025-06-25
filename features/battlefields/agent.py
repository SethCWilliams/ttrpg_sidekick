"""
Battlefield Generator Agent

Generates detailed battlefield descriptions with terrain, hazards, and tactical considerations.
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
    BATTLEFIELD_TEMPLATE_FULL = f.read()

with open(PROMPT_DIR / "brief.prompt", "r") as f:
    BATTLEFIELD_TEMPLATE_BRIEF = f.read()

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
        system_prompt = """You are a creative and imaginative TTRPG assistant. Your job is to fill out the provided battlefield sheet template using the user's prompt.

IMPORTANT CREATIVITY GUIDELINES:
- Be unexpected and avoid common tropes and stereotypes
- Create unique, memorable battlefields that surprise and delight
- Don't rely on typical fantasy clichés - subvert expectations
- Make each battlefield feel distinct and original
- Add unexpected terrain features, hazards, or tactical elements
- Think outside the box while still making the battlefield tactically interesting

You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."""
        
        # Choose the template based on the 'brief' flag
        template = BATTLEFIELD_TEMPLATE_BRIEF if input_spec.brief else BATTLEFIELD_TEMPLATE_FULL
        
        user_prompt = f"""
Please create a battlefield based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

CREATIVITY CHALLENGE: Make this battlefield truly unique and memorable. Avoid obvious tropes and create something that will surprise players. Think about what would make this battlefield stand out in a world full of fantasy combat environments.

Now, take that idea and fill out this template completely. Be creative and make the battlefield come alive with tactical depth and environmental storytelling.

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
        cleaned_sheet = clean_sheet(raw_sheet, BATTLEFIELD_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_battlefield(input_spec: BattlefieldSpec) -> str:
    """
    Generates a battlefield sheet using the BattlefieldGeneratorAgent.
    """
    agent = BattlefieldGeneratorAgent()
    return agent.generate_battlefield_sheet(input_spec) 