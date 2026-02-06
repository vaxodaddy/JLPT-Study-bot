#!/bin/bash
# JLPT Study Bot - Quick Setup Script

echo "🎌 JLPT Study Bot - Setup Script 🎌"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.8+ required. You have Python $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your:"
    echo "   1. Telegram bot token"
    echo "   2. Telegram chat ID"
    echo "   3. AI backend configuration (Ollama/Gemini/Claude)"
    echo ""
    echo "Run: nano .env"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Make bot executable
chmod +x jlpt_bot.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env with your credentials: nano .env"
echo "   2. Start the bot: python3 jlpt_bot.py"
echo ""
echo "🤖 AI Backend Options:"
echo "   • Ollama (Local, Free): Install from ollama.com, then: ollama pull qwen2.5:14b"
echo "   • Gemini (Free tier): Get API key from aistudio.google.com"
echo "   • Claude (Paid): Get API key from console.anthropic.com"
echo ""
echo "📅 For daily automated lessons, set up cron:"
echo "   crontab -e"
echo "   Add: 0 8 * * * cd $(pwd) && python3 jlpt_bot.py --daily"
echo ""
