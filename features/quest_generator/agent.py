"""
Quest Generator Agent

Generates detailed TTRPG quests with objectives, rewards, NPCs, and plot hooks.
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
    QUEST_TEMPLATE_FULL = f.read()

with open(PROMPT_DIR / "brief.prompt", "r") as f:
    QUEST_TEMPLATE_BRIEF = f.read()

# Quest-specific filler phrases to remove
QUEST_FILLER_PHRASES = [
    "Here is the quest profile",
    "Here is the quest template filled out",
    "Quest Profile: A Comprehensive Adventure Guide",
    "Of course, here is the filled-out template"
]

class QuestSpec(BaseModel):
    """Input specification for quest generation."""
    world_name: str = Field(..., description="Name of the world/campaign")
    prompt: str = Field(..., description="A freeform text prompt describing the quest.")
    brief: bool = Field(False, description="Whether to generate a brief version of the sheet.")


class QuestGeneratorAgent:
    """Agent for generating detailed quests by filling out a template."""
    
    def __init__(self):
        self.client = llm_service.client
        self.model = llm_service.model

    def generate_quest_sheet(self, input_spec: QuestSpec) -> str:
        """Generates a detailed quest sheet based on a freeform prompt."""
        system_prompt = """You are a creative and imaginative TTRPG assistant. Your job is to fill out the provided quest sheet template using the user's prompt.

IMPORTANT CREATIVITY GUIDELINES:
- Be unexpected and avoid common tropes and stereotypes
- Create unique, memorable quests that surprise and delight
- Don't rely on typical fantasy clichés - subvert expectations
- Make each quest feel distinct and original
- Add unexpected twists, moral dilemmas, or unique challenges
- Think outside the box while still making the quest believable and playable

You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."""
        
        # Choose the template based on the 'brief' flag
        template = QUEST_TEMPLATE_BRIEF if input_spec.brief else QUEST_TEMPLATE_FULL

        user_prompt = f"""
Please create a quest based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

CREATIVITY CHALLENGE: Make this quest truly unique and memorable. Avoid obvious tropes and create something that will surprise players. Think about what would make this quest stand out in a world full of fantasy adventures.

Now, take that idea and fill out this template completely. Be creative and make the quest come alive with interesting challenges, meaningful choices, and compelling rewards.

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
        cleaned_sheet = clean_sheet(raw_sheet, QUEST_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_quest(input_spec: QuestSpec) -> str:
    """Generates a quest sheet using the QuestGeneratorAgent."""
    agent = QuestGeneratorAgent()
    return agent.generate_quest_sheet(input_spec) 