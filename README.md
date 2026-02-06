# 🎌 JLPT N1 Study Bot

A Telegram bot powered by AI to help you study for the JLPT N1 exam. Features daily news-based lessons, kanji practice, grammar drills, and interactive quizzes.

## ✨ Features

- 📰 **Daily Lessons** - Automated news article analysis with vocabulary, grammar, and comprehension questions
- 📝 **Kanji Practice** - Generate N1-level kanji practice sentences
- 📖 **Grammar Drills** - Interactive grammar pattern exercises
- 🎯 **Quizzes** - Quick N1 quizzes covering vocabulary, grammar, and kanji
- 🤖 **Text Analysis** - Send any Japanese text for instant analysis

## 🚀 Setup

### Prerequisites

- Python 3.8+
- A Telegram account
- One of the following AI backends:
  - Ollama (running locally - **recommended for free usage**)
  - Google Gemini API key (free tier available)
  - Anthropic Claude API key (paid)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/jlpt-study-bot.git
cd jlpt-study-bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your Telegram bot:**
   - Open Telegram and message [@BotFather](https://t.me/botfather)
   - Send `/newbot` and follow the instructions
   - Copy your bot token

4. **Get your Telegram Chat ID:**
   - Start a chat with your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for `"chat":{"id":123456789}` in the response

5. **Configure environment variables:**

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Choose ONE of the following:

# Option 1: Ollama (Local, Free)
OLLAMA_BASE_URL=http://localhost:11434
# Or if using ngrok: https://xxxx-xx-xx.ngrok-free.app

# Option 2: Google Gemini (Free tier)
GEMINI_API_KEY=your_gemini_api_key_here

# Option 3: Anthropic Claude (Paid)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Setting up AI Backend

#### Option 1: Ollama (Local, Free) - Recommended

**On your local machine:**

1. Install Ollama:
   - Windows: Download from [ollama.com](https://ollama.com/download)
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`
   - Mac: Download from [ollama.com](https://ollama.com/download)

2. Download a model:
```bash
ollama pull qwen2.5:14b
# OR for lighter model:
ollama pull qwen2.5:7b
```

3. Test it:
```bash
ollama run qwen2.5:14b
```

**If running bot on a different server (like EC2):**

Use ngrok to expose Ollama:
```bash
ngrok http 11434
```

Then use the ngrok URL in your `.env` file.

#### Option 2: Google Gemini

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Add to `.env` file

#### Option 3: Anthropic Claude

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add credits to your account
4. Add to `.env` file

## 🎮 Usage

### Running the Bot

**Start the bot:**
```bash
python jlpt_bot.py
```

**Run in background (Linux/Mac):**
```bash
nohup python jlpt_bot.py > bot.log 2>&1 &
```

**Stop background bot:**
```bash
pkill -f jlpt_bot.py
```

### Telegram Commands

Once the bot is running, use these commands in Telegram:

- `/start` - Start the bot and see welcome message
- `/help` - Show available commands
- `/daily` - Get today's news-based lesson
- `/analyze [text]` - Analyze any Japanese text
- `/kanji` - Generate kanji practice exercises
- `/grammar` - Get grammar pattern drills
- `/quiz` - Take a quick N1 quiz

**Or simply send any Japanese text** and the bot will analyze it automatically!

## 📅 Daily Automated Lessons

To receive daily lessons automatically at a specific time:

### Using Cron (Linux/Mac)

1. Open crontab:
```bash
crontab -e
```

2. Add this line (for 8 AM daily):
```cron
0 8 * * * cd /path/to/jlpt-study-bot && /usr/bin/python3 jlpt_bot.py --daily
```

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create a new task
3. Set trigger for daily at your preferred time
4. Set action: `python jlpt_bot.py --daily`
5. Set start in: your bot directory

## 🏗️ Architecture

```
User (Telegram) 
    ↓
Telegram Bot API
    ↓
JLPT Study Bot (Python)
    ↓
AI Backend (Ollama/Gemini/Claude)
    ↓
News Scraper (Todai News)
```

## 📁 Project Structure

```
jlpt-study-bot/
├── jlpt_bot.py          # Main bot script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in repo)
├── .env.example         # Example environment file
├── .gitignore          # Git ignore file
├── README.md           # This file
└── bot.log             # Log file (created when running)
```

## 🔧 Configuration

You can customize the bot by editing `jlpt_bot.py`:

- **News source**: Change the URL in `scrape_todai_news()`
- **AI prompts**: Modify prompts in `analyze_with_ai()`
- **Model selection**: Change the model name for your AI backend

## 🐛 Troubleshooting

**Bot doesn't respond:**
- Check if bot is running: `ps aux | grep jlpt_bot`
- Check logs: `tail -f bot.log`
- Verify your bot token is correct

**AI errors:**
- **Ollama**: Make sure Ollama is running: `ollama list`
- **Gemini**: Check rate limits (15/min, 1500/day on free tier)
- **Claude**: Verify you have credits in your account

**Can't find chat ID:**
- Send a message to your bot first
- Then check the getUpdates URL
- Look for the `"id"` field in the JSON response

## 💡 Tips

- Use **Qwen 2.5** models for best Japanese language performance
- The **14B model** gives better quality but needs more RAM/VRAM
- The **7B model** is faster and uses less resources
- Add delays between requests if hitting rate limits
- Use `nohup` or `screen` to keep bot running after SSH disconnect

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This bot is for educational purposes. News content is scraped from public sources. Please respect the terms of service of any websites you scrape.

## 📧 Support

If you encounter issues, please open an issue on GitHub.

---

がんばって！ Good luck with your JLPT N1 studies! 🎌📚
