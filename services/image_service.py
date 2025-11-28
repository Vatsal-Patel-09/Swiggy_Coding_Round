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
            "western_comic": "Marvel/DC comic book style, bold outlines, dynamic composition, cel-shading, vibrant colors",
            "manga": "Japanese manga style, expressive characters, speed lines, black and white with screentones",
            "cartoon": "Animated cartoon style, bright colors, exaggerated expressions, clean lines",
            "realistic": "Semi-realistic comic art, detailed shading, dramatic lighting"
        }
        
        style_desc = style_instructions.get(style, style_instructions["western_comic"])
        
        prompt = f"""Create a single comic book panel illustration:

SCENE: {scene_description}

ART STYLE: {style_desc}

REQUIREMENTS:
- Single panel composition, no borders or frames
- Dramatic and engaging perspective
- Professional comic book quality
- Rich colors and dynamic lighting
- NO text, speech bubbles, or captions
- NO watermarks or signatures
- 16:9 landscape aspect ratio
- High detail and clean linework"""
        
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
