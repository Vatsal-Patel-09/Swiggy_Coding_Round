"""
Story display component.

Renders the current story scene with beautiful formatting.
"""

import streamlit as st
from models.story import Scene


def display_scene(scene: Scene, scene_number: int) -> None:
    """
    Display a story scene with formatted styling.
    
    Args:
        scene: The scene to display
        scene_number: The scene number for display
    """
    # Scene header
    st.markdown(f"### 📖 Scene {scene_number}")
    
    # Scene content with nice styling
    st.markdown(
        f"""
        <div style="
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #4CAF50;
            margin: 10px 0;
            line-height: 1.8;
            font-size: 17px;
            color: #2c3e50;
            font-weight: 400;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            {scene.content}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")


def display_compact_scene(scene: Scene, is_current: bool = False) -> None:
    """
    Display a compact version of a scene for history.
    
    Args:
        scene: The scene to display
        is_current: Whether this is the current scene
    """
    border_color = "#4CAF50" if is_current else "#9E9E9E"
    bg_color = "#E8F5E9" if is_current else "#000000"
    
    # Truncate content for compact display
    content_preview = scene.content[:150] + "..." if len(scene.content) > 150 else scene.content
    
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 12px;
            border-radius: 8px;
            border-left: 3px solid {border_color};
            margin: 8px 0;
            font-size: 14px;
            color: #1f1f1f;
        ">
            <strong>Scene {scene.id}</strong><br/>
            {content_preview}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Show selected choice if any
    if scene.selected_choice_id:
        selected = scene.get_selected_choice()
        if selected:
            st.markdown(
                f"<small>✓ <em>Chose: {selected.text}</em></small>",
                unsafe_allow_html=True
            )


def display_ending_scene(scene: Scene, scene_number: int) -> None:
    """
    Display the final scene of the story with special styling.
    
    Args:
        scene: The ending scene
        scene_number: The scene number
    """
    st.markdown(f"### 🎬 Final Scene - Scene {scene_number}")
    
    st.markdown(
        f"""
        <div style="
            background-color: #fffde7;
            padding: 25px;
            border-radius: 10px;
            border: 3px solid #FFD700;
            margin: 10px 0;
            line-height: 1.8;
            font-size: 17px;
            color: #2c3e50;
            font-weight: 400;
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
        ">
            {scene.content}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.success("🎉 The End! Thank you for experiencing this story.")
    st.markdown("---")
