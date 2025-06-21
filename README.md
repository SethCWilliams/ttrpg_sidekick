# TTRPG Sidekick

An extensible AI TTRPG Sidekick that generates NPCs, quests, magic items, buildings, battlefields, session recaps, and character backstories for tabletop RPGs.

## Features

- **NPC Generator**: Create detailed NPCs with motives, secrets, and dialogue
- **Quest Generator**: Generate compelling quests with objectives, rewards, and story hooks
- **Magic Item Generator**: Design unique magical artifacts with properties, lore, and mechanics
- **Building Generator**: Create detailed locations and establishments
- **Modular Architecture**: Each feature is a separate plugin
- **World Memory**: Persistent storage for campaign data
- **Structured Output**: All data uses Pydantic models for type safety
- **Smart Routing**: Automatically detects what type of content you want to generate
- **Local Model Support**: Use Ollama for local AI models or OpenAI for cloud models

## Quick Start

### Prerequisites

- Python 3.8+
- direnv (recommended for environment management)
- OpenAI API key (for cloud models) OR Ollama (for local models)

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
   - Check prerequisites (direnv, Python 3)
   - Offer to install Ollama (optional)
   - Start Ollama service if needed
   - Download llama3 model if requested
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
   
   # Edit .envrc and add your API configuration
   # For OpenAI:
   # export OPENAI_API_KEY="sk-your-api-key-here"
   # export API_PROVIDER="openai"
   # 
   # For Ollama (local models):
   # export API_PROVIDER="ollama"
   # export OLLAMA_MODEL="llama3"
   
   # Allow direnv to load the environment
   direnv allow
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the generators:**
   ```bash
   python test_npc_generator.py
   python test_quest_generator.py
   python test_magic_item_generator.py
   ```

### Setting Up Local Models (Optional)

If you prefer to use local models instead of OpenAI:

1. **Install Ollama:**
   ```bash
   # macOS (with Homebrew)
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Download a model:**
   ```bash
   ollama pull llama3
   ```

4. **Configure your environment:**
   ```bash
   # In .envrc
   export API_PROVIDER="ollama"
   export OLLAMA_MODEL="llama3"
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
│   ├── notion_logger.py   # Notion integration
│   ├── llm_service.py     # Centralized LLM client management
│   ├── text_utils.py      # Text processing utilities
│   └── utils.py           # General utilities
├── features/              # Feature modules
│   ├── npc_generator/     # NPC generation
│   │   └── agent.py       # NPC generator agent
│   ├── quest_generator/   # Quest generation
│   │   └── agent.py       # Quest generator agent
│   ├── magic_items/       # Magic item generation
│   │   └── agent.py       # Magic item generator agent
│   ├── building_generator/ # Building generation
│   │   └── agent.py       # Building generator agent
│   ├── backstories/       # Character backstory generation
│   ├── battlefields/      # Battlefield generation
│   └── recaps/           # Session recap generation
├── data/                  # Data storage
│   ├── worlds/           # World-specific data
│   └── rulesets/         # RPG rulesets
├── interface/            # User interfaces
│   ├── api.py           # FastAPI server
│   ├── cli.py           # Command-line interface
│   └── discord_bot.py   # Discord bot interface
├── main.py              # Entry point
├── router.py            # Request routing
├── setup.sh             # Automated setup script
├── test_npc_generator.py # NPC generator tests
├── test_quest_generator.py # Quest generator tests
├── test_magic_item_generator.py # Magic item generator tests
└── test_building_generator.py # Building generator tests
```

## How It Works

The TTRPG Sidekick uses a simple but powerful architecture to understand and respond to user requests:

1. **Entry Point (`main.py`):** The main script captures the user's free-form prompt from the command line.
2. **LLM Service (`core/llm_service.py`):** A centralized singleton service initializes the language model client (either local Ollama or cloud OpenAI) based on the `.envrc` configuration. This client is then shared across the application.
3. **Router (`router.py`):** The user's prompt is sent to the `Router`, which uses the LLM to perform a single task: classify the user's intent (e.g., 'npc', 'building', 'quest', 'magic_item').
4. **Generator Agent (`features/.../agent.py`):** Based on the detected intent, the main script calls the appropriate generator agent.
5. **Template Filling:** The agent combines the user's prompt with a detailed template and sends it to the LLM to be creatively filled out. The final, formatted text is then returned to the user.

## How to Use

The TTRPG Sidekick is run from the command line. The main script is `main.py`, which takes your creative prompt as its primary argument.

### Basic Usage

```bash
python main.py "YOUR PROMPT HERE"
```

The application will automatically detect what type of content you want to create and generate a detailed sheet for you.

### Examples

**To generate an NPC:**
```bash
python main.py "a grumpy dwarf blacksmith named Borin"
```

**To generate a Building:**
```bash
python main.py "a seaside tavern called 'The Salty Siren'"
```

**To generate a Quest:**
```bash
python main.py "find the missing crown of the ancient king"
```

**To generate a Magic Item:**
```bash
python main.py "a sword that can control fire and was forged by a dragon"
```

**To generate more detailed content:**
```bash
python main.py "Create Osperado, the half-elf banker with a missing leg. He's secretly a member of the city's thieves' guild."
```

### Specifying a World

You can also provide a campaign world name for context, which can help the AI generate more relevant content.

```bash
python main.py "a mysterious wizard's tower" --world "Eberron"
```

### Brief Mode

For quicker, more concise output, use the `--brief` flag:

```bash
python main.py "a magic ring" --brief
```

## Usage

### NPC Generator

The NPC generator creates detailed NPCs with the following information:
- Name, race, and class
- Motives and secrets
- Sample dialogue
- Appearance and personality
- Background story

### Quest Generator

The quest generator creates compelling adventures with:
- Quest objectives and goals
- Rewards and consequences
- Story hooks and plot points
- NPCs involved
- Locations and challenges

### Magic Item Generator

The magic item generator designs unique artifacts with:
- Item properties and abilities
- Combat mechanics and bonuses
- Lore and history
- Roleplay hooks and personality
- Balance considerations

### Building Generator

The building generator creates detailed locations with:
- Physical description and atmosphere
- Layout and key areas
- Inhabitants and staff
- Roleplay opportunities
- Secrets and history

### Programmatic Usage

```python
from features.npc_generator.agent import NPCSpec, generate_npc
from features.quest_generator.agent import QuestSpec, generate_quest
from features.magic_items.agent import MagicItemSpec, generate_magic_item
from features.building_generator.agent import BuildingSpec, generate_building

