#!/usr/bin/env python3
"""
JLPT N1 Study Bot
A Telegram bot for Japanese language learning with AI-powered lessons and exercises.
Supports multiple AI backends: Ollama (local), Google Gemini, and Anthropic Claude.
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# AI Backend Configuration - Auto-detect which one is configured
OLLAMA_URL = os.getenv('OLLAMA_BASE_URL')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')
ANTHROPIC_KEY = os.getenv('ANTHROPIC_API_KEY')

# Determine which AI backend to use
AI_BACKEND = None
if OLLAMA_URL:
    AI_BACKEND = 'ollama'
    logger.info("Using Ollama backend")
elif GEMINI_KEY:
    AI_BACKEND = 'gemini'
    from google import genai
    client = genai.Client(api_key=GEMINI_KEY)
    MODEL_ID = "gemini-2.0-flash"
    logger.info("Using Gemini backend")
elif ANTHROPIC_KEY:
    AI_BACKEND = 'claude'
    from anthropic import Anthropic
    anthropic_client = Anthropic(api_key=ANTHROPIC_KEY)
    logger.info("Using Claude backend")
else:
    logger.error("No AI backend configured! Please set OLLAMA_BASE_URL, GEMINI_API_KEY, or ANTHROPIC_API_KEY in .env")
    sys.exit(1)


def scrape_todai_news():
    """Scrape a news article from Todai News"""
    try:
        url = "https://japanese.todaiinews.com/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article') or soup.find('div', class_='article')
        
        if article:
            title = article.find('h2') or article.find('h1')
            paragraphs = article.find_all('p')[:3]  # Get first 3 paragraphs
            
            title_text = title.get_text(strip=True) if title else "No title"
            content_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            return f"{title_text}\n\n{content_text}"
        
        return "Could not find article content"
        
    except Exception as e:
        logger.error(f"Error scraping news: {e}")
        return f"Error fetching news: {str(e)}"


def analyze_with_ai(text, task_type="daily_lesson"):
    """Use configured AI backend to analyze Japanese text"""
    
    prompts = {
        "daily_lesson": f"""You are a JLPT N1 study assistant. Analyze this Japanese news article:

{text}

Provide:
1. **Vocabulary** (10-15 N1 words with readings & meanings)
2. **Grammar Points** (3-5 N1 patterns with explanations)
3. **Kanji Analysis** (difficult kanji with readings)
4. **Questions** (5 comprehension questions)
5. **Summary** (brief English summary)

Format clearly for Telegram messaging.""",

        "analyze": f"""Analyze this Japanese text for a JLPT N1 student:

{text}

Provide:
- Key vocabulary with readings
- Grammar patterns used
- Kanji breakdown
- Brief English summary

Keep it educational and clear.""",

        "kanji_practice": """Generate 10 JLPT N1 kanji practice sentences:
- Use complex N1 kanji
- Provide furigana readings
- Include English translation
- Mark the target kanji

Make it challenging but educational.""",

        "grammar_drill": """Create 5 JLPT N1 grammar practice questions:
- Present sentence with blank
- Provide 4 multiple choice options
- Indicate correct answer
- Explain why it's correct

Focus on commonly confused N1 grammar patterns.""",

        "quiz": """Create a JLPT N1 quiz with 5 questions:
- 2 vocabulary questions
- 2 grammar questions
- 1 kanji reading question

Provide multiple choice options and answers at the end."""
    }
    
    prompt = prompts.get(task_type, prompts["analyze"])
    
    try:
        if AI_BACKEND == 'ollama':
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "qwen2.5:14b",  # Change this to your preferred model
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()['response']
            
        elif AI_BACKEND == 'gemini':
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            return response.text
            
        elif AI_BACKEND == 'claude':
            message = anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
            
    except Exception as e:
        logger.error(f"AI error ({AI_BACKEND}): {e}")
        return f"Error analyzing text: {str(e)}"


# Telegram Bot Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    backend_name = AI_BACKEND.capitalize()
    welcome_message = f"""🎌 Welcome to JLPT N1 Study Assistant! 🎌

Powered by {backend_name} AI

**Commands:**
/daily - Get today's news-based lesson
/analyze [text] - Analyze any Japanese text
/kanji - Practice kanji reading
/grammar - Grammar pattern drills
/quiz - Quick N1 quiz
/help - Show this message

You can also send me any Japanese text and I'll analyze it!

がんばって! 📚"""
    
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await start(update, context)


async def daily_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate daily lesson from news"""
    await update.message.reply_text("📰 Fetching today's news article... Please wait!")
    
    # Scrape news
    article = scrape_todai_news()
    
    # Analyze with AI
    await update.message.reply_text(f"🤖 Analyzing with {AI_BACKEND.capitalize()}...")
    lesson = analyze_with_ai(article, "daily_lesson")
    
    # Send lesson (split if too long)
    if len(lesson) > 4000:
        parts = [lesson[i:i+4000] for i in range(0, len(lesson), 4000)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(lesson)


async def analyze_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze text sent by user"""
    if not context.args:
        await update.message.reply_text("Please provide text to analyze!\nUsage: /analyze [Japanese text]")
        return
    
    text = ' '.join(context.args)
    await update.message.reply_text("🤖 Analyzing your text...")
    
    analysis = analyze_with_ai(text, "analyze")
    await update.message.reply_text(analysis)


async def kanji_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate kanji practice"""
    await update.message.reply_text("📝 Generating kanji practice...")
    
    practice = analyze_with_ai("", "kanji_practice")
    
    if len(practice) > 4000:
        parts = [practice[i:i+4000] for i in range(0, len(practice), 4000)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(practice)


async def grammar_drill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate grammar drills"""
    await update.message.reply_text("📖 Creating grammar drills...")
    
    drill = analyze_with_ai("", "grammar_drill")
    await update.message.reply_text(drill)


async def quiz_me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate quick quiz"""
    await update.message.reply_text("🎯 Preparing your quiz...")
    
    quiz = analyze_with_ai("", "quiz")
    await update.message.reply_text(quiz)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages (Japanese text to analyze)"""
    text = update.message.text
    
    # Check if it contains Japanese characters
    if any('\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9faf' for char in text):
        await update.message.reply_text("🤖 Analyzing your Japanese text...")
        analysis = analyze_with_ai(text, "analyze")
        await update.message.reply_text(analysis)
    else:
        await update.message.reply_text("Send me some Japanese text and I'll analyze it! Or use /help to see commands.")


async def send_daily_lesson_scheduled():
    """Send daily lesson to configured chat (for scheduled execution)"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Scrape and analyze
    article = scrape_todai_news()
    lesson = analyze_with_ai(article, "daily_lesson")
    
    # Send to user
    if len(lesson) > 4000:
        parts = [lesson[i:i+4000] for i in range(0, len(lesson), 4000)]
        for part in parts:
            await application.bot.send_message(chat_id=CHAT_ID, text=part)
    else:
        await application.bot.send_message(chat_id=CHAT_ID, text=lesson)
    
    logger.info("Daily lesson sent successfully")


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("daily", daily_lesson))
    application.add_handler(CommandHandler("analyze", analyze_text))
    application.add_handler(CommandHandler("kanji", kanji_practice))
    application.add_handler(CommandHandler("grammar", grammar_drill))
    application.add_handler(CommandHandler("quiz", quiz_me))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info(f"Starting JLPT Study Bot with {AI_BACKEND.capitalize()} backend...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--daily':
        # Run daily lesson and exit (for cron/scheduled tasks)
        asyncio.run(send_daily_lesson_scheduled())
    else:
        # Run bot normally
        main()
