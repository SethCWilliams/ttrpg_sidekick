"""
Character Backstory Generator Agent

Generates detailed character backstories with personal history, motivations, and character development.
"""

import os
from pydantic import BaseModel, Field
from openai import OpenAI
from core.llm_service import llm_service
from core.text_utils import clean_sheet

BACKSTORY_TEMPLATE_FULL = """
📖 Character Backstory: A Comprehensive Life Story

📌 1. Basic Information
  • Character Name:
  • Race/Species:
  • Class/Profession:
  • Age:
  • Place of Birth:
  • Current Residence:
⸻
👶 2. Early Life & Childhood
  • Family Background: (Parents, siblings, extended family)
  • Childhood Home: (Where they grew up, what it was like)
  • Early Influences: (People, events, or experiences that shaped them)
  • First Memories: (Earliest significant memories)
  • Childhood Dreams: (What they wanted to be when they grew up)
⸻
🎓 3. Education & Training
  • Formal Education: (Schools, apprenticeships, training)
  • Mentors & Teachers: (Who taught them their skills)
  • Key Lessons Learned: (Important knowledge or wisdom gained)
  • First Signs of Talent: (When their abilities first emerged)
  • Struggles & Challenges: (Difficulties in learning or training)
⸻
💔 4. Defining Moments & Trauma
  • Major Life Events: (Events that changed their life forever)
  • Losses & Tragedies: (Deaths, betrayals, failures)
  • Moments of Triumph: (Achievements, victories, breakthroughs)
  • Personal Failures: (Mistakes, regrets, things they wish they could change)
  • Turning Points: (Decisions that set them on their current path)
⸻
❤️ 5. Relationships & Connections
  • Romantic Relationships: (Past loves, current partner, heartbreaks)
  • Friends & Allies: (Close friends, trusted companions)
  • Rivals & Enemies: (People they compete with or oppose)
  • Family Ties: (Current relationship with family members)
  • Mentors & Students: (People they guide or who guide them)
⸻
🎯 6. Goals & Motivations
  • Primary Goal: (Their main driving force, what they want most)
  • Secondary Goals: (Other important objectives)
  • Fears & Insecurities: (What scares them, what they're afraid of)
  • Values & Beliefs: (What they stand for, their moral code)
  • What They're Willing to Sacrifice: (What they'd give up for their goals)
⸻
🌍 7. World Experience & Travel
  • Places They've Been: (Cities, countries, realms they've visited)
  • Cultures They've Encountered: (Different societies and customs)
  • Languages They Know: (Languages spoken, how they learned them)
  • Notable Experiences Abroad: (Memorable events from their travels)
  • Places They Want to Visit: (Destinations they dream of)
⸻
⚔️ 8. Skills & Abilities
  • Natural Talents: (Things they're naturally good at)
  • Learned Skills: (Abilities they've worked hard to develop)
  • Unique Abilities: (Special powers, magic, or rare skills)
  • Weaknesses: (Areas where they struggle or are vulnerable)
  • How They Use Their Skills: (How they apply their abilities)
⸻
🎭 9. Personality & Character
  • Core Personality Traits: (Their fundamental characteristics)
  • Quirks & Habits: (Unique behaviors, mannerisms, or rituals)
  • How They Handle Stress: (Their coping mechanisms)
  • Sense of Humor: (What makes them laugh, their style of humor)
  • How Others See Them: (Their reputation, how they're perceived)
⸻
🔮 10. Future Aspirations & Destiny
  • Short-term Goals: (What they want to accomplish soon)
  • Long-term Dreams: (Their ultimate aspirations)
  • Prophecies or Omens: (Any predictions about their future)
  • Legacy They Want to Leave: (How they want to be remembered)
  • What They're Still Searching For: (Something missing in their life)
"""

BACKSTORY_TEMPLATE_BRIEF = """
📖 Character Backstory (Brief)

📌 1. Basic Information
  • Character Name:
  • Race/Species:
  • Class/Profession:
  • Age:
⸻
👶 2. Early Life & Childhood
  • Family Background:
  • Early Influences:
  • First Signs of Talent:
⸻
💔 3. Defining Moments & Trauma
  • Major Life Events:
  • Personal Failures:
  • Turning Points:
⸻
❤️ 4. Relationships & Connections
  • Friends & Allies:
  • Rivals & Enemies:
  • Family Ties:
⸻
🎯 5. Goals & Motivations
  • Primary Goal:
  • Fears & Insecurities:
  • Values & Beliefs:
⸻
⚔️ 6. Skills & Abilities
  • Natural Talents:
  • Learned Skills:
  • Weaknesses:
⸻
🎭 7. Personality & Character
  • Core Personality Traits:
  • Quirks & Habits:
  • How Others See Them:
"""

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