# Generate an NPC
npc_spec = NPCSpec(
    world_name="Forgotten Realms",
    prompt="a wise old wizard who lives in a tower",
    brief=False
)
npc = generate_npc(npc_spec)

# Generate a quest
quest_spec = QuestSpec(
    world_name="Forgotten Realms",
    prompt="rescue the kidnapped princess from the dragon",
    brief=False
)
quest = generate_quest(quest_spec)

# Generate a magic item
item_spec = MagicItemSpec(
    world_name="Forgotten Realms",
    prompt="a sword that can control lightning",
    brief=False
)
magic_item = generate_magic_item(item_spec)

# Generate a building
building_spec = BuildingSpec(
    world_name="Forgotten Realms",
    prompt="a magical library filled with ancient tomes",
    brief=False
)
building = generate_building(building_spec)
```

### Environment Variables

The following environment variables can be configured in `.envrc`:

**For OpenAI:**
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `API_PROVIDER`: Set to "openai" (default)
- `OPENAI_MODEL`: Model to use (default: "gpt-4o")

**For Ollama (local models):**
- `API_PROVIDER`: Set to "ollama"
- `OLLAMA_BASE_URL`: Ollama server URL (default: "http://localhost:11434/v1")
- `OLLAMA_MODEL`: Model to use (default: "llama3")

**General:**
- `TTRPG_DATA_DIR`: Base data directory (default: "data")
- `TTRPG_WORLDS_DIR`: World data directory (default: "data/worlds")
- `TTRPG_RULESETS_DIR`: Rulesets directory (default: "data/rulesets")

## Development

### Adding New Features

1. Create a new directory in `features/`
2. Implement an `agent.py` with a generator class and convenience function
3. Use Pydantic models for input/output
4. Add routing logic to `router.py`
5. Update `main.py` to handle the new generator
6. Create a test file following the existing pattern

### Code Style

- Use type hints for all functions
- Follow PEP 8 style guide
- Use Pydantic models for structured data
- Write docstrings for all public functions
- Include both full and brief templates for generators

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

### API Issues

If you're having trouble with the API:

1. **Check your API key is set correctly:**
   ```bash
   echo $OPENAI_API_KEY
   ```

2. **For Ollama, ensure the service is running:**
   ```bash
   curl http://localhost:11434/v1/models
   ```

### Ollama Issues

If you're having trouble with Ollama:

1. **Check if Ollama is running:**
   ```bash
   ollama list
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Check available models:**
   ```bash
   ollama list
   ```

4. **Download a model if needed:**
   ```bash
   ollama pull llama3
   ```

## License

[Your License Here] 