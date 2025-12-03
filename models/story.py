"""
Data models for the Interactive Story Generator.

This module defines the core data structures:
- Scene: Represents a single story scene with choices
- Story: Manages the complete story with all scenes
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Choice(BaseModel):
    """Represents a choice option for the user."""
    
    id: int = Field(..., description="Unique identifier for the choice")
    text: str = Field(..., min_length=10, description="The choice text displayed to user")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "Venture deeper into the mysterious forest"
            }
        }


class Scene(BaseModel):
    """Represents a single scene in the story with comic panel."""
    
    id: int = Field(..., description="Unique identifier for the scene")
    content: str = Field(..., min_length=20, description="The scene narrative text")
    choices: List[Choice] = Field(default_factory=list, max_length=2, description="Available choices (max 2)")
    selected_choice_id: Optional[int] = Field(None, description="ID of the choice user selected")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the scene was created")
    
    # Comic panel fields (Panel Mode - single image per scene)
    image_path: Optional[str] = Field(None, description="Path to generated comic panel image")
    image_prompt: Optional[str] = Field(None, description="Prompt used to generate the image")
    
    # Comic page fields (Page Mode - multi-panel comic page)
    panel_breakdown: Optional[List[dict]] = Field(None, description="Panel-by-panel breakdown for page mode")
    scene_title: Optional[str] = Field(None, description="Short title for the scene/page")
    is_page_mode: bool = Field(False, description="Whether this scene uses page mode (multi-panel)")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "You stand at the edge of a dark forest...",
                "choices": [
                    {"id": 1, "text": "Enter the forest"},
                    {"id": 2, "text": "Walk around the perimeter"}
                ],
                "selected_choice_id": None,
                "image_path": "/path/to/comic_panel.png",
                "image_prompt": "Comic panel of hero at forest edge...",
                "panel_breakdown": None,
                "scene_title": "The Dark Forest",
                "is_page_mode": False
            }
        }
    
    def select_choice(self, choice_id: int) -> bool:
        """
        Mark a choice as selected.
        
        Args:
            choice_id: The ID of the choice to select
            
        Returns:
            bool: True if selection was successful, False otherwise
        """
        if any(choice.id == choice_id for choice in self.choices):
            self.selected_choice_id = choice_id
            return True
        return False
    
    def get_selected_choice(self) -> Optional[Choice]:
        """
        Get the selected choice object.
        
        Returns:
            Optional[Choice]: The selected choice or None if no selection made
        """
        if self.selected_choice_id is None:
            return None
        return next((choice for choice in self.choices if choice.id == self.selected_choice_id), None)


class Story(BaseModel):
    """Manages the complete interactive story."""
    
    initial_prompt: str = Field(..., min_length=10, description="User's initial story prompt")
    scenes: List[Scene] = Field(default_factory=list, description="All scenes in the story")
    current_scene_index: int = Field(0, description="Index of the current scene")
    created_at: datetime = Field(default_factory=datetime.now, description="Story creation timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "initial_prompt": "A detective investigating a haunted mansion",
                "scenes": [],
                "current_scene_index": 0
            }
        }
    
    def add_scene(self, scene: Scene) -> None:
        """
        Add a new scene to the story.
        
        Args:
            scene: The Scene object to add
        """
        self.scenes.append(scene)
        self.current_scene_index = len(self.scenes) - 1
    
    def get_current_scene(self) -> Optional[Scene]:
        """
        Get the current active scene.
        
        Returns:
            Optional[Scene]: The current scene or None if no scenes exist
        """
        if not self.scenes or self.current_scene_index >= len(self.scenes):
            return None
        return self.scenes[self.current_scene_index]
    
    def get_scene_count(self) -> int:
        """
        Get the total number of scenes in the story.
        
        Returns:
            int: Number of scenes
        """
        return len(self.scenes)
    
    def get_story_context(self, max_scenes: int = 3) -> str:
        """
        Get recent story context for AI generation.
        
        Args:
            max_scenes: Maximum number of recent scenes to include
            
        Returns:
            str: Formatted story context
        """
        if not self.scenes:
            return f"Story Prompt: {self.initial_prompt}"
        
        # Get the last N scenes
        recent_scenes = self.scenes[-max_scenes:] if len(self.scenes) > max_scenes else self.scenes
        
        context_parts = [f"Story Prompt: {self.initial_prompt}\n\nStory so far:"]
        
        for i, scene in enumerate(recent_scenes, 1):
            context_parts.append(f"\nScene {scene.id}:")
            context_parts.append(scene.content)
            
            if scene.selected_choice_id is not None:
                selected = scene.get_selected_choice()
                if selected:
                    context_parts.append(f"[User chose: {selected.text}]")
        
        return "\n".join(context_parts)
    
    def can_continue(self) -> bool:
        """
        Check if the story can continue (current scene has a selected choice).
        
        Returns:
            bool: True if story can continue, False otherwise
        """
        current = self.get_current_scene()
        return current is not None and current.selected_choice_id is not None
    
    def get_story_path(self) -> List[str]:
        """
        Get the path of choices made throughout the story.
        
        Returns:
            List[str]: List of choice texts selected by the user
        """
        path = []
        for scene in self.scenes:
            if scene.selected_choice_id is not None:
                selected = scene.get_selected_choice()
                if selected:
                    path.append(selected.text)
        return path
