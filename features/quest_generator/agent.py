"""
Quest Generator Agent

Generates detailed TTRPG quests with objectives, rewards, NPCs, and plot hooks.
"""

import os
from pydantic import BaseModel, Field
from openai import OpenAI
from core.llm_service import llm_service
from core.text_utils import clean_sheet

# A detailed template for generating quests
QUEST_TEMPLATE_FULL = """
🎯 Quest Profile: A Comprehensive Adventure Guide

📌 1. Quest Overview (Quick DM Info)
  • Quest Title:
  • Quest Type: (e.g., Fetch Quest, Escort, Investigation, Combat, Social)
  • Difficulty Level: (Easy, Medium, Hard, Deadly)
  • Recommended Party Level:
  • Estimated Duration: (1 session, 2-3 sessions, Long-term arc)
  • Quest Giver: (Who is offering this quest?)
⸻
🎭 2. The Hook & Setup
  • The Problem: (What's wrong that needs fixing?)
  • The Request: (What does the quest giver want the party to do?)
  • Urgency: (Why does this need to be done now?)
  • Initial Clues: (What does the party know going in?)
⸻
🗺️ 3. Quest Objectives & Structure
  • Primary Objective: (The main goal)
  • Secondary Objectives: (Optional side goals that add depth)
  • Key Locations: (Where does this quest take place?)
  • Major NPCs: (Who will the party encounter?)
  • Obstacles & Challenges: (What stands in their way?)
⸻
💰 4. Rewards & Consequences
  • Monetary Reward: (Gold, gems, etc.)
  • Item Rewards: (Magic items, equipment, etc.)
  • Social Rewards: (Reputation, allies, favors, etc.)
  • Experience Points: (How much XP is this worth?)
  • Consequences of Failure: (What happens if they don't succeed?)
  • Consequences of Success: (How does this change the world?)
⸻
🎲 5. Roleplay & Story Elements
  • Moral Dilemmas: (Are there tough choices to make?)
  • Plot Twists: (Unexpected revelations or complications)
  • Character Development Opportunities: (How can PCs grow from this?)
  • World-Building Elements: (What does this reveal about the setting?)
⸻
⚔️ 6. Combat & Mechanics (If Applicable)
  • Potential Encounters: (What creatures or NPCs might they fight?)
  • Environmental Hazards: (Traps, weather, terrain challenges)
  • Special Mechanics: (Unique rules or systems for this quest)
  • Boss Fight: (If there's a climactic battle, describe it)
⸻
🧩 7. Secrets & Hidden Elements
  • Hidden Objectives: (Things the party might discover)
  • Secret NPCs: (Characters who might not be what they seem)
  • Alternative Solutions: (Different ways to complete the quest)
  • Long-term Implications: (How this quest affects future adventures)
"""

# A brief version of the quest template
QUEST_TEMPLATE_BRIEF = """
🎯 Quest Profile (Brief)

📌 1. Quest Overview
  • Quest Title:
  • Quest Type:
  • Difficulty Level:
  • Quest Giver:
⸻
🎭 2. The Hook & Setup
  • The Problem:
  • The Request:
  • Urgency:
⸻
🗺️ 3. Quest Objectives
  • Primary Objective:
  • Key Locations:
  • Major NPCs:
⸻
💰 4. Rewards & Consequences
  • Rewards:
  • Consequences of Failure:
  • Consequences of Success:
"""

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
        system_prompt = "You are a silent and efficient TTRPG assistant. Your only job is to fill out the provided quest sheet template using the user's prompt. You must fill out the template directly. Do not add any extra comments, introductions, or sign-offs. Your response should only contain the filled-out template."
        
        # Choose the template based on the 'brief' flag
        template = QUEST_TEMPLATE_BRIEF if input_spec.brief else QUEST_TEMPLATE_FULL

        user_prompt = f"""
Please create a quest based on the following idea:
---
USER PROMPT: "{input_spec.prompt}"
---

Now, take that idea and fill out this template completely. Be creative and make the quest come alive with interesting challenges, meaningful choices, and compelling rewards.

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
        cleaned_sheet = clean_sheet(raw_sheet, QUEST_FILLER_PHRASES)
        return cleaned_sheet


# Convenience function for direct usage
def generate_quest(input_spec: QuestSpec) -> str:
    """Generates a quest sheet using the QuestGeneratorAgent."""
    agent = QuestGeneratorAgent()
    return agent.generate_quest_sheet(input_spec) 