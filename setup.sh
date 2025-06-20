#!/bin/bash

# TTRPG Sidekick Setup Script
# This script sets up the development environment

set -e  # Exit on any error

echo "🎲 Setting up TTRPG Sidekick development environment..."
echo "=" * 50

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

# Allow direnv to load the environment
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
echo "To deactivate the virtual environment, simply leave the project directory"
echo "To reactivate it, return to the project directory" 