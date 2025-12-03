"""
Comic Page Prompt Builder.

Constructs detailed multi-panel comic page prompts for image generation.
Transforms scene content and panel breakdowns into structured prompts
that produce professional comic book pages.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class PanelDescription:
    """Represents a single panel in a comic page."""
    panel_number: int
    visual_description: str
    character_action: str
    dialogue: Optional[str] = None
    camera_angle: str = "medium shot"
    emotion: str = "neutral"


class ComicPagePromptBuilder:
    """
    Builds structured prompts for generating full comic pages with multiple panels.
    
    Transforms story scenes into detailed, structured prompts that guide
    image generation models to create cohesive multi-panel comic pages.
    """
    
    # Art style presets with detailed descriptions
    ART_STYLES: Dict[str, str] = {
        "western_comic": (
            "American comic book style with bold black outlines, dynamic poses, "
            "cel-shading, vibrant colors, dramatic shadows, and action-oriented composition. "
            "Similar to Marvel/DC comics with strong contrast and heroic proportions."
        ),
        "manga": (
            "Japanese manga style with expressive eyes, speed lines for motion, "
            "screentones for shading, dramatic expressions, and dynamic panel layouts. "
            "Black and white with gray tones, emotional depth, and cinematic framing."
        ),
        "cartoon": (
            "Animated cartoon style with bright cheerful colors, rounded shapes, "
            "exaggerated expressions, clean bold lines, and playful compositions. "
            "Fun and energetic like modern animated series."
        ),
        "graphic_novel": (
            "Graphic novel style with realistic proportions, moody atmospheric lighting, "
            "muted color palette, detailed backgrounds, and cinematic composition. "
            "Sophisticated and mature visual storytelling."
        ),
        "retro_comic": (
            "Vintage 1960s comic book style with halftone dots, primary colors, "
            "classic speech bubbles, nostalgic aesthetics, and bold simple shapes. "
            "Retro pop art feel with limited color palette."
        ),
        "watercolor": (
            "Poetic watercolor-ink style with fine ink outlines, soft bleeding washes, "
            "visible paper grain texture, muted greys and blues with vivid accents, "
            "expressive brushwork, and delicate artistic feel."
        )
    }
    
    # Panel layout templates
    LAYOUT_TEMPLATES: Dict[str, str] = {
        "2_panels": "two equal horizontal panels stacked vertically",
        "3_panels": "three panels - one large on top, two smaller below",
        "4_panels": "classic 2x2 grid layout with equal sized panels",
        "5_panels": "dynamic layout with one large hero panel and four smaller panels around it",
        "action": "dynamic angled panels with dramatic compositions",
        "cinematic": "wide letterbox panels like movie storyboards"
    }
    
    def __init__(self, art_style: str = "western_comic"):
        """
        Initialize the prompt builder.
        
        Args:
            art_style: Default art style for comic pages
        """
        self.art_style = art_style
    
    def build_comic_page_prompt(
        self,
        title: str,
        panels: List[PanelDescription],
        art_style: Optional[str] = None,
        aspect_ratio: str = "16:9",
        layout: str = "4_panels",
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        Build a complete structured prompt for a multi-panel comic page.
        
        Args:
            title: Page title or chapter heading
            panels: List of panel descriptions
            art_style: Art style override (uses default if None)
            aspect_ratio: Image aspect ratio
            layout: Panel layout template
            additional_instructions: Extra generation instructions
            
        Returns:
            str: Complete structured prompt for image generation
        """
        style = art_style or self.art_style
        style_desc = self.ART_STYLES.get(style, self.ART_STYLES["western_comic"])
        layout_desc = self.LAYOUT_TEMPLATES.get(layout, self.LAYOUT_TEMPLATES["4_panels"])
        
        num_panels = len(panels)
        
        prompt = f"""GENERATE A PROFESSIONAL MULTI-PANEL COMIC BOOK PAGE

PAGE TITLE: "{title}"

LAYOUT STRUCTURE:
- Total panels: {num_panels}
- Arrangement: {layout_desc}
- Clear black panel borders with white gutters between panels
- {aspect_ratio} overall page aspect ratio

ART STYLE (apply consistently to ALL panels):
{style_desc}

PANEL-BY-PANEL BREAKDOWN:
"""
        # Add each panel with detailed description
        for panel in panels:
            prompt += f"""
[PANEL {panel.panel_number}]
- Visual: {panel.visual_description}
- Action: {panel.character_action}
- Camera: {panel.camera_angle}
- Mood: {panel.emotion}
"""
            if panel.dialogue:
                prompt += f"- Speech bubble: \"{panel.dialogue}\"\n"
        
        prompt += f"""
CRITICAL REQUIREMENTS:
- SAME character designs across ALL {num_panels} panels (consistent face, hair, clothing, colors)
- Clear visual storytelling flow from panel 1 to panel {num_panels}
- Each panel is a distinct scene moment, not repeated
- Dynamic varied compositions (different angles, distances, poses)
- Professional comic book illustration quality
- Visible panel borders separating each panel
- Characters are expressive with clear emotions

RESTRICTIONS:
- NO random floating objects
- NO distorted anatomy unless stylized
- NO unclear action or confusing composition
"""
        
        if additional_instructions:
            prompt += f"\nADDITIONAL: {additional_instructions}"
        
        return prompt
    
    def _build_panel_prompt(self, panel: PanelDescription) -> str:
        """
        Build prompt text for a single panel.
        
        Args:
            panel: Panel description object
            
        Returns:
            str: Panel prompt text
        """
        prompt = f"Panel {panel.panel_number}: "
        prompt += f"{panel.visual_description} "
        prompt += f"The character(s) {panel.character_action}. "
        prompt += f"Camera angle: {panel.camera_angle}. "
        prompt += f"Mood/emotion: {panel.emotion}. "
        
        if panel.dialogue:
            prompt += f"Speech bubble says: \"{panel.dialogue}\". "
        
        return prompt
    
    def build_from_scene_and_panels(
        self,
        scene_title: str,
        scene_content: str,
        panel_breakdown: List[Dict[str, str]],
        art_style: Optional[str] = None,
        page_number: int = 1
    ) -> str:
        """
        Build comic page prompt from scene content and panel breakdown.
        
        This is the main method used in the story generation flow.
        
        Args:
            scene_title: Title for this page/scene
            scene_content: Original scene narrative (for context)
            panel_breakdown: List of panel dicts from Gemini
            art_style: Art style preference
            page_number: Page number in the story
            
        Returns:
            str: Complete comic page prompt
        """
        style = art_style or self.art_style
        style_desc = self.ART_STYLES.get(style, self.ART_STYLES["western_comic"])
        
        # Convert panel breakdown to PanelDescription objects
        panels = []
        for i, panel_data in enumerate(panel_breakdown, 1):
            panel = PanelDescription(
                panel_number=i,
                visual_description=panel_data.get("visual", ""),
                character_action=panel_data.get("action", ""),
                dialogue=panel_data.get("dialogue"),
                camera_angle=panel_data.get("camera", "medium shot"),
                emotion=panel_data.get("emotion", "engaged")
            )
            panels.append(panel)
        
        # Determine layout based on panel count
        panel_count = len(panels)
        if panel_count <= 2:
            layout = "2_panels"
        elif panel_count == 3:
            layout = "3_panels"
        elif panel_count == 4:
            layout = "4_panels"
        else:
            layout = "5_panels"
        
        layout_desc = self.LAYOUT_TEMPLATES.get(layout, self.LAYOUT_TEMPLATES["4_panels"])
        
        # Build a comprehensive prompt with scene context
        prompt = f"""GENERATE A PROFESSIONAL MULTI-PANEL COMIC BOOK PAGE

PAGE {page_number}: "{scene_title}"

STORY CONTEXT FOR THIS PAGE:
{scene_content[:500]}...

LAYOUT STRUCTURE:
- Total panels: {panel_count}
- Arrangement: {layout_desc}
- Clear black panel borders with white gutters between panels
- 16:9 landscape overall page aspect ratio

ART STYLE (consistent across ALL panels):
{style_desc}

SEQUENTIAL PANEL BREAKDOWN:
"""
        # Add each panel with detailed description
        for panel in panels:
            prompt += f"""
=== PANEL {panel.panel_number} ===
VISUAL SCENE: {panel.visual_description}
CHARACTER ACTION: {panel.character_action}
CAMERA ANGLE: {panel.camera_angle}
EMOTIONAL TONE: {panel.emotion}
"""
            if panel.dialogue:
                prompt += f"SPEECH BUBBLE TEXT: \"{panel.dialogue}\"\n"
        
        prompt += f"""
CRITICAL CONSISTENCY REQUIREMENTS:
1. IDENTICAL character designs in every panel (same face shape, hair color/style, outfit, body type)
2. Consistent environment/setting details throughout the page
3. Logical visual progression from panel 1 → panel {panel_count}
4. Each panel shows a DIFFERENT moment in the sequence (no duplicates)
5. Professional comic illustration quality with polished finish

COMPOSITION GUIDELINES:
- Vary camera distances (close-up, medium, wide) across panels for visual interest
- Use dynamic angles when action intensifies
- Ensure character expressions match the emotional tone
- Background details support the narrative

STRICT RESTRICTIONS:
- NO distorted or inconsistent anatomy
- NO random floating objects or elements
- NO unclear actions or confusing staging
- NO missing panel borders
- ALL panels must be clearly separated and distinct"""
        
        return prompt
    
    def build_simple_prompt(
        self,
        scene_content: str,
        art_style: Optional[str] = None,
        num_panels: int = 4
    ) -> str:
        """
        Build a simpler prompt when detailed panel breakdown is not available.
        
        Lets the image model decide panel content based on scene description.
        
        Args:
            scene_content: The scene narrative
            art_style: Art style preference
            num_panels: Number of panels to generate
            
        Returns:
            str: Comic page prompt
        """
        style = art_style or self.art_style
        style_desc = self.ART_STYLES.get(style, self.ART_STYLES["western_comic"])
        layout = self.LAYOUT_TEMPLATES.get(f"{num_panels}_panels", "4_panels")
        
        prompt = f"""GENERATE A {num_panels}-PANEL COMIC BOOK PAGE

SCENE TO ILLUSTRATE:
{scene_content}

LAYOUT STRUCTURE:
- Total panels: {num_panels}
- Arrangement: {layout}
- Clear black panel borders with white gutters
- 16:9 landscape overall page aspect ratio

ART STYLE:
{style_desc}

AUTOMATIC PANEL BREAKDOWN INSTRUCTIONS:
1. Read the scene and identify {num_panels} KEY SEQUENTIAL MOMENTS
2. Panel 1: Opening/setup moment of the scene
3. Panels 2-{num_panels-1}: Rising action and key developments
4. Panel {num_panels}: Climax or closing moment

CRITICAL REQUIREMENTS:
- IDENTICAL character designs across ALL {num_panels} panels
- Same character faces, hair, clothing, and proportions throughout
- Clear visual storytelling progression from start to finish
- Each panel captures a DISTINCT moment (no repetition)
- Dynamic varied compositions (different angles, distances)
- Professional comic book illustration quality

CHARACTER CONSISTENCY CHECKLIST:
✓ Face shape and features remain identical
✓ Hair color, style, and length consistent
✓ Outfit/clothing unchanged unless story dictates
✓ Body proportions and height relationships maintained
✓ Any unique features (scars, accessories) present in all panels

RESTRICTIONS:
- NO distorted anatomy or inconsistent character designs
- NO confusing compositions or unclear actions
- NO missing or broken panel borders
- ALL panels must be visually distinct and properly separated"""
        
        return prompt
    
    def build_cover_prompt(
        self,
        story_title: str,
        story_theme: str,
        main_characters: Optional[str] = None,
        art_style: Optional[str] = None
    ) -> str:
        """
        Build a prompt for generating a comic book cover.
        
        Args:
            story_title: Title of the comic/story
            story_theme: Brief theme or genre description
            main_characters: Description of main characters
            art_style: Art style preference
            
        Returns:
            str: Cover page prompt
        """
        style = art_style or self.art_style
        style_desc = self.ART_STYLES.get(style, self.ART_STYLES["western_comic"])
        
        prompt = f"""GENERATE A PROFESSIONAL COMIC BOOK COVER

COMIC TITLE: "{story_title}"
GENRE/THEME: {story_theme}

ART STYLE:
{style_desc}
"""
        
        if main_characters:
            prompt += f"""
FEATURED CHARACTERS:
{main_characters}
"""
        
        prompt += f"""
COVER COMPOSITION REQUIREMENTS:
- TITLE "{story_title}" prominently displayed at the TOP in bold stylized comic font
- Main character(s) in a DYNAMIC, eye-catching hero pose as the focal point
- Dramatic lighting with strong contrast (rim lighting, spotlights, or atmospheric glow)
- Background hints at the story's setting or theme
- Professional comic book cover quality with polished, print-ready finish
- 3:4 portrait aspect ratio (standard comic book cover proportions)

VISUAL IMPACT GOALS:
- The cover should IMMEDIATELY grab attention
- Convey the genre and tone of the story at a glance
- Make viewers curious and eager to read the comic
- Character pose should be powerful, dramatic, or intriguing
- Colors should pop and create strong visual hierarchy

TITLE STYLING:
- Large, bold, readable from a distance
- Style matches the genre (action = angular/bold, fantasy = ornate, horror = dripping/scratchy)
- Positioned at top with room for character art below
- May include subtle effects (shadows, outlines, gradients)

RESTRICTIONS:
- NO distorted anatomy or unclear character designs
- NO cluttered or confusing compositions
- NO watermarks, signatures, or modern UI elements
- Title must be clearly readable and properly integrated"""
        
        return prompt


# Convenience function
def get_comic_prompt_builder(art_style: str = "western_comic") -> ComicPagePromptBuilder:
    """Get a ComicPagePromptBuilder instance."""
    return ComicPagePromptBuilder(art_style=art_style)
