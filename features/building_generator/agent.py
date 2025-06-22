from typing import Optional
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
    BUILDING_TEMPLATE_FULL = f.read()

with open(PROMPT_DIR / "brief.prompt", "r") as f:
    BUILDING_TEMPLATE_BRIEF = f.read()

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