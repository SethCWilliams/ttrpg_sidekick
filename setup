#!/bin/bash

# TTRPG Sidekick Setup Script
# This script sets up the development environment

set -e  # Exit on any error

echo "🎲 Setting up TTRPG Sidekick development environment..."
echo "=================================================="

# Check if direnv is installed
if ! command -v direnv &> /dev/null; then
    echo "❌ direnv is not installed. Please install it first:"
    echo "   macOS: brew install direnv"
    echo "   Ubuntu/Debian: sudo apt-get install direnv"
    echo "   Or visit: https://direnv.net/"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check for Ollama installation
echo ""
echo "🤖 Checking for Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed."
    echo ""
    echo "Ollama allows you to run local language models instead of using OpenAI."
    echo "This is optional - you can still use OpenAI if you prefer."
    echo ""
    read -p "Would you like to install Ollama? (y/n): " install_ollama
    
    if [[ $install_ollama =~ ^[Yy]$ ]]; then
        echo "📥 Installing Ollama..."
        
        # Detect OS and install accordingly
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install ollama
            else
                echo "❌ Homebrew not found. Please install Homebrew first:"
                echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                echo "   Then run: brew install ollama"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            curl -fsSL https://ollama.ai/install.sh | sh
        else
            echo "❌ Unsupported OS. Please install Ollama manually:"
            echo "   Visit: https://ollama.ai/download"
            exit 1
        fi
        
        echo "✅ Ollama installed successfully!"
    else
        echo "ℹ️  Skipping Ollama installation. You can install it later if needed."
    fi
else
    echo "✅ Ollama is already installed"
fi

# Check if Ollama is running and offer to start it
if command -v ollama &> /dev/null; then
    echo ""
    echo "🔍 Checking if Ollama service is running..."
    if ! curl -s http://localhost:11434/v1/models &> /dev/null; then
        echo "⚠️  Ollama service is not running."
        read -p "Would you like to start Ollama now? (y/n): " start_ollama
        
        if [[ $start_ollama =~ ^[Yy]$ ]]; then
            echo "🚀 Starting Ollama service..."
            ollama serve &
            sleep 3  # Give it a moment to start
            
            # Check if it started successfully
            if curl -s http://localhost:11434/v1/models &> /dev/null; then
                echo "✅ Ollama service started successfully!"
            else
                echo "❌ Failed to start Ollama service. Please start it manually:"
                echo "   ollama serve"
            fi
        else
            echo "ℹ️  You'll need to start Ollama manually before using local models:"
            echo "   ollama serve"
        fi
    else
        echo "✅ Ollama service is running"
    fi
    
    # Check for llama3 model
    echo ""
    echo "🔍 Checking for llama3 model..."
    if ! ollama list | grep -q "llama3"; then
        echo "⚠️  llama3 model is not installed."
        read -p "Would you like to download llama3? (This may take a while) (y/n): " download_llama3
        
        if [[ $download_llama3 =~ ^[Yy]$ ]]; then
            echo "📥 Downloading llama3 model..."
            ollama pull llama3
            echo "✅ llama3 model downloaded successfully!"
        else
            echo "ℹ️  Skipping llama3 download. You can download it later with:"
            echo "   ollama pull llama3"
        fi
    else
        echo "✅ llama3 model is already installed"
    fi
fi

# Allow direnv to load the environment
echo ""
echo "🔧 Setting up direnv environment..."
direnv allow

# The virtual environment will be created automatically by direnv
echo "🐍 Virtual environment will be created automatically by direnv"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. The virtual environment is now active (you'll see (.venv) in your prompt)"
echo "2. Your environment variables are loaded"
echo "3. You can now run: python test_npc_generator.py"
echo ""
echo "Configuration options:"
echo "- For OpenAI: Set OPENAI_API_KEY in .envrc"
echo "- For Ollama: Set API_PROVIDER=ollama in .envrc"
echo ""
echo "To deactivate the virtual environment, simply leave the project directory"
echo "To reactivate it, return to the project directory" 