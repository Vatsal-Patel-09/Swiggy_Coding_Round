# Interactive Story Generator - Project Plan

## Overview
A Streamlit-based web application that generates interactive stories using Google's Gemini API. Users provide an initial story prompt, and the AI generates story scenes with branching narrative choices.

## Core Features

### 1. Story Initialization
- User inputs an initial story prompt (text)
- AI generates the first scene based on the prompt
- Scene is displayed to the user

### 2. Branching Narrative
- For each scene, AI generates 2 different continuation options
- User selects their preferred option
- Selected option becomes the next scene
- Process repeats recursively, building the story

### 3. Story Management
- Track story history (all scenes and choices)
- Display current scene prominently
- Show story progression/breadcrumb trail
- Option to restart or save story

## Technical Architecture

### Project Structure
```
swiggy/
├── .env                          # Environment variables (Gemini API key)
├── app.py                        # Main Streamlit application entry point
├── requirements.txt              # Python dependencies
├── config/
│   └── settings.py              # Configuration management
├── models/
│   └── story.py                 # Story data models (Scene, Story classes)
├── services/
│   ├── gemini_service.py        # Gemini API integration
│   └── story_service.py         # Story generation logic
├── utils/
│   ├── prompt_templates.py      # AI prompt templates
│   └── session_manager.py       # Session state management
└── components/
    ├── story_display.py         # UI component for story display
    ├── choice_selector.py       # UI component for choice selection
    └── story_history.py         # UI component for story history
```

## Technology Stack

### Frontend
- **Streamlit**: Web UI framework
- Responsive layout with columns
- Session state for story persistence

### Backend
- **Python 3.8+**: Core language
- **google-generativeai**: Gemini API client
- **python-dotenv**: Environment variable management

### AI Integration
- **Gemini API** (google-generativeai)
- Model: gemini-1.5-flash or gemini-1.5-pro
- Temperature: 0.8-0.9 for creative outputs

## Module Breakdown

### 1. `app.py` (Main Application)
- Initialize Streamlit app
- Manage page layout and navigation
- Orchestrate components
- Handle user interactions

### 2. `models/story.py` (Data Models)
**Classes:**
- `Scene`: Represents a single story scene
  - `id`: Unique identifier
  - `content`: Scene text
  - `choices`: List of available choices
  - `selected_choice`: User's selection
  
- `Story`: Manages the entire story
  - `scenes`: List of Scene objects
  - `current_scene_index`: Track position
  - `initial_prompt`: User's starting prompt
  - Methods: `add_scene()`, `get_current_scene()`, `get_history()`

### 3. `services/gemini_service.py` (AI Service)
**Class: `GeminiService`**
- `initialize()`: Setup Gemini client
- `generate_scene(prompt, context)`: Generate story scene
- `generate_choices(scene_content, story_context)`: Generate 2 branching options
- Error handling and retry logic

### 4. `services/story_service.py` (Business Logic)
**Class: `StoryService`**
- `start_new_story(initial_prompt)`: Initialize story
- `generate_next_scene(story, choice)`: Continue story based on choice
- `get_formatted_context(story)`: Prepare context for AI
- Story validation and consistency checks

### 5. `utils/prompt_templates.py` (Prompt Engineering)
- `INITIAL_SCENE_TEMPLATE`: Template for first scene generation
- `CONTINUATION_TEMPLATE`: Template for scene continuations
- `CHOICE_GENERATION_TEMPLATE`: Template for creating 2 choices
- Context formatting helpers

### 6. `utils/session_manager.py` (State Management)
- Initialize and manage Streamlit session state
- Persist story data across interactions
- Handle resets and new stories

### 7. `components/` (UI Components)
- **`story_display.py`**: Render current scene with styling
- **`choice_selector.py`**: Display and handle choice selection
- **`story_history.py`**: Show story progression timeline

### 8. `config/settings.py` (Configuration)
- Load environment variables
- API configuration
- App settings (max story length, model parameters)

## User Flow

1. **Landing Page**
   - Welcome message
   - Text input for initial story prompt
   - "Start Story" button

2. **Story Generation**
   - Display loading spinner
   - Generate first scene
   - Show scene content

3. **Choice Selection**
   - Display 2 AI-generated choices
   - User clicks preferred option
   - Generate next scene

4. **Story Progression**
   - Update story history
   - Display new scene
   - Generate new choices
   - Repeat until user stops

5. **Story Management**
   - Sidebar: Story history/timeline
   - Option to restart
   - (Optional) Download/save story

## API Integration Details

### Gemini API Setup
```python
# .env file
GEMINI_API_KEY=your_api_key_here
```

### Prompt Strategy
- **Scene Generation**: Include full story context for coherence
- **Choice Generation**: Create distinct, interesting branching paths
- **Temperature**: Higher for creativity (0.8-0.9)
- **Max Tokens**: ~500-800 per scene

## Development Phases

### Phase 1: Core Setup ✓
- [ ] Project structure
- [ ] Environment setup
- [ ] Dependencies installation
- [ ] Basic Streamlit app

### Phase 2: Data Models
- [ ] Scene class implementation
- [ ] Story class implementation
- [ ] Unit tests

### Phase 3: AI Integration
- [ ] Gemini service setup
- [ ] Prompt templates
- [ ] Scene generation
- [ ] Choice generation

### Phase 4: Business Logic
- [ ] Story service implementation
- [ ] Context management
- [ ] Story flow control

### Phase 5: UI Components
- [ ] Story display component
- [ ] Choice selector component
- [ ] Story history component

### Phase 6: Main Application
- [ ] Integrate all components
- [ ] Session state management
- [ ] Error handling
- [ ] User experience polish

### Phase 7: Testing & Refinement
- [ ] End-to-end testing
- [ ] Prompt optimization
- [ ] UI/UX improvements
- [ ] Documentation

## Key Dependencies

```txt
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pydantic>=2.0.0  # For data validation
```

## Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.8
MAX_TOKENS=800
```

## Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Scalability**: Easy to add features (save stories, themes, etc.)
3. **Testability**: Clear interfaces between modules
4. **Maintainability**: Well-documented code with type hints
5. **User Experience**: Smooth interactions, clear feedback

## Future Enhancements (Post-MVP)

- Story themes/genres selection
- Character consistency tracking
- Image generation for scenes (Imagen API)
- Story export (PDF, EPUB)
- Multi-user story collaboration
- Story branching visualization
- Save/load functionality with database
- User authentication

## Success Metrics

- Story generation time < 5 seconds per scene
- Coherent narrative across scenes
- Distinct and meaningful choices
- Smooth user experience
- Error-free API interactions

---

## Next Steps

Once this plan is approved, I will:
1. Create the project structure with all directories
2. Set up `requirements.txt` and `.env` template
3. Implement data models (`models/story.py`)
4. Build Gemini service (`services/gemini_service.py`)
5. Create prompt templates (`utils/prompt_templates.py`)
6. Implement story service (`services/story_service.py`)
7. Build UI components (`components/`)
8. Create main Streamlit app (`app.py`)
9. Test and refine

**Please review this plan and let me know if you'd like any modifications before I proceed with implementation!**
