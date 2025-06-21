# TTRPG Sidekick

An extensible AI TTRPG Sidekick that generates NPCs, quests, magic items, buildings, battlefields, session recaps, and character backstories for tabletop RPGs.

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

2. **Set up your environment for the first time:**
   ```bash
   # Copy the example environment configuration
   cp .envrc.example .envrc

   # Allow direnv to load the environment (required the first time)
   direnv allow
   ```
   This will:
   - Set up environment variables for the project
   - Add the project directory to your PATH so you can run `setup` (without `./`) from the project root
   - Automatically create and activate a Python virtual environment when you enter the directory

3. **Run the setup script:**
   ```bash
   setup
   ```
   (You can now just type `setup` instead of `./setup` as long as you're in the project root and direnv is active.)

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
   python test_battlefield_generator.py
   python test_backstory_generator.py
   ```

### Basic Usage

```bash
# Automatic detection
python main.py "a grumpy dwarf blacksmith named Borin"

# Explicit control with qualifiers
python main.py "/npc a young wizard who was orphaned"
python main.py "/backstory a young wizard who was orphaned"
python main.py "/quest find the missing crown"
python main.py "/building a seaside tavern"
python main.py "/magic_item a sword that controls fire"
python main.py "/battlefield a narrow mountain pass"

# With world context and brief mode
python main.py "/npc a merchant" --world "Eberron" --brief
```

## Project Overview

### Features

- **NPC Generator**: Create detailed NPCs with motives, secrets, and dialogue
- **Quest Generator**: Generate compelling quests with objectives, rewards, and story hooks
- **Magic Item Generator**: Design unique magical artifacts with properties, lore, and mechanics
- **Building Generator**: Create detailed locations and establishments
- **Battlefield Generator**: Design tactical combat environments with terrain and hazards
- **Character Backstory Generator**: Create rich character histories and personal development
- **Modular Architecture**: Each feature is a separate plugin
- **World Memory**: Persistent storage for campaign data
- **Structured Output**: All data uses Pydantic models for type safety
- **Smart Routing**: Automatically detects what type of content you want to generate
- **Explicit Qualifiers**: Use prefixes to explicitly specify content type
- **Local Model Support**: Use Ollama for local AI models or OpenAI for cloud models

### How It Works

The TTRPG Sidekick uses a simple but powerful architecture to understand and respond to user requests:

1. **Entry Point (`main.py`):** The main script captures the user's free-form prompt from the command line.
2. **LLM Service (`core/llm_service.py`):** A centralized singleton service initializes the language model client (either local Ollama or cloud OpenAI) based on the `.envrc` configuration. This client is then shared across the application.
3. **Router (`router.py`):** The user's prompt is sent to the `Router`, which first checks for explicit qualifiers, then uses the LLM to classify the user's intent if no qualifier is found.
4. **Generator Agent (`features/.../agent.py`):** Based on the detected intent, the main script calls the appropriate generator agent.
5. **Template Filling:** The agent combines the user's prompt with a detailed template and sends it to the LLM to be creatively filled out. The final, formatted text is then returned to the user.

### Project Structure

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
│   ├── battlefields/      # Battlefield generation
│   │   └── agent.py       # Battlefield generator agent
│   ├── backstories/       # Character backstory generation
│   │   └── agent.py       # Backstory generator agent
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
├── test_battlefield_generator.py # Battlefield generator tests
└── test_backstory_generator.py # Backstory generator tests
```

### Available Generators

#### NPC Generator
Creates detailed NPCs with name, race, class, motives, secrets, sample dialogue, appearance, personality, and background story.

#### Quest Generator
Creates compelling adventures with quest objectives, rewards, consequences, story hooks, plot points, NPCs involved, locations, and challenges.

#### Magic Item Generator
Designs unique artifacts with item properties, abilities, combat mechanics, bonuses, lore, history, roleplay hooks, personality, and balance considerations.

#### Building Generator
Creates detailed locations with physical description, atmosphere, layout, key areas, inhabitants, staff, roleplay opportunities, secrets, and history.

#### Battlefield Generator
Creates tactical combat environments with physical layout, terrain features, environmental hazards, cover options, tactical considerations, chokepoints, combat zones, objectives, forces, and deployment options.

#### Character Backstory Generator
Creates rich character histories with personal history, formative experiences, relationships, connections, goals, motivations, fears, skills development, abilities, and future aspirations.

### Available Qualifiers

| Qualifier | Purpose |
|-----------|---------|
| `/npc` | Generate NPCs |
| `/backstory` | Generate character backstories |
| `/quest` | Generate quests |
| `/building` | Generate buildings/locations |
| `/magic_item` | Generate magic items |
| `/battlefield` | Generate battlefields |

### Programmatic Usage

```python
from features.npc_generator.agent import NPCSpec, generate_npc
from features.quest_generator.agent import QuestSpec, generate_quest
from features.magic_items.agent import MagicItemSpec, generate_magic_item
from features.building_generator.agent import BuildingSpec, generate_building
from features.battlefields.agent import BattlefieldSpec, generate_battlefield
from features.backstories.agent import BackstorySpec, generate_backstory

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

# Generate a battlefield
battlefield_spec = BattlefieldSpec(
    world_name="Forgotten Realms",
    prompt="a narrow mountain pass where armies clash",
    brief=False
)
battlefield = generate_battlefield(battlefield_spec)

# Generate a backstory
backstory_spec = BackstorySpec(
    world_name="Forgotten Realms",
    prompt="a young wizard who was orphaned and discovered magical powers",
    brief=False
)
backstory = generate_backstory(backstory_spec)
```

## Helpful Information

### Setting Up Local Models

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

### Local Model Selection

When using local models, you have several options with different performance and quality trade-offs:

#### Model Comparison

| Model | Size | Quality | Speed | Memory | Best For |
|-------|------|---------|-------|--------|----------|
| **llama3** | ~4GB | High | Medium | 8GB+ | Best overall quality |
| **llama3.2** | ~4GB | Very High | Medium | 8GB+ | Latest and greatest |
| **phi3** | ~2GB | Good | Fast | 4GB+ | Good balance |
| **phi3.5** | ~2GB | Very Good | Fast | 4GB+ | Best value |
| **mistral** | ~4GB | High | Medium | 8GB+ | Good reasoning |
| **codellama** | ~4GB | High | Medium | 8GB+ | Code-focused tasks |

#### Performance Considerations

**Memory Requirements:**
- **4GB models** (llama3, llama3.2, mistral): Require 8GB+ RAM for optimal performance
- **2GB models** (phi3, phi3.5): Work well with 4GB+ RAM
- **Larger models** may require 16GB+ RAM for smooth operation

**Speed vs Quality Trade-offs:**
- **Faster models** (phi3, phi3.5): Generate responses quickly but may have less depth
- **Slower models** (llama3, llama3.2): Take longer but produce more detailed and coherent content
- **Quality models**: Better at following templates and maintaining consistency

**Hardware Recommendations:**
- **Minimum**: 4GB RAM, any modern CPU
- **Recommended**: 8GB+ RAM, recent CPU (2018+)
- **Optimal**: 16GB+ RAM, recent CPU with good single-thread performance

#### Model-Specific Recommendations

**For TTRPG Content Generation:**
- **llama3.2**: Best overall quality for creative writing and template following
- **phi3.5**: Excellent balance of speed and quality for most use cases
- **llama3**: Reliable fallback with good template adherence

**For Different Use Cases:**
- **Quick generation**: Use phi3 or phi3.5
- **High-quality output**: Use llama3.2 or llama3
- **Limited resources**: Use phi3 (smallest footprint)
- **Best value**: Use phi3.5 (good quality, reasonable speed)

#### Switching Models

To try different models:

```bash
# Download a new model
ollama pull phi3.5

# Update your configuration
export OLLAMA_MODEL="phi3.5"

# Test the new model
python main.py "/npc a wise old wizard"
```

#### Troubleshooting Performance

**If responses are slow:**
- Try a smaller model (phi3 instead of llama3)
- Ensure you have adequate RAM available
- Close other memory-intensive applications

**If quality is poor:**
- Switch to a larger model (llama3.2 instead of phi3)
- Check that the model downloaded completely
- Ensure you have enough RAM for the model

**If you get memory errors:**
- Use a smaller model
- Increase your system's swap/virtual memory
- Close other applications to free up RAM

### Virtual Environment

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

### Development

#### Adding New Features

1. Create a new directory in `features/`
2. Implement an `agent.py` with a generator class and convenience function
3. Use Pydantic models for input/output
4. Add routing logic to `router.py`
5. Update `main.py` to handle the new generator
6. Create a test file following the existing pattern

#### Code Style

- Use type hints for all functions
- Follow PEP 8 style guide
- Use Pydantic models for structured data
- Write docstrings for all public functions
- Include both full and brief templates for generators

### Troubleshooting

#### Virtual Environment Issues

If you encounter issues with the virtual environment:

1. **Remove the existing environment:**
   ```bash
   rm -rf .venv
   ```

2. **Recreate it:**
   ```bash
   direnv reload
   ```

#### Environment Variables Not Loading

If environment variables aren't loading:

1. **Check if direnv is properly configured:**
   ```bash
   direnv status
   ```

2. **Reallow the environment:**
   ```bash
   direnv allow
   ```

#### API Issues

If you're having trouble with the API:

1. **Check your API key is set correctly:**
   ```bash
   echo $OPENAI_API_KEY
   ```

2. **For Ollama, ensure the service is running:**
   ```bash
   curl http://localhost:11434/v1/models
   ```

#### Ollama Issues

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