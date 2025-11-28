"""
Interactive Comic Story Generator - Main Streamlit Application

A web application that creates interactive comic book stories using AI.
Users provide an initial prompt, AI generates scenes with comic panels and branching choices.
"""

import streamlit as st
from typing import Optional

# Import project modules
from config.settings import settings
from models.story import Story
from services.story_service import get_story_service
from utils.session_manager import SessionManager
from components.story_display import display_scene, display_ending_scene
from components.comic_display import display_comic_panel, display_comic_panel_ending, display_loading_panel
from components.choice_selector import display_choices, display_choice_prompt
from components.story_history import display_story_history, display_stats_sidebar
from utils.comic_exporter import export_story_pdf, get_pdf_download_name


# Page configuration
st.set_page_config(
    page_title="Interactive Comic Generator",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inject_comic_theme() -> None:
    """Inject comic book themed CSS styling."""
    st.markdown("""
    <style>
    /* ========================================
       COMIC BOOK THEME - Main Styles
       ======================================== */
    
    /* Import Comic Font */
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');
    
    /* Hide Streamlit Branding but keep menu functional */
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Style the hamburger menu button - comic theme */
    #MainMenu {
        visibility: visible !important;
    }
    
    button[data-testid="stMainMenuButton"],
    #MainMenu button {
        background: #ffeb3b !important;
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 3px 3px 0px #000 !important;
        color: #000 !important;
    }
    
    button[data-testid="stMainMenuButton"]:hover,
    #MainMenu button:hover {
        background: #fdd835 !important;
        transform: translate(1px, 1px);
        box-shadow: 2px 2px 0px #000 !important;
    }
    
    button[data-testid="stMainMenuButton"] svg,
    #MainMenu svg {
        fill: #000 !important;
        stroke: #000 !important;
    }
    
    /* Style the header/navbar - comic theme */
    header[data-testid="stHeader"] {
        background: linear-gradient(90deg, #d32f2f 0%, #f44336 50%, #d32f2f 100%) !important;
        border-bottom: 4px solid #000 !important;
        box-shadow: 0 4px 0px #000 !important;
    }
    
    /* Sidebar toggle button - always visible */
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="baseButton-headerNoPadding"] {
        background: #ffeb3b !important;
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 3px 3px 0px #000 !important;
        color: #000 !important;
    }
    
    button[data-testid="stSidebarCollapseButton"]:hover,
    button[data-testid="baseButton-headerNoPadding"]:hover {
        background: #fdd835 !important;
        transform: translate(1px, 1px);
        box-shadow: 2px 2px 0px #000 !important;
    }
    
    button[data-testid="stSidebarCollapseButton"] svg,
    button[data-testid="baseButton-headerNoPadding"] svg {
        fill: #000 !important;
        stroke: #000 !important;
    }
    
    /* When sidebar is collapsed - show expand button prominently */
    [data-testid="stSidebar"][aria-expanded="false"] ~ section button[kind="header"] {
        background: #ffeb3b !important;
        border: 3px solid #000 !important;
    }
    
    /* Main Background with Halftone Pattern */
    .stApp {
        background: 
            radial-gradient(circle, rgba(255,193,7,0.1) 1px, transparent 1px),
            linear-gradient(135deg, #fff9c4 0%, #ffecb3 25%, #ffe082 50%, #ffca28 75%, #ffc107 100%);
        background-size: 8px 8px, 100% 100%;
    }
    
    /* Main Container - responsive width */
    .main .block-container {
        padding-top: 2rem;
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Make main content area responsive */
    .main {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    section.main > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* ========================================
       SIDEBAR - Fixed Width & Styling
       ======================================== */
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #42a5f5 0%, #1976d2 100%) !important;
        border-right: 5px solid #000 !important;
        min-width: 300px !important;
        max-width: 300px !important;
        width: 300px !important;
        overflow-x: hidden !important;
        transition: all 0.3s ease !important;
    }
    
    /* When sidebar is collapsed */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 0 !important;
        max-width: 0 !important;
        width: 0 !important;
        border-right: none !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        overflow-x: hidden !important;
        width: 100% !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        overflow-x: hidden !important;
    }
    
    /* Sidebar collapse/expand button inside sidebar */
    section[data-testid="stSidebar"] button[data-testid="stSidebarCollapseButton"] {
        background: #ffeb3b !important;
        border: 3px solid #000 !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar text - white for labels but allow overrides */
    section[data-testid="stSidebar"] > div > div > div > p,
    section[data-testid="stSidebar"] > div > div > div > label {
        color: #ffffff !important;
        font-family: 'Comic Neue', sans-serif !important;
    }
    
    /* Don't override colors inside custom HTML divs */
    section[data-testid="stSidebar"] div[style] p,
    section[data-testid="stSidebar"] div[style] span {
        /* Allow inline styles to work */
    }
    
    /* Sidebar expander fix */
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(255,255,255,0.2) !important;
        border: 2px solid #fff !important;
        border-radius: 8px !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderHeader p,
    section[data-testid="stSidebar"] .streamlit-expanderHeader svg {
        color: #fff !important;
        fill: #fff !important;
        font-weight: bold !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderContent {
        background: #ffffff !important;
        border: 2px solid #000 !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderContent p {
        color: #1a1a1a !important;
    }
    
    /* ========================================
       TYPOGRAPHY
       ======================================== */
    
    h1, h2, h3 {
        font-family: 'Bangers', cursive !important;
        letter-spacing: 2px;
    }
    
    .main h1, .main h2, .main h3 {
        text-shadow: 3px 3px 0px #000, -1px -1px 0px #000;
        color: #d32f2f !important;
    }
    
    h1 {
        font-size: 3.5rem !important;
        text-align: center;
    }
    
    .main p, .main li, .main span, .main label {
        font-family: 'Comic Neue', cursive !important;
        font-size: 1.1rem;
        color: #1a1a1a;
    }
    
    /* ========================================
       BUTTONS - Comic Style
       ======================================== */
    
    .stButton > button {
        font-family: 'Bangers', cursive !important;
        font-size: 1.3rem !important;
        letter-spacing: 1px;
        padding: 15px 30px !important;
        border: 4px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 5px 5px 0px #000 !important;
        transition: all 0.1s ease !important;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translate(2px, 2px) !important;
        box-shadow: 3px 3px 0px #000 !important;
    }
    
    .stButton > button:active {
        transform: translate(4px, 4px) !important;
        box-shadow: 1px 1px 0px #000 !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #ff5252 0%, #d32f2f 100%) !important;
        color: #fff !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(180deg, #42a5f5 0%, #1976d2 100%) !important;
        color: #fff !important;
    }
    
    /* ========================================
       TEXT INPUT - Comic Style
       ======================================== */
    
    .stTextArea textarea {
        font-family: 'Comic Neue', cursive !important;
        font-size: 1.1rem !important;
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 4px 4px 0px #000 !important;
        background: #fffef0 !important;
        color: #1a1a1a !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #d32f2f !important;
        box-shadow: 4px 4px 0px #d32f2f !important;
    }
    
    /* ========================================
       ALERTS & MESSAGES
       ======================================== */
    
    .stAlert {
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 4px 4px 0px #000 !important;
        font-family: 'Comic Neue', cursive !important;
    }
    
    /* ========================================
       SELECTBOX - Fix text visibility & cursor
       ======================================== */
    
    .stSelectbox > div > div {
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 3px 3px 0px #000 !important;
        background: #fff !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        transform: translate(1px, 1px) !important;
        box-shadow: 2px 2px 0px #000 !important;
        background: #fffef0 !important;
    }
    
    /* Make dropdown text dark/visible with pointer cursor */
    .stSelectbox [data-baseweb="select"] {
        background: #fff !important;
        cursor: pointer !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: #fff !important;
        color: #1a1a1a !important;
        cursor: pointer !important;
    }
    
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div[data-baseweb="select-value-container"] {
        color: #1a1a1a !important;
        cursor: pointer !important;
    }
    
    /* Dropdown arrow with pointer */
    .stSelectbox svg {
        fill: #1a1a1a !important;
        cursor: pointer !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="popover"] [data-baseweb="menu"] {
        background: #fff !important;
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 4px 4px 0px #000 !important;
    }
    
    [data-baseweb="popover"] li {
        color: #1a1a1a !important;
        background: #fff !important;
        cursor: pointer !important;
        font-family: 'Comic Neue', sans-serif !important;
    }
    
    [data-baseweb="popover"] li:hover {
        background: #fff9c4 !important;
    }
    
    .stSelectbox label {
        color: #fff !important;
    }
    
    /* ========================================
       CHECKBOX
       ======================================== */
    
    .stCheckbox label span {
        color: #fff !important;
    }
    
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #fff !important;
    }
    
    /* ========================================
       DIVIDERS
       ======================================== */
    
    hr {
        border: none;
        height: 4px;
        background: 
            repeating-linear-gradient(
                90deg,
                #000 0px,
                #000 10px,
                #ffeb3b 10px,
                #ffeb3b 20px
            );
        margin: 30px 0;
    }
    
    /* ========================================
       DOWNLOAD BUTTON
       ======================================== */
    
    .stDownloadButton > button {
        font-family: 'Bangers', cursive !important;
        border: 3px solid #000 !important;
        border-radius: 8px !important;
        box-shadow: 4px 4px 0px #000 !important;
        background: linear-gradient(180deg, #4caf50 0%, #388e3c 100%) !important;
        color: #fff !important;
    }
    
    </style>
    """, unsafe_allow_html=True)


def initialize_app() -> None:
    """Initialize the application and session state."""
    SessionManager.initialize()
    # Initialize comic mode setting
    if 'comic_mode' not in st.session_state:
        st.session_state.comic_mode = True
    if 'art_style' not in st.session_state:
        st.session_state.art_style = "western_comic"


def display_welcome_screen() -> None:
    """Display the welcome screen for new users."""
    # Comic-style header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="
            font-family: 'Bangers', cursive;
            font-size: 4rem;
            color: #d32f2f;
            text-shadow: 4px 4px 0px #ffeb3b, 7px 7px 0px #000;
            letter-spacing: 3px;
            margin-bottom: 10px;
        ">💥 COMIC STORY GENERATOR 💥</h1>
        <p style="
            font-family: 'Comic Neue', cursive;
            font-size: 1.3rem;
            color: #1a1a1a;
        ">Create Your Own Interactive Comic Adventure!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # How it works in comic panels
    st.markdown("""
    <div style="
        background: #fff;
        border: 4px solid #000;
        border-radius: 10px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 8px 8px 0px #000;
    ">
        <h3 style="
            font-family: 'Bangers', cursive;
            color: #1976d2;
            text-shadow: 2px 2px 0px #000;
            margin-bottom: 15px;
        ">⚡ HOW IT WORKS ⚡</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">
            <div style="
                background: #ffeb3b;
                border: 3px solid #000;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 4px 4px 0px #000;
            ">
                <span style="font-size: 2rem;">📝</span>
                <span style="font-family: 'Bangers', cursive; font-size: 0.9rem;">WRITE</span>
            </div>
            <div style="
                background: #ff5252;
                border: 3px solid #000;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 4px 4px 0px #000;
            ">
                <span style="font-size: 2rem;">🎨</span>
                <span style="font-family: 'Bangers', cursive; font-size: 0.9rem; color: #fff;">CREATE</span>
            </div>
            <div style="
                background: #4caf50;
                border: 3px solid #000;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 4px 4px 0px #000;
            ">
                <span style="font-size: 2rem;">🔀</span>
                <span style="font-family: 'Bangers', cursive; font-size: 0.9rem; color: #fff;">CHOOSE</span>
            </div>
            <div style="
                background: #42a5f5;
                border: 3px solid #000;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 4px 4px 0px #000;
            ">
                <span style="font-size: 2rem;">📥</span>
                <span style="font-family: 'Bangers', cursive; font-size: 0.9rem; color: #fff;">EXPORT</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_user_prompt() -> Optional[str]:
    """
    Get initial story prompt from user.
    
    Returns:
        Optional[str]: User's story prompt or None
    """
    st.markdown("""
    <div style="
        background: #fff;
        border: 4px solid #000;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 6px 6px 0px #000;
        position: relative;
    ">
        <div style="
            position: absolute;
            top: -15px;
            left: 20px;
            background: #ff5252;
            color: #fff;
            padding: 5px 15px;
            border: 3px solid #000;
            border-radius: 5px;
            font-family: 'Bangers', cursive;
            font-size: 1.2rem;
            box-shadow: 3px 3px 0px #000;
        ">📝 YOUR STORY IDEA</div>
    </div>
    """, unsafe_allow_html=True)
    
    prompt = st.text_area(
        "Describe your story idea:",
        placeholder="Example: A brave knight discovers a dragon who just wants to be friends...",
        height=100,
        max_chars=500,
        help="Provide a brief description of the story you want to create (minimum 10 characters)",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💥 START ADVENTURE!", type="primary", width="stretch"):
            if prompt and len(prompt.strip()) >= 10:
                return prompt.strip()
            else:
                st.error("⚠️ POW! Enter at least 10 characters!")
    
    return None


def handle_story_start(prompt: str) -> None:
    """
    Handle starting a new story.
    
    Args:
        prompt: User's initial story prompt
    """
    try:
        SessionManager.set_loading(True)
        SessionManager.clear_messages()
        
        # Get settings from session state
        comic_mode = st.session_state.get('comic_mode', True)
        art_style = st.session_state.get('art_style', 'western_comic')
        
        with st.spinner("💥 CREATING YOUR COMIC... KAPOW!"):
            from services.story_service import StoryService
            story_service = StoryService(
                generate_images=comic_mode,
                art_style=art_style
            )
            story = story_service.start_new_story(prompt)
            SessionManager.set_story(story)
            SessionManager.set_success("💥 BOOM! Your comic panel is ready!")
        
    except Exception as e:
        SessionManager.set_error(f"Failed to start story: {str(e)}")
    finally:
        SessionManager.set_loading(False)
        st.rerun()


def handle_choice_selection(choice_id: int) -> None:
    """
    Handle user's choice selection.
    
    Args:
        choice_id: ID of the selected choice
    """
    try:
        SessionManager.set_loading(True)
        SessionManager.clear_messages()
        
        story = SessionManager.get_story()
        if not story:
            SessionManager.set_error("No active story found.")
            return
        
        # Get settings from session state
        comic_mode = st.session_state.get('comic_mode', True)
        art_style = st.session_state.get('art_style', 'western_comic')
        
        with st.spinner("⚡ CREATING NEXT PANEL... ZAP!"):
            from services.story_service import StoryService
            story_service = StoryService(
                generate_images=comic_mode,
                art_style=art_style
            )
            next_scene = story_service.continue_story(story, choice_id)
            
            # Check if this is the ending
            if not next_scene.choices:
                SessionManager.set_success("🎬 THE END! Export your comic as PDF!")
            else:
                SessionManager.set_success("💥 WHAM! New panel created!")
        
    except Exception as e:
        SessionManager.set_error(f"Failed to continue story: {str(e)}")
    finally:
        SessionManager.set_loading(False)
        st.rerun()


def display_story_interface(story: Story) -> None:
    """
    Display the main story interface with comic panels.
    
    Args:
        story: Current story instance
    """
    current_scene = story.get_current_scene()
    
    if not current_scene:
        SessionManager.set_error("Unable to load current scene.")
        return
    
    # Check if comic mode is enabled
    comic_mode = st.session_state.get('comic_mode', True)
    
    # Display all scenes in the story (full history)
    for i, scene in enumerate(story.scenes):
        is_current = (i == story.current_scene_index)
        
        # Display scene as comic panel or text
        if not scene.choices:
            # This is an ending scene
            if comic_mode:
                display_comic_panel_ending(scene, scene.id)
            else:
                display_ending_scene(scene, scene.id)
        else:
            # Normal scene
            if comic_mode:
                display_comic_panel(scene, scene.id)
            else:
                display_scene(scene, scene.id)
            
            # Show selected choice if user has made one
            if scene.selected_choice_id is not None:
                selected_choice = scene.get_selected_choice()
                if selected_choice:
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(90deg, #c8e6c9 0%, #a5d6a7 100%);
                        border: 3px solid #000;
                        border-radius: 8px;
                        padding: 12px 20px;
                        margin: 10px 0;
                        box-shadow: 4px 4px 0px #000;
                        font-family: 'Bangers', cursive;
                        font-size: 1.1rem;
                    ">
                        ✓ YOU CHOSE: {selected_choice.text}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("---")
        
        # Only show choice buttons for the current scene if choice not yet made
        if is_current and scene.choices and scene.selected_choice_id is None:
            # Comic-style choice prompt
            st.markdown("""
            <div style="
                text-align: center;
                margin: 20px 0;
            ">
                <span style="
                    font-family: 'Bangers', cursive;
                    font-size: 2rem;
                    color: #d32f2f;
                    text-shadow: 2px 2px 0px #ffeb3b, 4px 4px 0px #000;
                    animation: pulse 1s ease-in-out infinite;
                ">⚡ WHAT DO YOU DO? ⚡</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Choice buttons with callback
            choice_id = display_choices(
                scene,
                disabled=SessionManager.is_loading()
            )
            
            if choice_id:
                handle_choice_selection(choice_id)


def display_sidebar_controls(story: Optional[Story]) -> None:
    """
    Display sidebar with controls and story info.
    
    Args:
        story: Current story or None
    """
    # Comic-style sidebar title
    st.sidebar.markdown("""
    <h2 style="
        font-family: 'Bangers', cursive;
        color: #fff;
        text-shadow: 3px 3px 0px #000;
        text-align: center;
        margin-bottom: 20px;
    ">COMIC CONTROLS</h2>
    """, unsafe_allow_html=True)
    
    if story:
        # Display story stats and history
        display_stats_sidebar(story)
        display_story_history(story)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <h3 style="
            font-family: 'Bangers', cursive;
            color: #ffeb3b;
            text-shadow: 2px 2px 0px #000;
        ">EXPORT COMIC</h3>
        """, unsafe_allow_html=True)
        
        # Export to PDF button
        if st.sidebar.button("DOWNLOAD PDF", width="stretch", type="primary"):
            with st.spinner("Generating PDF..."):
                pdf_bytes = export_story_pdf(story)
                if pdf_bytes:
                    st.sidebar.download_button(
                        label="SAVE PDF",
                        data=pdf_bytes,
                        file_name=get_pdf_download_name(story),
                        mime="application/pdf",
                        width="stretch"
                    )
                else:
                    st.sidebar.error("PDF export failed.")
        
        # Reset button
        st.sidebar.markdown("---")
        if st.sidebar.button("🆕 NEW STORY", use_container_width=True, type="secondary"):
            SessionManager.clear_story()
            st.rerun()
    else:
        # Art style and settings when no story is active
        _render_art_style_selector()
        
        st.sidebar.markdown("""
        <p style="
            background: rgba(255,255,255,0.2);
            padding: 10px;
            border-radius: 8px;
            color: #fff;
            font-family: 'Comic Neue', sans-serif;
            text-align: center;
            margin-top: 15px;
        ">Start a story to begin your adventure!</p>
        """, unsafe_allow_html=True)
    
    # About section - always shown at the bottom
    _render_about_section()


def _render_art_style_selector() -> None:
    """Render the art style selector with comic theme."""
    # Art style selector with comic label
    st.sidebar.markdown("""
    <p style="
        font-family: 'Bangers', cursive;
        color: #ffeb3b;
        text-shadow: 2px 2px 0px #000;
        font-size: 1.2rem;
        margin-bottom: 8px;
    ">🎨 ART STYLE</p>
    """, unsafe_allow_html=True)
    
    art_style = st.sidebar.selectbox(
        "Choose comic style:",
        options=["western_comic", "manga", "cartoon", "graphic_novel", "retro_comic"],
        format_func=lambda x: {
            "western_comic": "🦸 Marvel/DC Style",
            "manga": "🎌 Manga Style",
            "cartoon": "🎨 Cartoon Style",
            "graphic_novel": "📖 Graphic Novel",
            "retro_comic": "📰 Retro Comics"
        }.get(x, x),
        label_visibility="collapsed",
        key="art_style_select"
    )
    st.session_state.art_style = art_style
    
    # Show selected style preview
    style_info = {
        "western_comic": "Bold outlines, dynamic action, vibrant colors",
        "manga": "Japanese style, expressive characters, speed lines",
        "cartoon": "Bright colors, exaggerated expressions",
        "graphic_novel": "Realistic, moody atmosphere",
        "retro_comic": "Vintage 60s style, halftone dots"
    }
    
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.15);
        border: 2px dashed rgba(255,255,255,0.5);
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
    ">
        <p style="
            font-size: 0.85rem;
            color: #fff;
            font-family: 'Comic Neue', sans-serif;
            margin: 0;
            font-style: italic;
        ">💡 {style_info.get(art_style, '')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Comic mode toggle
    comic_mode = st.sidebar.checkbox(
        "🖼️ Enable Comic Panels",
        value=st.session_state.get('comic_mode', True),
        key="comic_mode_check",
        help="When enabled, each scene will have an AI-generated comic panel image"
    )
    st.session_state.comic_mode = comic_mode


def _render_about_section() -> None:
    """Render the About section with comic theme."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.15);
        border: 2px solid rgba(255,255,255,0.5);
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
    ">
        <h4 style="
            font-family: 'Bangers', cursive;
            color: #ffeb3b;
            margin-bottom: 8px;
            text-shadow: 1px 1px 0px #000;
        ">ℹ️ ABOUT</h4>
        <p style="font-size: 0.9rem; color: #fff; margin: 5px 0; font-family: 'Comic Neue', sans-serif;">
            🤖 Model: {settings.model_name}
        </p>
        <p style="font-size: 0.9rem; color: #fff; margin: 5px 0; font-family: 'Comic Neue', sans-serif;">
            📚 Max Scenes: {settings.max_story_length}
        </p>
        <p style="font-size: 0.9rem; color: #fff; margin: 5px 0; font-family: 'Comic Neue', sans-serif;">
            🖼️ Image: Imagen 4.0 Ultra
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_messages() -> None:
    """Display error and success messages."""
    error = SessionManager.get_error()
    if error:
        st.markdown(f"""
        <div style="
            background: #ffcdd2;
            border: 3px solid #000;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 4px 4px 0px #000;
            font-family: 'Bangers', cursive;
            color: #c62828;
        ">
            💢 {error}
        </div>
        """, unsafe_allow_html=True)
    
    success = SessionManager.get_success()
    if success:
        st.markdown(f"""
        <div style="
            background: #c8e6c9;
            border: 3px solid #000;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 4px 4px 0px #000;
            font-family: 'Bangers', cursive;
            color: #2e7d32;
        ">
            {success}
        </div>
        """, unsafe_allow_html=True)


def main() -> None:
    """Main application entry point."""
    # Inject comic theme CSS
    inject_comic_theme()
    
    # Initialize
    initialize_app()
    
    # Get current story
    story = SessionManager.get_story()
    
    # Display sidebar
    display_sidebar_controls(story)
    
    # Main content area
    if not story:
        # No active story - show welcome screen
        display_welcome_screen()
        
        prompt = get_user_prompt()
        if prompt:
            handle_story_start(prompt)
    else:
        # Active story - show story interface
        st.markdown("""
        <h1 style="
            font-family: 'Bangers', cursive;
            text-align: center;
            color: #d32f2f;
            text-shadow: 3px 3px 0px #ffeb3b, 6px 6px 0px #000;
            font-size: 3rem;
            margin-bottom: 20px;
        ">🎭 YOUR COMIC ADVENTURE 🎭</h1>
        """, unsafe_allow_html=True)
        
        # Display messages
        display_messages()
        
        # Display story
        display_story_interface(story)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.exception(e)
