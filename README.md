# 🎭 Interactive Story Generator

An AI-powered interactive storytelling web application built with Streamlit and Google's Gemini API.

## Features

- 📝 **User-Driven Stories**: Start with your own story prompt
- 🤖 **AI-Generated Scenes**: Gemini AI creates immersive story scenes
- 🔀 **Branching Narratives**: Choose between 2 options at each scene
- 📖 **Story History**: Track your journey through the story
- 🎬 **Dynamic Endings**: Experience unique conclusions based on your choices

## Project Structure

```
swiggy/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
├── models/
│   ├── __init__.py
│   └── story.py               # Data models (Story, Scene, Choice)
├── services/
│   ├── __init__.py
│   ├── gemini_service.py      # Gemini API integration
│   └── story_service.py       # Story generation logic
├── utils/
│   ├── __init__.py
│   ├── prompt_templates.py    # AI prompt templates
│   └── session_manager.py     # Session state management
└── components/
    ├── __init__.py
    ├── story_display.py       # Scene display component
    ├── choice_selector.py     # Choice selection UI
    └── story_history.py       # Story progress display
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### 2. Installation

1. **Activate your virtual environment** (if not already activated):
   ```powershell
   venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Your `.env` file should already contain your Gemini API key
   - Verify it looks like this:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

### 3. Running the Application

Run the Streamlit app:
```powershell
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

1. **Start a Story**:
   - Enter your story idea in the text area (minimum 10 characters)
   - Click "🚀 Start Story"
   - Wait for AI to generate the opening scene

2. **Make Choices**:
   - Read the current scene
   - Click one of the two choice buttons
   - Watch as the story unfolds based on your decision

3. **Track Progress**:
   - View story statistics in the sidebar
   - See your journey path (choices made)
   - Review story history

4. **Start New Story**:
   - Click "🔄 Start New Story" in the sidebar anytime

## Configuration

Edit `.env` file to customize:

```env
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-2.0-flash-exp      # Latest Gemini 2.0 model
TEMPERATURE=0.85                      # Creativity (0.0-1.0)
MAX_TOKENS=800                        # Max response length
MAX_STORY_LENGTH=20                   # Max number of scenes
CONTEXT_SCENES=3                      # Scenes to include in context
```

## Architecture Highlights

### Modular Design
- **Models**: Clean data structures with Pydantic validation
- **Services**: Separated business logic and API integration
- **Components**: Reusable UI components
- **Utils**: Helper functions and utilities

### Key Features
- **Error Handling**: Robust retry logic for API calls
- **Session Management**: Persistent state across interactions
- **Responsive UI**: Clean, intuitive interface
- **Context Management**: Smart context passing to AI

## Troubleshooting

### API Key Issues
- Ensure `GEMINI_API_KEY` is set correctly in `.env`
- Verify the key is valid at [Google AI Studio](https://ai.google.dev/)

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're in the correct virtual environment

### Story Generation Fails
- Check your internet connection
- Verify API key has quota remaining
- Check error messages in the UI

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI**: Google Gemini API (gemini-2.0-flash-exp)
- **Data Validation**: Pydantic
- **Environment**: python-dotenv

## Future Enhancements

- [ ] Save/load stories to database
- [ ] Story themes and genres
- [ ] Character consistency tracking
- [ ] Image generation for scenes
- [ ] Export stories (PDF, EPUB)
- [ ] Story branching visualization
- [ ] Multi-user collaboration

## License

This project is for educational purposes.

## Credits

Built with ❤️ using:
- [Streamlit](https://streamlit.io/)
- [Google Gemini AI](https://ai.google.dev/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
