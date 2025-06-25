#!/usr/bin/env python3
"""
Smart Conversational Chat Interface for TTRPG Sidekick

Provides an interactive chat interface that intelligently routes to specific generators
when appropriate, while maintaining conversational capabilities for general questions.
"""

import os
import sys
from core.llm_service import llm_service
from router import Router
from features.npc_generator.agent import NPCSpec, generate_npc
from features.building_generator.agent import BuildingSpec, generate_building
from features.quest_generator.agent import QuestSpec, generate_quest
from features.magic_items.agent import MagicItemSpec, generate_magic_item
from features.battlefields.agent import BattlefieldSpec, generate_battlefield
from features.backstories.agent import BackstorySpec, generate_backstory


def print_welcome():
    """Print the welcome message."""
    print("🎲 Welcome to TTRPG Sidekick Chat!")
    print("=" * 50)
    print("I'm here to help with your TTRPG needs.")
    print("I can generate specific content or answer general questions.")
    print()
    print("I can create:")
    print("• NPCs (characters, merchants, villains, etc.)")
    print("• Buildings (taverns, shops, towers, etc.)")
    print("• Quests (missions, adventures, objectives)")
    print("• Magic Items (weapons, artifacts, enchanted objects)")
    print("• Battlefields (combat environments, tactical situations)")
    print("• Backstories (character histories, personal stories)")
    print()
    print("Commands:")
    print("• /help - Show this help message")
    print("• /clear - Clear conversation history")
    print("• /world <name> - Set the campaign world (optional)")
    print("• /brief - Toggle brief mode for next generation")
    print("• /quit or /exit - Exit the chat")
    print()
    print("You can also use qualifiers like /npc, /quest, etc. to force specific generators.")
    print("Example: '/npc a wise old wizard who lives in a tower'")
    print()
    print("Start chatting! (Type /help for commands)")
    print("-" * 50)


class SmartChatSession:
    """Manages a smart chat session that can route to generators or provide conversational responses."""
    
    def __init__(self, world_name: str = None):
        self.world_name = world_name
        self.conversation_history = []
        self.router = Router()
        self.brief_mode = False
        
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
        
    def generate_with_generator(self, intent: str, prompt: str) -> str:
        """Generate content using the appropriate generator."""
        try:
            # Use a generic world name if none is specified
            world_name = self.world_name if self.world_name else "Generic Fantasy"
            
            if intent == "npc":
                spec = NPCSpec(world_name=world_name, prompt=prompt, brief=self.brief_mode)
                result = generate_npc(spec)
            elif intent == "building":
                spec = BuildingSpec(world_name=world_name, prompt=prompt, brief=self.brief_mode)
                result = generate_building(spec)
            elif intent == "quest":
                spec = QuestSpec(world_name=world_name, prompt=prompt, brief=self.brief_mode)
                result = generate_quest(spec)
            elif intent == "magic_item":
                spec = MagicItemSpec(world_name=world_name, prompt=prompt, brief=self.brief_mode)
                result = generate_magic_item(spec)
            elif intent == "battlefield":
                spec = BattlefieldSpec(world_name=world_name, prompt=prompt, brief=self.brief_mode)
                result = generate_battlefield(spec)
            elif intent == "backstory":
                spec = BackstorySpec(world_name=world_name, prompt=prompt, brief=self.brief_mode)
                result = generate_backstory(spec)
            else:
                result = f"Sorry, I'm not sure how to handle that request. I can currently generate 'npc', 'building', 'quest', 'magic_item', 'battlefield', or 'backstory'."
            
            return result
        except Exception as e:
            return f"❌ Error generating content: {str(e)}"
    
    def handle_input(self, user_input: str) -> str:
        """Handle user input by either routing to a generator or providing conversational response."""
        
        # Route the request to see if it matches any generator
        routed_request = self.router.route_request(user_input)
        intent = routed_request.get("intent")
        prompt = routed_request.get("prompt", user_input)
        
        # If we detected a specific generator intent, use it
        if intent in ['npc', 'building', 'quest', 'magic_item', 'battlefield', 'backstory']:
            print(f"🔎 Intent Detected: {intent.upper()}")
            if self.brief_mode:
                print("📜 Brief mode enabled")
            
            result = self.generate_with_generator(intent, prompt)
            return result
        
        # Otherwise, provide a conversational response
        return self._get_conversational_response(user_input)
    
    def _get_conversational_response(self, user_input: str) -> str:
        """Get a conversational response from the model."""
        try:
            # Create messages for the API call
            messages = [
                {"role": "system", "content": "You are a helpful TTRPG assistant. You help with creating NPCs, quests, magic items, buildings, battlefields, and character backstories. Be creative and engaging in your responses. If someone asks for specific content generation, suggest they try being more specific about what they want to create."}
            ]
            
            # Add conversation history (keep last 10 messages to avoid token limits)
            recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
            messages.extend(recent_history)
            
            # Get response from the model
            response = llm_service.client.chat.completions.create(
                model=llm_service.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"


def main():
    """Main chat loop."""
    # Check environment
    api_provider = os.getenv("API_PROVIDER", "openai").lower()
    if api_provider == "openai" and (not os.getenv("OPENAI_API_KEY") or "your-api-key" in os.getenv("OPENAI_API_KEY")):
        print("❌ API_PROVIDER is set to 'openai', but OPENAI_API_KEY is not configured in .envrc.")
        sys.exit(1)
    elif api_provider == "ollama":
        print("✅ Using Ollama. Ensure the Ollama application is running.")
    
    # Initialize chat session
    session = SmartChatSession()
    
    print_welcome()
    
    try:
        while True:
            # Get user input
            try:
                world_display = session.world_name if session.world_name else "General"
                user_input = input(f"🎲 [{world_display}] > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower().split()[0]
                
                if command in ["/quit", "/exit"]:
                    print("👋 Goodbye!")
                    break
                elif command == "/help":
                    print_welcome()
                    continue
                elif command == "/clear":
                    session.clear_history()
                    print("🗑️  Conversation history cleared.")
                    continue
                elif command == "/world":
                    parts = user_input.split(maxsplit=1)
                    if len(parts) > 1:
                        session.world_name = parts[1]
                        print(f"🌍 World changed to: {session.world_name}")
                    else:
                        print("Usage: /world <world_name>")
                    continue
                elif command == "/brief":
                    session.brief_mode = not session.brief_mode
                    status = "enabled" if session.brief_mode else "disabled"
                    print(f"📜 Brief mode {status}")
                    continue
                else:
                    # Check if this might be a qualifier (like /npc, /quest, etc.)
                    qualifier = command[1:]  # Remove the leading slash
                    valid_qualifiers = ['npc', 'building', 'quest', 'magic_item', 'battlefield', 'backstory']
                    
                    if qualifier in valid_qualifiers:
                        # This is a valid qualifier, let the router handle it
                        pass  # Continue to the normal processing below
                    else:
                        print(f"❌ Unknown command: {command}")
                        continue
            
            # Add user message to history
            session.add_message("user", user_input)
            
            # Generate response
            print("🧠 Thinking...")
            response = session.handle_input(user_input)
            
            # Add assistant response to history
            session.add_message("assistant", response)
            
            # Print response
            print("-" * 50)
            print(response)
            print("-" * 50)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
