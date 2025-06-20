# TTRPG Sidekick

An extensible AI TTRPG Sidekick that generates NPCs, quests, magic items, buildings, battlefields, session recaps, and character backstories for tabletop RPGs.

## Features

- **NPC Generator**: Create detailed NPCs with motives, secrets, and dialogue
- **Modular Architecture**: Each feature is a separate plugin
- **World Memory**: Persistent storage for campaign data
- **Structured Output**: All data uses Pydantic models for type safety

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- direnv (recommended for environment management)

### Installation

#### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ttrpg_sidekick
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

   This will:
   - Check prerequisites
   - Set up direnv environment
   - Create a virtual environment
   - Install dependencies
   - Configure environment variables

#### Option 2: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ttrpg_sidekick
   ```

2. **Set up direnv:**
   ```bash
   # Copy the example configuration
   cp .envrc.example .envrc
   
   # Edit .envrc and add your OpenAI API key
   # export OPENAI_API_KEY="sk-your-api-key-here"
   
   # Allow direnv to load the environment
   direnv allow
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the NPC generator:**
   ```bash
   python test_npc_generator.py
   ```

## Virtual Environment

This project uses `direnv` to automatically manage a virtual environment. When you enter the project directory:

- A virtual environment is automatically created (if it doesn't exist)
- The virtual environment is automatically activated
- Environment variables are loaded
- Dependencies are available

When you leave the project directory, the virtual environment is automatically deactivated.

### Manual Virtual Environment (Alternative)

If you prefer to manage the virtual environment manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables manually
export OPENAI_API_KEY="your-api-key-here"
```

## Project Structure

```
ttrpg_sidekick/
├── .cursor/rules/          # Cursor IDE rules
├── core/                   # Shared services
│   ├── memory.py          # World memory management
│   ├── rule_engine.py     # RPG rules lookup
│   └── notion_logger.py   # Notion integration
├── features/              # Feature modules
│   └── npc_generator/     # NPC generation
│       └── agent.py       # NPC generator agent
├── data/                  # Data storage
│   ├── worlds/           # World-specific data
│   └── rulesets/         # RPG rulesets
├── interface/            # User interfaces
│   ├── api.py           # FastAPI server
│   └── cli.py           # Command-line interface
├── main.py              # Entry point
├── router.py            # Request routing
├── setup.sh             # Automated setup script
└── test_npc_generator.py # Test script
```

## How to Use

The TTRPG Sidekick is run from the command line. The main script is `main.py`, which takes your creative prompt as its primary argument.

### Basic Usage

```bash
python main.py "YOUR PROMPT HERE"
```

The application will automatically detect whether you want to create an NPC or a building and will generate a detailed sheet for you.

### Examples

**To generate an NPC:**
```bash
python main.py "a grumpy dwarf blacksmith named Borin"
```

**To generate a Building:**
```bash
python main.py "a seaside tavern called 'The Salty Siren'"
```

**To generate a more detailed NPC:**
```bash
python main.py "Create Osperado, the half-elf banker with a missing leg. He's secretly a member of the city's thieves' guild."
```

### Specifying a World

You can also provide a campaign world name for context, which can help the AI generate more relevant content.

```bash
python main.py "a mysterious wizard's tower" --world "Eberron"
```

## Usage

### NPC Generator

The NPC generator creates detailed NPCs with the following information:
- Name, race, and class
- Motives and secrets
- Sample dialogue
- Appearance and personality
- Background story

```python
from features.npc_generator.agent import NPCSpec, generate_npc
from core.memory import MemoryService

# Create specification
npc_spec = NPCSpec(
    world_name="Forgotten Realms",
    race_preference="Elf",
    class_preference="Wizard",
    role="Shopkeeper",
    location="Waterdeep",
    tone="Mysterious"
)

# Generate NPC
memory_service = MemoryService()
npc = generate_npc(npc_spec, memory_service)
```

### Environment Variables

The following environment variables can be configured in `.envrc`:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `TTRPG_DATA_DIR`: Base data directory (default: "data")
- `TTRPG_WORLDS_DIR`: World data directory (default: "data/worlds")
- `TTRPG_RULESETS_DIR`: Rulesets directory (default: "data/rulesets")

## Development

### Adding New Features

1. Create a new directory in `features/`
2. Implement an `agent.py` with a `generate()` function
3. Use Pydantic models for input/output
4. Integrate with the memory service for persistence

### Code Style

- Use type hints for all functions
- Follow PEP 8 style guide
- Use Pydantic models for structured data
- Write docstrings for all public functions

## Troubleshooting

### Virtual Environment Issues

If you encounter issues with the virtual environment:

1. **Remove the existing environment:**
   ```bash
   rm -rf .venv
   ```

2. **Recreate it:**
   ```bash
   direnv reload
   ```

### Environment Variables Not Loading

If environment variables aren't loading:

1. **Check if direnv is properly configured:**
   ```bash
   direnv status
   ```

2. **Reallow the environment:**
   ```bash
   direnv allow
   ```

## License

[Your License Here] 