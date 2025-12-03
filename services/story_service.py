"""
Story service - Business logic for story generation and management.

Orchestrates the story creation process using Gemini API and image generation.
Supports both Panel Mode (single image per scene) and Page Mode (multi-panel comic pages).
"""

from typing import Tuple, Optional
from models.story import Story, Scene, Choice
from services.gemini_service import get_gemini_service
from services.image_service import get_image_service
from utils.prompt_templates import PromptTemplates, PromptFormatter
from utils.image_prompts import ComicPromptTemplates
from config.settings import settings


class StoryService:
    """Service for managing story generation and flow."""
    
    def __init__(
        self, 
        generate_images: bool = True, 
        art_style: str = "western_comic",
        page_mode: bool = False,
        num_panels: int = 4
    ):
        """
        Initialize the story service.
        
        Args:
            generate_images: Whether to generate images for scenes
            art_style: Art style for comic generation
            page_mode: If True, generates full comic pages with multiple panels.
                      If False (default), generates single panel per scene.
            num_panels: Number of panels per page in page mode (3-5)
        """
        self.gemini_service = get_gemini_service()
        self.image_service = get_image_service()
        self.prompt_templates = PromptTemplates()
        self.comic_prompts = ComicPromptTemplates()
        self.generate_images = generate_images
        self.art_style = art_style
        self.page_mode = page_mode
        self.num_panels = max(3, min(5, num_panels))  # Clamp between 3-5
    
    def start_new_story(self, initial_prompt: str) -> Story:
        """
        Start a new story from user's initial prompt.
        
        Args:
            initial_prompt: User's story idea
            
        Returns:
            Story: New story instance with first scene
            
        Raises:
            ValueError: If initial_prompt is invalid
            Exception: If scene generation fails
        """
        # Validate input
        if not initial_prompt or len(initial_prompt.strip()) < 10:
            raise ValueError("Story prompt must be at least 10 characters long")
        
        initial_prompt = initial_prompt.strip()
        
        # Create story object
        story = Story(initial_prompt=initial_prompt)
        
        # Generate first scene
        first_scene = self._generate_first_scene(initial_prompt)
        story.add_scene(first_scene)
        
        return story
    
    def _generate_first_scene(self, user_prompt: str) -> Scene:
        """
        Generate the first scene of the story.
        
        Args:
            user_prompt: User's initial story prompt
            
        Returns:
            Scene: Generated first scene with choices
        """
        # Generate scene content
        scene_prompt = self.prompt_templates.get_initial_scene_prompt(user_prompt)
        scene_content = self.gemini_service.generate_scene(scene_prompt, is_first_scene=True)
        
        # Clean the scene content
        scene_content = PromptFormatter.clean_scene_text(scene_content)
        
        # Generate choices for the scene
        choices_prompt = self.prompt_templates.get_choices_prompt(
            scene_content=scene_content,
            story_context=f"Initial prompt: {user_prompt}"
        )
        choice1_text, choice2_text = self.gemini_service.generate_choices(choices_prompt)
        
        # Create choice objects
        choices = [
            Choice(id=1, text=choice1_text),
            Choice(id=2, text=choice2_text)
        ]
        
        # Generate image based on mode
        image_path = None
        image_prompt = None
        panel_breakdown = None
        scene_title = None
        
        if self.generate_images:
            if self.page_mode:
                # PAGE MODE: Generate multi-panel comic page
                image_path, image_prompt, panel_breakdown, scene_title = self._generate_comic_page(
                    scene_content=scene_content,
                    scene_id=1
                )
            else:
                # PANEL MODE: Generate single comic panel
                image_path, image_prompt = self.image_service.generate_comic_panel(
                    scene_description=scene_content,
                    scene_id=1,
                    style=self.art_style
                )
        
        # Create and return scene
        scene = Scene(
            id=1,
            content=scene_content,
            choices=choices,
            image_path=image_path,
            image_prompt=image_prompt,
            panel_breakdown=panel_breakdown,
            scene_title=scene_title,
            is_page_mode=self.page_mode
        )
        
        return scene
    
    def _generate_comic_page(
        self, 
        scene_content: str, 
        scene_id: int
    ) -> Tuple[Optional[str], Optional[str], Optional[list], Optional[str]]:
        """
        Generate a full comic page with multiple panels (Page Mode).
        
        Args:
            scene_content: The scene narrative
            scene_id: Scene identifier
            
        Returns:
            Tuple of (image_path, image_prompt, panel_breakdown, scene_title)
        """
        try:
            # 1. Generate scene title
            scene_title = self.gemini_service.generate_scene_title(scene_content)
            print(f"📖 Scene title: {scene_title}")
            
            # 2. Generate panel breakdown
            panel_breakdown = self.gemini_service.generate_panel_breakdown(
                scene_content=scene_content,
                num_panels=self.num_panels
            )
            print(f"🎬 Generated {len(panel_breakdown)} panels")
            
            # 3. Generate the comic page image
            image_path, image_prompt = self.image_service.generate_comic_page(
                scene_content=scene_content,
                panel_breakdown=panel_breakdown,
                scene_id=scene_id,
                scene_title=scene_title,
                style=self.art_style
            )
            
            return image_path, image_prompt, panel_breakdown, scene_title
            
        except Exception as e:
            print(f"⚠ Page mode generation failed: {e}")
            print("⚠ Falling back to simple page mode...")
            
            # Fallback to simple page generation
            try:
                image_path, image_prompt = self.image_service.generate_simple_comic_page(
                    scene_content=scene_content,
                    scene_id=scene_id,
                    num_panels=self.num_panels,
                    style=self.art_style
                )
                return image_path, image_prompt, None, "The Story Continues"
            except Exception as e2:
                print(f"⚠ Simple page mode also failed: {e2}")
                return None, None, None, None
    
    def continue_story(self, story: Story, selected_choice_id: int) -> Scene:
        """
        Continue the story based on user's choice.
        
        Args:
            story: Current story instance
            selected_choice_id: ID of the choice user selected
            
        Returns:
            Scene: Next scene in the story
            
        Raises:
            ValueError: If choice selection is invalid
            Exception: If scene generation fails
        """
        # Get current scene and validate choice
        current_scene = story.get_current_scene()
        if not current_scene:
            raise ValueError("No current scene found")
        
        if not current_scene.select_choice(selected_choice_id):
            raise ValueError(f"Invalid choice ID: {selected_choice_id}")
        
        # Get selected choice text
        selected_choice = current_scene.get_selected_choice()
        if not selected_choice:
            raise ValueError("Could not retrieve selected choice")
        
        # Generate next scene
        next_scene = self._generate_next_scene(story, selected_choice.text)
        story.add_scene(next_scene)
        
        return next_scene
    
    def _generate_next_scene(self, story: Story, selected_choice_text: str) -> Scene:
        """
        Generate the next scene based on story context and choice.
        
        Args:
            story: Current story instance
            selected_choice_text: Text of the selected choice
            
        Returns:
            Scene: Generated next scene with choices and comic panel/page
        """
        # Get story context
        story_context = story.get_story_context(max_scenes=settings.context_scenes)
        scene_id = story.get_scene_count() + 1
        
        # Check if this should be a final scene
        is_ending = story.get_scene_count() >= settings.max_story_length - 1
        
        if is_ending:
            # Generate ending scene
            scene_prompt = self.prompt_templates.get_story_ending_prompt(
                story_context=story_context,
                selected_choice=selected_choice_text
            )
            scene_content = self.gemini_service.generate_scene(scene_prompt, is_first_scene=False)
            scene_content = PromptFormatter.clean_scene_text(scene_content)
            
            # Generate image based on mode
            image_path = None
            image_prompt = None
            panel_breakdown = None
            scene_title = None
            
            if self.generate_images:
                if self.page_mode:
                    image_path, image_prompt, panel_breakdown, scene_title = self._generate_comic_page(
                        scene_content=scene_content,
                        scene_id=scene_id
                    )
                else:
                    image_path, image_prompt = self.image_service.generate_comic_panel(
                        scene_description=scene_content,
                        scene_id=scene_id,
                        style=self.art_style
                    )
            
            # No choices for ending scene
            scene = Scene(
                id=scene_id,
                content=scene_content,
                choices=[],
                image_path=image_path,
                image_prompt=image_prompt,
                panel_breakdown=panel_breakdown,
                scene_title=scene_title or "The End",
                is_page_mode=self.page_mode
            )
        else:
            # Generate continuation scene
            scene_prompt = self.prompt_templates.get_continuation_prompt(
                story_context=story_context,
                selected_choice=selected_choice_text
            )
            scene_content = self.gemini_service.generate_scene(scene_prompt, is_first_scene=False)
            scene_content = PromptFormatter.clean_scene_text(scene_content)
            
            # Generate choices
            choices_prompt = self.prompt_templates.get_choices_prompt(
                scene_content=scene_content,
                story_context=story_context
            )
            choice1_text, choice2_text = self.gemini_service.generate_choices(choices_prompt)
            
            # Create choice objects
            choices = [
                Choice(id=1, text=choice1_text),
                Choice(id=2, text=choice2_text)
            ]
            
            # Generate image based on mode
            image_path = None
            image_prompt = None
            panel_breakdown = None
            scene_title = None
            
            if self.generate_images:
                if self.page_mode:
                    image_path, image_prompt, panel_breakdown, scene_title = self._generate_comic_page(
                        scene_content=scene_content,
                        scene_id=scene_id
                    )
                else:
                    image_path, image_prompt = self.image_service.generate_comic_panel(
                        scene_description=scene_content,
                        scene_id=scene_id,
                        style=self.art_style
                    )
            
            scene = Scene(
                id=scene_id,
                content=scene_content,
                choices=choices,
                image_path=image_path,
                image_prompt=image_prompt,
                panel_breakdown=panel_breakdown,
                scene_title=scene_title,
                is_page_mode=self.page_mode
            )
        
        return scene
    
    def validate_story_state(self, story: Story) -> Tuple[bool, str]:
        """
        Validate the current state of the story.
        
        Args:
            story: Story to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not story:
            return False, "Story object is None"
        
        if not story.scenes:
            return False, "Story has no scenes"
        
        current_scene = story.get_current_scene()
        if not current_scene:
            return False, "No current scene found"
        
        if not current_scene.content:
            return False, "Current scene has no content"
        
        return True, ""
    
    def get_story_summary(self, story: Story) -> dict:
        """
        Get a summary of the story state.
        
        Args:
            story: Story to summarize
            
        Returns:
            dict: Story summary information
        """
        current_scene = story.get_current_scene()
        
        return {
            'total_scenes': story.get_scene_count(),
            'current_scene_id': current_scene.id if current_scene else None,
            'has_choices': len(current_scene.choices) > 0 if current_scene else False,
            'can_continue': story.can_continue(),
            'is_ending': story.get_scene_count() >= settings.max_story_length,
            'story_path': story.get_story_path()
        }


# Global service instance
_story_service: Optional[StoryService] = None


def get_story_service() -> StoryService:
    """
    Get or create the global story service instance.
    
    Returns:
        StoryService: The global service instance
    """
    global _story_service
    
    if _story_service is None:
        _story_service = StoryService()
    
    return _story_service
