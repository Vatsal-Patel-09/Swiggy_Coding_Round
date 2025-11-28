"""
Comic book models for managing comic pages and export.

Provides structures for organizing story scenes into a comic book format.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from models.story import Scene, Story


class ComicPanel(BaseModel):
    """Represents a single panel in the comic."""
    
    panel_id: int = Field(..., description="Unique panel identifier")
    scene_id: int = Field(..., description="Reference to the source scene")
    image_path: Optional[str] = Field(None, description="Path to panel image")
    caption: str = Field(..., description="Short narrative text for the panel")
    page_number: int = Field(..., description="Page this panel belongs to")
    position: str = Field("full", description="Panel position: full, top, bottom")
    
    class Config:
        json_schema_extra = {
            "example": {
                "panel_id": 1,
                "scene_id": 1,
                "image_path": "/images/panel_1.png",
                "caption": "The hero stands at the edge of destiny...",
                "page_number": 1,
                "position": "full"
            }
        }


class ComicPage(BaseModel):
    """Represents a single page in the comic book."""
    
    page_number: int = Field(..., description="Page number in sequence")
    panels: List[ComicPanel] = Field(default_factory=list, description="Panels on this page")
    is_cover: bool = Field(False, description="Whether this is the cover page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "page_number": 1,
                "panels": [],
                "is_cover": False
            }
        }
    
    def add_panel(self, panel: ComicPanel) -> None:
        """Add a panel to this page."""
        self.panels.append(panel)
    
    def get_panel_count(self) -> int:
        """Get the number of panels on this page."""
        return len(self.panels)


class ComicBook(BaseModel):
    """Manages the complete comic book structure."""
    
    title: str = Field("My Comic Story", description="Title of the comic book")
    pages: List[ComicPage] = Field(default_factory=list, description="All pages in order")
    cover_image: Optional[str] = Field(None, description="Cover image path")
    created_at: datetime = Field(default_factory=datetime.now)
    art_style: str = Field("western_comic", description="Art style used")
    
    # Source story reference
    initial_prompt: str = Field("", description="Original story prompt")
    total_scenes: int = Field(0, description="Total number of scenes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Hero's Journey",
                "pages": [],
                "art_style": "western_comic"
            }
        }
    
    def add_page(self, page: ComicPage) -> None:
        """Add a page to the comic book."""
        self.pages.append(page)
    
    def get_page_count(self) -> int:
        """Get total number of pages."""
        return len(self.pages)
    
    def get_total_panels(self) -> int:
        """Get total number of panels across all pages."""
        return sum(page.get_panel_count() for page in self.pages)
    
    def get_page(self, page_number: int) -> Optional[ComicPage]:
        """Get a specific page by number."""
        for page in self.pages:
            if page.page_number == page_number:
                return page
        return None
    
    def get_all_image_paths(self) -> List[str]:
        """Get all image paths in page order."""
        paths = []
        if self.cover_image:
            paths.append(self.cover_image)
        for page in sorted(self.pages, key=lambda p: p.page_number):
            for panel in page.panels:
                if panel.image_path:
                    paths.append(panel.image_path)
        return paths
    
    def to_tree_structure(self) -> Dict[str, Any]:
        """
        Convert comic to a tree structure for visualization.
        
        Returns:
            Dict representing the comic structure
        """
        tree = {
            "title": self.title,
            "cover": self.cover_image,
            "page_count": self.get_page_count(),
            "pages": []
        }
        
        for page in sorted(self.pages, key=lambda p: p.page_number):
            page_node = {
                "page_number": page.page_number,
                "is_cover": page.is_cover,
                "panels": [
                    {
                        "panel_id": panel.panel_id,
                        "caption": panel.caption[:50] + "..." if len(panel.caption) > 50 else panel.caption,
                        "has_image": panel.image_path is not None
                    }
                    for panel in page.panels
                ]
            }
            tree["pages"].append(page_node)
        
        return tree


def create_comic_from_story(story: Story, art_style: str = "western_comic") -> ComicBook:
    """
    Create a ComicBook structure from a Story.
    
    Args:
        story: The completed story
        art_style: Art style used for the comic
        
    Returns:
        ComicBook: Structured comic book
    """
    comic = ComicBook(
        title=f"Comic: {story.initial_prompt[:30]}...",
        art_style=art_style,
        initial_prompt=story.initial_prompt,
        total_scenes=story.get_scene_count()
    )
    
    # Create one page per scene (one full panel per page)
    for i, scene in enumerate(story.scenes):
        page = ComicPage(
            page_number=i + 1,
            is_cover=(i == 0)
        )
        
        panel = ComicPanel(
            panel_id=i + 1,
            scene_id=scene.id,
            image_path=scene.image_path,
            caption=scene.content,
            page_number=i + 1,
            position="full"
        )
        
        page.add_panel(panel)
        comic.add_page(page)
    
    return comic
