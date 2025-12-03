"""
Gemini API service for AI-powered story generation.

Handles all interactions with Google's Gemini API.
"""

import time
from typing import Optional, Tuple
import google.generativeai as genai
from config.settings import settings


class GeminiService:
    """Service for interacting with Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini service."""
        self.model = None
        self.is_initialized = False
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize the Gemini API client."""
        try:
            genai.configure(api_key=settings.gemini_api_key)
            
            self.model = genai.GenerativeModel(
                model_name=settings.model_name,
                generation_config=settings.get_generation_config()
            )
            
            self.is_initialized = True
            print(f"✓ Gemini service initialized with model: {settings.model_name}")
            
        except Exception as e:
            print(f"✗ Failed to initialize Gemini service: {str(e)}")
            raise
    
    def generate_text(
        self, 
        prompt: str, 
        max_retries: int = 3,
        retry_delay: float = 2.0
    ) -> str:
        """
        Generate text using Gemini API with retry logic.
        
        Args:
            prompt: The prompt to send to the API
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            str: Generated text from the API
            
        Raises:
            Exception: If generation fails after all retries
        """
        if not self.is_initialized:
            raise RuntimeError("Gemini service not initialized")
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                
                # Check if response has text
                if not response.text:
                    raise ValueError("Empty response from API")
                
                return response.text.strip()
                
            except Exception as e:
                last_error = e
                print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # Exponential backoff
        
        raise Exception(f"Failed to generate text after {max_retries} attempts: {str(last_error)}")
    
    def generate_scene(
        self, 
        prompt: str,
        is_first_scene: bool = False
    ) -> str:
        """
        Generate a story scene.
        
        Args:
            prompt: The formatted prompt for scene generation
            is_first_scene: Whether this is the first scene
            
        Returns:
            str: Generated scene text
        """
        try:
            scene_text = self.generate_text(prompt)
            
            # Basic validation
            if len(scene_text) < 50:
                raise ValueError(f"Generated scene too short: {len(scene_text)} characters")
            
            return scene_text
            
        except Exception as e:
            error_msg = f"Failed to generate scene: {str(e)}"
            print(f"✗ {error_msg}")
            raise Exception(error_msg)
    
    def generate_choices(self, prompt: str) -> Tuple[str, str]:
        """
        Generate two story choices.
        
        Args:
            prompt: The formatted prompt for choice generation
            
        Returns:
            Tuple[str, str]: Two choice texts
            
        Raises:
            Exception: If choices cannot be generated or parsed
        """
        try:
            response = self.generate_text(prompt)
            
            # Parse the choices from response
            from utils.prompt_templates import PromptFormatter
            choice1, choice2 = PromptFormatter.extract_choices(response)
            
            # Validate choices
            if len(choice1) < 8 or len(choice2) < 8:
                raise ValueError("Generated choices too short")
            
            if choice1.lower() == choice2.lower():
                raise ValueError("Generated choices are identical")
            
            return choice1, choice2
            
        except Exception as e:
            error_msg = f"Failed to generate choices: {str(e)}"
            print(f"✗ {error_msg}")
            raise Exception(error_msg)
    
    def generate_panel_breakdown(
        self, 
        scene_content: str, 
        num_panels: int = 4
    ) -> list[dict]:
        """
        Generate a panel-by-panel breakdown of a scene for comic visualization.
        
        Args:
            scene_content: The scene narrative to break down
            num_panels: Number of panels to create (3-5 recommended)
            
        Returns:
            list[dict]: List of panel descriptions with visual, action, camera, emotion, dialogue
            
        Raises:
            Exception: If panel breakdown cannot be generated or parsed
        """
        try:
            from utils.prompt_templates import PromptTemplates, PromptFormatter
            
            # Get the prompt for panel breakdown
            prompt = PromptTemplates.get_panel_breakdown_prompt(scene_content, num_panels)
            
            # Generate the breakdown
            response = self.generate_text(prompt)
            
            # Parse the panels
            panels = PromptFormatter.extract_panel_breakdown(response)
            
            # Validate we got reasonable panels
            if len(panels) < 2:
                raise ValueError(f"Expected {num_panels} panels, got {len(panels)}")
            
            print(f"✓ Generated {len(panels)} panel breakdown")
            return panels
            
        except Exception as e:
            error_msg = f"Failed to generate panel breakdown: {str(e)}"
            print(f"✗ {error_msg}")
            raise Exception(error_msg)
    
    def generate_scene_title(self, scene_content: str) -> str:
        """
        Generate a short catchy title for a scene.
        
        Args:
            scene_content: The scene narrative
            
        Returns:
            str: Short scene title
        """
        try:
            from utils.prompt_templates import PromptTemplates, PromptFormatter
            
            prompt = PromptTemplates.get_scene_title_prompt(scene_content)
            response = self.generate_text(prompt, max_retries=2)
            
            return PromptFormatter.extract_scene_title(response)
            
        except Exception as e:
            print(f"⚠ Could not generate scene title: {e}")
            return "The Story Continues"
    
    def health_check(self) -> bool:
        """
        Check if the Gemini service is working properly.
        
        Returns:
            bool: True if service is healthy, False otherwise
        """
        try:
            if not self.is_initialized:
                return False
            
            # Try a simple generation
            test_prompt = "Say 'OK' if you can read this."
            response = self.generate_text(test_prompt, max_retries=1)
            
            return len(response) > 0
            
        except Exception:
            return False
    
    def __repr__(self) -> str:
        """String representation of the service."""
        status = "initialized" if self.is_initialized else "not initialized"
        return f"GeminiService(model={settings.model_name}, status={status})"


# Global service instance
_gemini_service: Optional[GeminiService] = None


def get_gemini_service() -> GeminiService:
    """
    Get or create the global Gemini service instance.
    
    Returns:
        GeminiService: The global service instance
    """
    global _gemini_service
    
    if _gemini_service is None:
        _gemini_service = GeminiService()
    
    return _gemini_service
