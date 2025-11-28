"""
Session manager for Streamlit state management.

Handles persistence of story data across user interactions.
"""

import streamlit as st
from typing import Optional
from models.story import Story


class SessionManager:
    """Manages Streamlit session state for the story application."""
    
    # Session state keys
    STORY_KEY = "current_story"
    INITIALIZED_KEY = "session_initialized"
    LOADING_KEY = "is_loading"
    ERROR_KEY = "error_message"
    SUCCESS_KEY = "success_message"
    
    @staticmethod
    def initialize() -> None:
        """Initialize session state with default values."""
        if SessionManager.INITIALIZED_KEY not in st.session_state:
            st.session_state[SessionManager.INITIALIZED_KEY] = True
            st.session_state[SessionManager.STORY_KEY] = None
            st.session_state[SessionManager.LOADING_KEY] = False
            st.session_state[SessionManager.ERROR_KEY] = None
            st.session_state[SessionManager.SUCCESS_KEY] = None
    
    @staticmethod
    def get_story() -> Optional[Story]:
        """
        Get the current story from session state.
        
        Returns:
            Optional[Story]: Current story or None
        """
        return st.session_state.get(SessionManager.STORY_KEY)
    
    @staticmethod
    def set_story(story: Optional[Story]) -> None:
        """
        Set the current story in session state.
        
        Args:
            story: Story to store
        """
        st.session_state[SessionManager.STORY_KEY] = story
    
    @staticmethod
    def has_story() -> bool:
        """
        Check if a story exists in session.
        
        Returns:
            bool: True if story exists
        """
        return SessionManager.get_story() is not None
    
    @staticmethod
    def clear_story() -> None:
        """Clear the current story from session."""
        st.session_state[SessionManager.STORY_KEY] = None
        SessionManager.clear_messages()
    
    @staticmethod
    def set_loading(is_loading: bool) -> None:
        """
        Set loading state.
        
        Args:
            is_loading: Loading state
        """
        st.session_state[SessionManager.LOADING_KEY] = is_loading
    
    @staticmethod
    def is_loading() -> bool:
        """
        Check if application is in loading state.
        
        Returns:
            bool: True if loading
        """
        return st.session_state.get(SessionManager.LOADING_KEY, False)
    
    @staticmethod
    def set_error(message: str) -> None:
        """
        Set error message.
        
        Args:
            message: Error message to display
        """
        st.session_state[SessionManager.ERROR_KEY] = message
        st.session_state[SessionManager.SUCCESS_KEY] = None
    
    @staticmethod
    def set_success(message: str) -> None:
        """
        Set success message.
        
        Args:
            message: Success message to display
        """
        st.session_state[SessionManager.SUCCESS_KEY] = message
        st.session_state[SessionManager.ERROR_KEY] = None
    
    @staticmethod
    def get_error() -> Optional[str]:
        """
        Get error message.
        
        Returns:
            Optional[str]: Error message or None
        """
        return st.session_state.get(SessionManager.ERROR_KEY)
    
    @staticmethod
    def get_success() -> Optional[str]:
        """
        Get success message.
        
        Returns:
            Optional[str]: Success message or None
        """
        return st.session_state.get(SessionManager.SUCCESS_KEY)
    
    @staticmethod
    def clear_messages() -> None:
        """Clear all messages (error and success)."""
        st.session_state[SessionManager.ERROR_KEY] = None
        st.session_state[SessionManager.SUCCESS_KEY] = None
    
    @staticmethod
    def reset_session() -> None:
        """Reset entire session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        SessionManager.initialize()
    
    @staticmethod
    def get_story_stats() -> dict:
        """
        Get statistics about the current story.
        
        Returns:
            dict: Story statistics
        """
        story = SessionManager.get_story()
        
        if not story:
            return {
                'exists': False,
                'scene_count': 0,
                'current_scene': None,
                'has_choices': False
            }
        
        current_scene = story.get_current_scene()
        
        return {
            'exists': True,
            'scene_count': story.get_scene_count(),
            'current_scene': current_scene.id if current_scene else None,
            'has_choices': len(current_scene.choices) > 0 if current_scene else False,
            'initial_prompt': story.initial_prompt
        }
