# 🚀 Quick Start Guide

Get your JLPT Study Bot running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- A Telegram account
- (Optional) Ollama installed locally for free AI backend

## Step 1: Get the Code

```bash
git clone https://github.com/yourusername/jlpt-study-bot.git
cd jlpt-study-bot
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## Step 3: Create Your Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name: `My JLPT Study Bot`
4. Choose a username: `my_jlpt_bot` (must be unique)
5. Copy the API token you receive

## Step 4: Get Your Chat ID

1. Start a chat with your new bot (click the link from BotFather)
2. Send any message (like "hello")
3. Visit this URL in your browser (replace YOUR_TOKEN):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":123456789}` - that number is your chat ID

## Step 5: Choose Your AI Backend

### Option A: Ollama (Free, Runs Locally) ⭐ Recommended

**Install Ollama:**
- Windows/Mac: Download from [ollama.com](https://ollama.com)
- Linux: `curl -fsSL https://ollama.com/install.sh | sh`

**Download a model:**
```bash
ollama pull qwen2.5:14b
```

**Your `.env` should have:**
```env
OLLAMA_BASE_URL=http://localhost:11434
```

### Option B: Google Gemini (Free Tier)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

**Your `.env` should have:**
```env
GEMINI_API_KEY=your_api_key_here
```

### Option C: Anthropic Claude (Paid)

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Create an API key
3. Add credits to your account

**Your `.env` should have:**
```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Step 6: Configure Environment Variables

Create a `.env` file:
```bash
cp .env.example .env
nano .env
```

Add your credentials:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321

# Choose ONE AI backend:
OLLAMA_BASE_URL=http://localhost:11434
# OR
# GEMINI_API_KEY=your_key_here
# OR
# ANTHROPIC_API_KEY=your_key_here
```

## Step 7: Run the Bot

```bash
python3 jlpt_bot.py
```

You should see:
```
INFO - Starting JLPT Study Bot with Ollama backend...
```

## Step 8: Test It!

Open Telegram and send these commands to your bot:

1. `/start` - See the welcome message
2. `/daily` - Get a news-based lesson
3. `/kanji` - Practice kanji
4. `/quiz` - Take a quick quiz

Or just send any Japanese text!

## Troubleshooting

**Bot doesn't respond?**
- Check bot is running in terminal
- Verify your bot token is correct
- Make sure you're messaging the right bot

**AI errors?**
- **Ollama**: Is it running? Try `ollama list`
- **Gemini**: Check API key and rate limits
- **Claude**: Verify you have credits

**Can't find chat ID?**
- Make sure you sent a message to the bot first
- Check the URL carefully (use YOUR bot token)
- Look for the "id" number in the JSON

## Next Steps

- Set up [daily automated lessons](README.md#daily-automated-lessons)
- Customize prompts in `jlpt_bot.py`
- Add more news sources
- Star the repo if you find it useful! ⭐

## Need Help?

- Check the full [README](README.md)
- Open an [issue](https://github.com/yourusername/jlpt-study-bot/issues)
- Read [CONTRIBUTING](CONTRIBUTING.md) if you want to help improve the bot

---

がんばって! Happy studying! 🎌📚
