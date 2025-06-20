"""
Memory Service for TTRPG Sidekick

Handles world-specific memory and context storage.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class MemoryService:
    """Service for managing world-specific memory and context."""
    
    def __init__(self, data_dir: Optional[str] = None):
        # Use environment variable or default
        self.data_dir = Path(data_dir or os.getenv("TTRPG_WORLDS_DIR", "data/worlds"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_world_context(self, world_name: str) -> Dict[str, Any]:
        """Get context for a specific world."""
        world_file = self.data_dir / f"{world_name}.json"
        if world_file.exists():
            with open(world_file, 'r') as f:
                return json.load(f)
        return {"description": "A fantasy world", "npcs": [], "locations": []}
    
    def store_npc(self, world_name: str, npc_data: Dict[str, Any]) -> None:
        """Store an NPC in world memory."""
        world_file = self.data_dir / f"{world_name}.json"
        
        if world_file.exists():
            with open(world_file, 'r') as f:
                world_data = json.load(f)
        else:
            world_data = {"description": "A fantasy world", "npcs": [], "locations": []}
        
        world_data["npcs"].append(npc_data)
        
        with open(world_file, 'w') as f:
            json.dump(world_data, f, indent=2)
    
    def get_world_npcs(self, world_name: str) -> list:
        """Get all NPCs for a world."""
        world_context = self.get_world_context(world_name)
        return world_context.get("npcs", [])
