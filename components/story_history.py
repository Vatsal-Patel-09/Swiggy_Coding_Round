"""
Story history component.

Displays the story's progression and path taken.
"""

import streamlit as st
from typing import List
from models.story import Story, Scene


def display_story_history(story: Story) -> None:
    """
    Display the complete story history in the sidebar.
    
    Args:
        story: The story to display history for
    """
    st.sidebar.markdown("""
    <h3 style="
        font-family: 'Bangers', cursive;
        color: #ffeb3b;
        text-shadow: 2px 2px 0px #000;
        margin-bottom: 10px;
    ">STORY PROGRESS</h3>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"""
    <p style="color: #fff; font-family: 'Comic Neue', sans-serif; font-size: 1rem;">
        <strong>Scenes:</strong> {story.get_scene_count()}
    </p>
    """, unsafe_allow_html=True)
    
    # Display initial prompt - simple text without emojis
    with st.sidebar.expander("Initial Prompt", expanded=False):
        st.markdown(f"<p style='color:#1a1a1a;'>{story.initial_prompt}</p>", unsafe_allow_html=True)
    
    # Display story path
    story_path = story.get_story_path()
    if story_path:
        with st.sidebar.expander("Your Journey", expanded=False):
            for i, choice_text in enumerate(story_path, 1):
                st.markdown(f"<p style='color:#1a1a1a;'>{i}. {choice_text}</p>", unsafe_allow_html=True)
    
    st.sidebar.markdown("---")


def display_scene_timeline(story: Story) -> None:
    """
    Display a timeline of all scenes.
    
    Args:
        story: The story to display timeline for
    """
    st.markdown("### Story Timeline")
    
    current_index = story.current_scene_index
    
    for i, scene in enumerate(story.scenes):
        is_current = i == current_index
        
        # Scene indicator
        status = " (Current)" if is_current else ""
        
        with st.expander(f"Scene {scene.id}{status}", expanded=is_current):
            st.write(scene.content)
            
            if scene.selected_choice_id:
                selected = scene.get_selected_choice()
                if selected:
                    st.success(f"Chose: {selected.text}")
            
            if is_current and scene.choices:
                st.info("Waiting for your decision...")


def display_stats_sidebar(story: Story) -> None:
    """
    Display story statistics in the sidebar.
    
    Args:
        story: The story to display stats for
    """
    st.sidebar.markdown("""
    <h3 style="
        font-family: 'Bangers', cursive;
        color: #ffeb3b;
        text-shadow: 2px 2px 0px #000;
        margin-bottom: 10px;
    ">STORY STATS</h3>
    """, unsafe_allow_html=True)
    
    stats_html = f"""
    <div style="
        background-color: #ffffff !important;
        padding: 15px;
        border-radius: 8px;
        border: 3px solid #000;
        margin: 10px 0;
        box-shadow: 4px 4px 0px #000;
    ">
        <p style="margin: 8px 0 !important; color: #1a1a1a !important; font-family: 'Comic Neue', sans-serif !important; font-size: 0.95rem !important;">
            <span style="color: #1a1a1a !important; font-weight: bold;">Total Scenes:</span> 
            <span style="color: #d32f2f !important; font-weight: bold;">{story.get_scene_count()}</span>
        </p>
        <p style="margin: 8px 0 !important; color: #1a1a1a !important; font-family: 'Comic Neue', sans-serif !important; font-size: 0.95rem !important;">
            <span style="color: #1a1a1a !important; font-weight: bold;">Choices Made:</span> 
            <span style="color: #1976d2 !important; font-weight: bold;">{len(story.get_story_path())}</span>
        </p>
        <p style="margin: 8px 0 !important; color: #1a1a1a !important; font-family: 'Comic Neue', sans-serif !important; font-size: 0.95rem !important;">
            <span style="color: #1a1a1a !important; font-weight: bold;">Current Scene:</span> 
            <span style="color: #388e3c !important; font-weight: bold;">{story.current_scene_index + 1}</span>
        </p>
    </div>
    """
    
    st.sidebar.markdown(stats_html, unsafe_allow_html=True)


def display_compact_history(story: Story, max_scenes: int = 5) -> None:
    """
    Display a compact history of recent scenes.
    
    Args:
        story: The story
        max_scenes: Maximum number of scenes to show
    """
    if not story.scenes:
        return
    
    st.markdown("### 📖 Recent Story")
    
    # Get recent scenes
    recent_scenes = story.scenes[-max_scenes:] if len(story.scenes) > max_scenes else story.scenes
    
    for scene in recent_scenes:
        is_current = scene.id == story.get_current_scene().id
        
        if is_current:
            st.markdown(f"**🔵 Scene {scene.id} (Current)**")
        else:
            st.markdown(f"⚪ Scene {scene.id}")
        
        # Truncate content
        content = scene.content[:100] + "..." if len(scene.content) > 100 else scene.content
        st.text(content)
        
        if scene.selected_choice_id:
            selected = scene.get_selected_choice()
            if selected:
                st.caption(f"✓ {selected.text}")
        
        st.markdown("")
