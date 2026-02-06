# Contributing to JLPT Study Bot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, AI backend)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- How it might work

### Code Contributions

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
   
   Use commit prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for improvements to existing features
   - `Docs:` for documentation changes

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/jlpt-study-bot.git
   cd jlpt-study-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file (copy from `.env.example`)

4. Run the bot locally to test:
   ```bash
   python3 jlpt_bot.py
   ```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions
- Keep functions focused and not too long
- Comment complex logic

## Testing

Before submitting a PR:
- Test all bot commands
- Verify compatibility with all AI backends
- Check that news scraping still works
- Test daily lesson scheduling

## Areas That Need Help

- [ ] Unit tests
- [ ] More news sources
- [ ] Additional study features (flashcards, spaced repetition)
- [ ] Support for other JLPT levels (N2, N3, etc.)
- [ ] Better error handling
- [ ] Performance optimizations
- [ ] Multi-language support for the bot interface
- [ ] Web dashboard

## Questions?

Feel free to open an issue for any questions about contributing!

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to learn and improve!
