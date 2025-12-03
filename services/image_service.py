"""
Image generation service for comic panels.

Uses Imagen 4.0 Ultra for primary generation with Pollinations.ai as fallback.
"""

import os
import base64
import urllib.parse
import requests
import time
from typing import Optional, Tuple
from pathlib import Path
from config.settings import settings

# Import the new Google GenAI SDK
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠ google-genai package not installed. Run: pip install google-genai")


class ImageService:
    """Service for generating comic-style images."""
    
    def __init__(self):
        """Initialize the image service."""
        self.client = None
        self.images_dir = Path(__file__).parent.parent / 'generated_images'
        self.images_dir.mkdir(exist_ok=True)
        self._initialize_imagen()
    
    def _initialize_imagen(self) -> None:
        """Initialize Imagen 4.0 Ultra for image generation."""
        if not GENAI_AVAILABLE:
            print("⚠ google-genai not available. Will use Pollinations fallback.")
            return
            
        try:
            self.client = genai.Client(api_key=settings.gemini_api_key)
            print("✓ Image service initialized with Imagen 4.0 Ultra")
        except Exception as e:
            print(f"⚠ Imagen init failed: {e}. Will use Pollinations fallback.")
    
    def generate_comic_panel(
        self, 
        scene_description: str,
        scene_id: int,
        style: str = "western_comic"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate a comic panel image for a scene.
        
        Args:
            scene_description: The scene text to visualize
            scene_id: Unique scene identifier
            style: Art style (western_comic, manga, etc.)
            
        Returns:
            Tuple[image_path, image_prompt]: Path to saved image and the prompt used
        """
        # Build the comic art prompt
        image_prompt = self._build_comic_prompt(scene_description, style)
        
        # Try Gemini first
        image_path = self._generate_with_gemini(image_prompt, scene_id)
        
        # Fallback to Pollinations if Gemini fails
        if not image_path:
            print("⚠ Gemini failed, trying Pollinations fallback...")
            image_path = self._generate_with_pollinations(image_prompt, scene_id)
        
        return image_path, image_prompt
    
    def _build_comic_prompt(self, scene_description: str, style: str) -> str:
        """
        Build a detailed prompt for comic-style image generation.
        
        Args:
            scene_description: The scene to visualize
            style: Art style preference
            
        Returns:
            str: Formatted prompt for image generation
        """
        style_instructions = {
            "western_comic": (
                "rendered in American comic book style with bold black ink outlines, "
                "dynamic action poses, cel-shading with vibrant saturated colors, "
                "dramatic shadows, and heroic proportions like Marvel or DC comics"
            ),
            "manga": (
                "rendered in Japanese manga style with expressive large eyes, "
                "speed lines for motion, screentone shading patterns, emotional expressions, "
                "black and white with gray tones, dynamic panel energy"
            ),
            "cartoon": (
                "rendered in modern animated cartoon style with bright cheerful colors, "
                "rounded friendly shapes, exaggerated fun expressions, clean bold outlines, "
                "playful and energetic like Pixar or Disney animation"
            ),
            "graphic_novel": (
                "rendered in graphic novel style with realistic proportions, "
                "moody atmospheric lighting, muted sophisticated color palette, "
                "detailed textured backgrounds, cinematic noir composition"
            ),
            "retro_comic": (
                "rendered in vintage 1960s comic book style with visible halftone dot patterns, "
                "limited primary color palette (red, blue, yellow), classic bold outlines, "
                "nostalgic silver age aesthetic with slightly faded colors"
            ),
            "watercolor": (
                "rendered in poetic watercolor-ink illustration style with fine delicate ink outlines, "
                "soft bleeding watercolor washes, visible paper grain texture, "
                "muted greys and blues with occasional vivid color accents, expressive brushwork"
            )
        }
        
        style_desc = style_instructions.get(style, style_instructions["western_comic"])
        
        # Extract key visual elements from the scene
        prompt = f"""Create a stunning single comic book panel illustration, {style_desc}.

SCENE TO ILLUSTRATE:
{scene_description}

VISUAL REQUIREMENTS:
- Capture the KEY DRAMATIC MOMENT from the scene
- Show clear character poses and expressions that convey emotion
- Use dynamic camera angle (low angle for power, high angle for vulnerability, dutch angle for tension)
- Include relevant environment/background details mentioned in the scene
- Dramatic lighting that enhances the mood (rim lighting, shadows, highlights)
- Professional comic book illustration quality with polished finish
- Characters should be the focal point with clear silhouettes

COMPOSITION:
- Single cohesive panel, NO borders or panel frames
- 16:9 landscape cinematic aspect ratio
- Rule of thirds composition for visual impact
- Depth with foreground, midground, background elements
- Leading lines drawing eye to the action

STRICT RESTRICTIONS:
- Absolutely NO text, words, letters, or writing of any kind
- NO speech bubbles or caption boxes
- NO watermarks, signatures, or logos
- NO UI elements or borders
- Characters should NOT be looking directly at camera unless scene requires it"""
        
        return prompt
    
    def _generate_with_gemini(self, prompt: str, scene_id: int) -> Optional[str]:
        """
        Generate image using Imagen 4.0 Ultra.
        
        Args:
            prompt: The image generation prompt
            scene_id: Scene identifier for filename
            
        Returns:
            Optional[str]: Path to saved image or None if failed
        """
        if not self.client:
            return None
        
        try:
            # Generate with Imagen 4.0 Ultra model
            response = self.client.models.generate_images(
                model="imagen-4.0-ultra-generate-001",
                prompt=prompt,
                config={
                    "number_of_images": 1,
                    "aspect_ratio": "16:9",
                    "safety_filter_level": "BLOCK_LOW_AND_ABOVE",
                }
            )
            
            # Check if response contains images
            if response.generated_images:
                for idx, generated_image in enumerate(response.generated_images):
                    # Get image data
                    image_data = generated_image.image.image_bytes
                    image_path = self.images_dir / f"scene_{scene_id}_{int(time.time())}.png"
                    
                    with open(image_path, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✓ Generated image with Imagen 4.0 Ultra: {image_path}")
                    return str(image_path)
            
            print("⚠ Imagen response did not contain images")
            return None
            
        except Exception as e:
            print(f"⚠ Imagen 4.0 image generation failed: {e}")
            return None
    
    def _generate_with_pollinations(self, prompt: str, scene_id: int) -> Optional[str]:
        """
        Generate image using Pollinations.ai (free fallback).
        
        Args:
            prompt: The image generation prompt
            scene_id: Scene identifier for filename
            
        Returns:
            Optional[str]: Path to saved image or None if failed
        """
        try:
            # Pollinations API endpoint - use simpler prompt encoding
            # Shorten prompt to avoid URL length issues
            short_prompt = prompt[:500] if len(prompt) > 500 else prompt
            encoded_prompt = urllib.parse.quote(short_prompt)
            
            # Updated Pollinations URL format
            url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=576&nologo=true&model=flux"
            
            print(f"⏳ Generating image with Pollinations...")
            
            # Download the image with headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=120, headers=headers)
            
            if response.status_code == 200 and len(response.content) > 1000:
                image_path = self.images_dir / f"scene_{scene_id}_{int(time.time())}.png"
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ Generated image with Pollinations: {image_path}")
                return str(image_path)
            else:
                print(f"⚠ Pollinations returned status: {response.status_code}")
                # Try alternative endpoint
                return self._generate_with_pollinations_alt(prompt, scene_id)
                
        except Exception as e:
            print(f"⚠ Pollinations image generation failed: {e}")
            return self._generate_with_pollinations_alt(prompt, scene_id)
    
    def _generate_with_pollinations_alt(self, prompt: str, scene_id: int) -> Optional[str]:
        """
        Alternative Pollinations endpoint fallback.
        """
        try:
            # Try the image.pollinations.ai endpoint
            short_prompt = prompt[:300] if len(prompt) > 300 else prompt
            encoded_prompt = urllib.parse.quote(short_prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            print(f"⏳ Trying alternative Pollinations endpoint...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=120, headers=headers, allow_redirects=True)
            
            if response.status_code == 200 and len(response.content) > 1000:
                image_path = self.images_dir / f"scene_{scene_id}_{int(time.time())}.png"
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ Generated image with Pollinations (alt): {image_path}")
                return str(image_path)
            else:
                print(f"⚠ All image generation methods failed")
                return None
                
        except Exception as e:
            print(f"⚠ Alternative Pollinations also failed: {e}")
            return None
    
    def get_image_as_base64(self, image_path: str) -> Optional[str]:
        """
        Convert an image file to base64 string for embedding.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Optional[str]: Base64 encoded image string
        """
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"⚠ Failed to encode image: {e}")
            return None
    
    def cleanup_old_images(self, keep_count: int = 50) -> None:
        """
        Clean up old generated images to save disk space.
        
        Args:
            keep_count: Number of recent images to keep
        """
        try:
            images = sorted(self.images_dir.glob("*.png"), key=os.path.getmtime, reverse=True)
            
            for old_image in images[keep_count:]:
                old_image.unlink()
                print(f"🗑️ Cleaned up: {old_image.name}")
                
        except Exception as e:
            print(f"⚠ Cleanup failed: {e}")
    
    def generate_comic_page(
        self, 
        scene_content: str,
        panel_breakdown: list[dict],
        scene_id: int,
        scene_title: str = "The Story Continues",
        style: str = "western_comic"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate a full comic page with multiple panels.
        
        This is the PAGE MODE - generates a complete comic page layout
        with multiple panels from a structured panel breakdown.
        
        Args:
            scene_content: The original scene narrative (for context)
            panel_breakdown: List of panel dicts with visual, action, camera, emotion, dialogue
            scene_id: Unique scene identifier
            scene_title: Title for the comic page
            style: Art style (western_comic, manga, etc.)
            
        Returns:
            Tuple[image_path, image_prompt]: Path to saved image and the prompt used
        """
        from utils.comic_prompt_builder import ComicPagePromptBuilder
        
        # Initialize the prompt builder
        builder = ComicPagePromptBuilder(art_style=style)
        
        # Build the structured comic page prompt
        image_prompt = builder.build_from_scene_and_panels(
            scene_title=scene_title,
            scene_content=scene_content,
            panel_breakdown=panel_breakdown,
            art_style=style,
            page_number=scene_id
        )
        
        print(f"📄 Generating comic page with {len(panel_breakdown)} panels...")
        
        # Try Imagen first (best for multi-panel comics)
        image_path = self._generate_with_gemini(image_prompt, scene_id)
        
        # Fallback to Pollinations if Gemini fails
        if not image_path:
            print("⚠ Imagen failed for page mode, trying Pollinations...")
            image_path = self._generate_with_pollinations(image_prompt, scene_id)
        
        return image_path, image_prompt
    
    def generate_simple_comic_page(
        self,
        scene_content: str,
        scene_id: int,
        num_panels: int = 4,
        style: str = "western_comic"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate a comic page with a simpler prompt (when panel breakdown unavailable).
        
        Uses a simplified prompt that lets the image model decide panel content.
        
        Args:
            scene_content: The scene narrative
            scene_id: Unique scene identifier
            num_panels: Number of panels to request
            style: Art style preference
            
        Returns:
            Tuple[image_path, image_prompt]: Path to saved image and the prompt used
        """
        from utils.comic_prompt_builder import ComicPagePromptBuilder
        
        builder = ComicPagePromptBuilder(art_style=style)
        image_prompt = builder.build_simple_prompt(
            scene_content=scene_content,
            art_style=style,
            num_panels=num_panels
        )
        
        print(f"📄 Generating simple {num_panels}-panel comic page...")
        
        # Try Imagen first
        image_path = self._generate_with_gemini(image_prompt, scene_id)
        
        if not image_path:
            print("⚠ Imagen failed, trying Pollinations...")
            image_path = self._generate_with_pollinations(image_prompt, scene_id)
        
        return image_path, image_prompt
    
    def generate_cover_page(
        self,
        story_title: str,
        story_theme: str,
        main_characters: Optional[str] = None,
        style: str = "western_comic"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate a comic book cover for the story.
        
        Args:
            story_title: Title of the comic/story
            story_theme: Brief theme or genre description
            main_characters: Description of main characters
            style: Art style preference
            
        Returns:
            Tuple[image_path, image_prompt]: Path to saved image and the prompt used
        """
        from utils.comic_prompt_builder import ComicPagePromptBuilder
        
        builder = ComicPagePromptBuilder(art_style=style)
        image_prompt = builder.build_cover_prompt(
            story_title=story_title,
            story_theme=story_theme,
            main_characters=main_characters,
            art_style=style
        )
        
        print(f"📕 Generating comic cover: {story_title}...")
        
        # Try Imagen first
        image_path = self._generate_with_gemini(image_prompt, 0)
        
        if not image_path:
            print("⚠ Imagen failed for cover, trying Pollinations...")
            image_path = self._generate_with_pollinations(image_prompt, 0)
        
        return image_path, image_prompt


# Global service instance
_image_service: Optional[ImageService] = None


def get_image_service() -> ImageService:
    """
    Get or create the global image service instance.
    
    Returns:
        ImageService: The global service instance
    """
    global _image_service
    
    if _image_service is None:
        _image_service = ImageService()
    
    return _image_service
