# Contributing to Tech Dashboard

Thank you for your interest in contributing to the Tech Dashboard project! 🎉

## Ways to Contribute

### 🐛 Bug Reports
- Use the GitHub Issues tab to report bugs
- Include detailed steps to reproduce the issue
- Provide your environment details (OS, Python version, etc.)

### 💡 Feature Requests
- Suggest new features via GitHub Issues
- Explain the use case and expected behavior
- Consider implementation complexity

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes
- Test your changes thoroughly
- Commit with clear messages (`git commit -m 'Add amazing feature'`)
- Push to your branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

## Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/tech-dashboard.git
   cd tech-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the scripts**
   ```bash
   python scripts/validate_config.py
   python scripts/fetch_tech_updates.py
   python scripts/generate_readme.py
   ```

## Code Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Include error handling
- Test your changes
- Update documentation if needed

## Adding New Features

### News Sources
To add new news sources, edit `fetch_tech_updates.py`:
- Add to the `news_sources` list in `fetch_tech_news()`
- Ensure proper error handling
- Test the RSS feed format

### Interest Categories
To add new interest categories:
- Update `config/interests.json` with the new category
- Update `validate_config.py` with the new category in `valid_interest_categories`
- Test the validation

### README Sections
To add new README sections:
- Edit `generate_readme.py`
- Add a new generation method
- Call it in the `generate_readme()` method
- Test the output

## Testing

- Always test your changes locally before submitting
- Ensure the GitHub Actions workflow passes
- Validate configuration changes with `validate_config.py`

## Questions?

Feel free to open an issue for questions or join the discussions!

Thank you for contributing! 🚀