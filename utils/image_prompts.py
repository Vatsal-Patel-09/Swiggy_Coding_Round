"""
Comic art prompt templates for image generation.

Provides specialized prompts for different comic styles and scenes.
"""

from typing import Dict


class ComicPromptTemplates:
    """Templates for generating comic-style image prompts."""
    
    # Art style definitions
    STYLES: Dict[str, str] = {
        "western_comic": (
            "American comic book style, bold black outlines, dynamic action poses, "
            "cel-shading, vibrant saturated colors, dramatic shadows, "
            "Marvel/DC superhero comics aesthetic"
        ),
        "manga": (
            "Japanese manga style, expressive eyes, speed lines for motion, "
            "detailed backgrounds, emotional expressions, clean linework, "
            "black and white with gray tones"
        ),
        "cartoon": (
            "Animated cartoon style, bright cheerful colors, rounded shapes, "
            "exaggerated expressions, clean simple lines, Pixar/Disney inspired"
        ),
        "graphic_novel": (
            "Graphic novel art style, realistic proportions, moody atmosphere, "
            "detailed shading, cinematic composition, muted color palette"
        ),
        "retro_comic": (
            "Vintage 1960s comic book style, halftone dots, primary colors, "
            "classic superhero poses, nostalgic pop art aesthetic"
        )
    }
    
    @staticmethod
    def get_scene_prompt(scene_text: str, style: str = "western_comic") -> str:
        """
        Generate an image prompt from scene text.
        
        Args:
            scene_text: The story scene text
            style: Art style key
            
        Returns:
            str: Formatted image generation prompt
        """
        style_desc = ComicPromptTemplates.STYLES.get(style, ComicPromptTemplates.STYLES["western_comic"])
        
        return f"""Create a single comic book panel illustration:

SCENE TO ILLUSTRATE: {scene_text}

ART STYLE: {style_desc}

COMPOSITION REQUIREMENTS:
- Single panel, no panel borders or frames
- Cinematic wide-angle composition (16:9)
- Dynamic perspective and dramatic angles
- Focus on the key moment of the scene
- Rich environmental details
- Expressive character poses and faces
- Professional comic book quality artwork

MUST NOT INCLUDE:
- Any text, words, or letters
- Speech bubbles or thought bubbles
- Captions or narration boxes
- Watermarks or signatures
- Multiple panels or comic strips
- Real photographs or people

Generate a visually stunning comic panel that captures the essence of this scene."""
    
    @staticmethod
    def get_cover_prompt(story_title: str, story_theme: str, style: str = "western_comic") -> str:
        """
        Generate a prompt for comic book cover art.
        
        Args:
            story_title: Title of the comic
            story_theme: Brief theme/genre description
            style: Art style key
            
        Returns:
            str: Formatted cover image prompt
        """
        style_desc = ComicPromptTemplates.STYLES.get(style, ComicPromptTemplates.STYLES["western_comic"])
        
        return f"""Create a comic book cover illustration:

TITLE: {story_title}
THEME: {story_theme}

ART STYLE: {style_desc}

COVER REQUIREMENTS:
- Dramatic hero pose or action scene
- Eye-catching composition
- Bold and dynamic layout
- Professional comic book cover quality
- Vibrant, attention-grabbing colors
- Epic and heroic atmosphere

MUST NOT INCLUDE:
- Any text, titles, or logos
- Speech bubbles
- Real photographs

Create an epic comic book cover that would grab attention on a shelf."""
    
    @staticmethod
    def get_action_prompt(action_description: str, style: str = "western_comic") -> str:
        """
        Generate a prompt specifically for action scenes.
        
        Args:
            action_description: Description of the action
            style: Art style key
            
        Returns:
            str: Formatted action scene prompt
        """
        style_desc = ComicPromptTemplates.STYLES.get(style, ComicPromptTemplates.STYLES["western_comic"])
        
        return f"""Create a dynamic action comic panel:

ACTION: {action_description}

ART STYLE: {style_desc}

ACTION PANEL REQUIREMENTS:
- Explosive dynamic composition
- Motion lines and impact effects
- Dramatic perspective (low angle or dutch angle)
- Energy and movement in every element
- Intense lighting with strong contrasts
- Characters in mid-action poses

MUST NOT INCLUDE:
- Any text or sound effects
- Speech bubbles
- Watermarks

Create a high-impact action scene that jumps off the page!"""
    
    @staticmethod  
    def get_emotional_prompt(emotion: str, scene_text: str, style: str = "western_comic") -> str:
        """
        Generate a prompt for emotional/dramatic scenes.
        
        Args:
            emotion: Primary emotion (sad, happy, tense, etc.)
            scene_text: The scene description
            style: Art style key
            
        Returns:
            str: Formatted emotional scene prompt
        """
        emotion_lighting = {
            "sad": "soft blue shadows, melancholic atmosphere, rain or mist",
            "happy": "warm golden lighting, bright cheerful colors, sunny atmosphere",
            "tense": "harsh dramatic shadows, red/orange accents, claustrophobic framing",
            "mysterious": "deep shadows, fog, moonlight, cool blue-purple palette",
            "romantic": "soft pink/warm lighting, dreamy atmosphere, gentle glow",
            "angry": "intense red lighting, sharp angles, aggressive composition"
        }
        
        lighting = emotion_lighting.get(emotion.lower(), "dramatic cinematic lighting")
        style_desc = ComicPromptTemplates.STYLES.get(style, ComicPromptTemplates.STYLES["western_comic"])
        
        return f"""Create an emotionally impactful comic panel:

SCENE: {scene_text}
EMOTION: {emotion}

ART STYLE: {style_desc}

EMOTIONAL REQUIREMENTS:
- {lighting}
- Close-up or medium shot for emotional impact
- Expressive character faces and body language
- Atmospheric environment that reinforces the mood
- Color palette that matches the emotion

MUST NOT INCLUDE:
- Any text or captions
- Speech bubbles
- Watermarks

Create a panel that makes the viewer feel the emotion."""
    
    @staticmethod
    def enhance_prompt_for_consistency(
        base_prompt: str, 
        character_descriptions: list = None,
        setting_description: str = None
    ) -> str:
        """
        Enhance a prompt with character/setting consistency hints.
        
        Args:
            base_prompt: The base image prompt
            character_descriptions: List of character descriptions
            setting_description: Description of the setting
            
        Returns:
            str: Enhanced prompt with consistency hints
        """
        consistency_notes = []
        
        if character_descriptions:
            chars = "\n".join([f"- {char}" for char in character_descriptions])
            consistency_notes.append(f"CHARACTERS:\n{chars}")
        
        if setting_description:
            consistency_notes.append(f"SETTING: {setting_description}")
        
        if consistency_notes:
            consistency_section = "\n\n".join(consistency_notes)
            return f"{base_prompt}\n\nCONSISTENCY REFERENCE:\n{consistency_section}"
        
        return base_prompt
