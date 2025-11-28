"""
Configuration management for the Interactive Story Generator.

Loads environment variables and provides application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        """Initialize settings and load environment variables."""
        # Load .env file
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        # Gemini API Configuration
        self.gemini_api_key: Optional[str] = os.getenv('GEMINI_API_KEY') or os.getenv('GENMINI_API_KEY')
        self.model_name: str = os.getenv('MODEL_NAME', 'gemini-2.0-flash-exp')
        
        # Generation Parameters
        self.temperature: float = float(os.getenv('TEMPERATURE', '0.85'))
        self.max_tokens: int = int(os.getenv('MAX_TOKENS', '800'))
        self.top_p: float = float(os.getenv('TOP_P', '0.95'))
        self.top_k: int = int(os.getenv('TOP_K', '40'))
        
        # Story Configuration
        self.max_story_length: int = int(os.getenv('MAX_STORY_LENGTH', '20'))
        self.context_scenes: int = int(os.getenv('CONTEXT_SCENES', '3'))
        self.num_choices: int = 2  # Always 2 choices as per requirements
        
        # UI Configuration
        self.app_title: str = "🎭 Interactive Story Generator"
        self.app_icon: str = "📖"
        
        # Validate required settings
        self._validate()
    
    def _validate(self) -> None:
        """Validate that required settings are present."""
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please add it to your .env file."
            )
    
    def get_generation_config(self) -> dict:
        """
        Get the generation configuration for Gemini API.
        
        Returns:
            dict: Generation configuration parameters
        """
        return {
            'temperature': self.temperature,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'max_output_tokens': self.max_tokens,
        }
    
    def __repr__(self) -> str:
        """String representation of settings (without exposing API key)."""
        return (
            f"Settings(model={self.model_name}, "
            f"temperature={self.temperature}, "
            f"max_tokens={self.max_tokens})"
        )


# Global settings instance
settings = Settings()
