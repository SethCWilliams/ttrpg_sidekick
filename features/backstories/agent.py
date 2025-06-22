"""
Character Backstory Generator Agent

Generates detailed character backstories with personal history, motivations, and character development.
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
    BACKSTORY_TEMPLATE_FULL = f.read()

with open(PROMPT_DIR / "brief.prompt", "r") as f:
    BACKSTORY_TEMPLATE_BRIEF = f.read()

# Backstory-specific filler phrases to remove
BACKSTORY_FILLER_PHRASES = [
    "Here is the character backstory",
    "Character Backstory: A Comprehensive Life Story",
    "Here is the filled-out backstory template",
    "Of course, here is the character backstory",
    "Behold the character's tale"
]

class BackstorySpec(BaseModel):
    """Input specification for character backstory generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the character backstory.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class BackstoryGeneratorAgent:
    """Agent for generating detailed character backstories by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_backstory_sheet(self, input_spec: BackstorySpec) -> str:
        """
        Generates a detailed character backstory sheet based on a freeform prompt.
        
        Args:
            input_spec: Specification for the character backstory to generate.
            
        Returns:
            A formatted string containing the completed backstory template.
        """
        system_prompt = "You are a silent and efficient TTRPG assistant. Your only job is to fill out the provided character backstory sheet template using the user's prompt. You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."
        
        # Choose the template based on the 'brief' flag
        template = BACKSTORY_TEMPLATE_BRIEF if input_spec.brief else BACKSTORY_TEMPLATE_FULL
        
        user_prompt = f"""
Please create a character backstory based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the character's story come alive with depth, emotion, and compelling narrative elements.

{template}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8, # Higher temperature for more creative storytelling
            max_tokens=2500,
        )
        
        raw_sheet = response.choices[0].message.content
        cleaned_sheet = clean_sheet(raw_sheet, BACKSTORY_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_backstory(input_spec: BackstorySpec) -> str:
    """
    Generates a character backstory sheet using the BackstoryGeneratorAgent.
    """
    agent = BackstoryGeneratorAgent()
    return agent.generate_backstory_sheet(input_spec) 