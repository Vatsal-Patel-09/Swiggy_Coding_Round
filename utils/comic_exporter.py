"""
Comic book PDF exporter.

Exports the comic story as a downloadable PDF file.
"""

import io
import re
from typing import Optional, List
from pathlib import Path
from datetime import datetime

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False
    print("⚠ fpdf2 not installed. PDF export will be limited.")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠ Pillow not installed. Image processing will be limited.")

from models.story import Story
from models.comic import ComicBook, create_comic_from_story


def sanitize_text_for_pdf(text: str) -> str:
    """
    Sanitize text to remove/replace Unicode characters not supported by Helvetica.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: Sanitized text safe for PDF
    """
    # Replace common Unicode characters with ASCII equivalents
    replacements = {
        '…': '...',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '–': '-',
        '—': '-',
        '•': '*',
        '→': '->',
        '←': '<-',
        '©': '(c)',
        '®': '(R)',
        '™': '(TM)',
        '°': ' degrees',
        '×': 'x',
        '÷': '/',
        '≈': '~',
        '≠': '!=',
        '≤': '<=',
        '≥': '>=',
        '±': '+/-',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        '₹': 'INR',
        '\u200b': '',  # Zero-width space
        '\u00a0': ' ',  # Non-breaking space
    }
    
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    
    # Remove any remaining non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    return text


class ComicPDFExporter:
    """Exports comic books to PDF format."""
    
    def __init__(self):
        """Initialize the PDF exporter."""
        self.page_width = 210  # A4 width in mm
        self.page_height = 297  # A4 height in mm
        self.margin = 10  # Page margin in mm
    
    def export_story_to_pdf(
        self, 
        story: Story, 
        title: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Export a story to PDF format.
        
        Args:
            story: The story to export
            title: Optional custom title
            
        Returns:
            bytes: PDF file content or None if export fails
        """
        if not FPDF_AVAILABLE:
            print("⚠ Cannot export PDF: fpdf2 not installed")
            return None
        
        try:
            # Create PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Set title
            comic_title = title or f"Comic: {story.initial_prompt[:40]}..."
            
            # Add cover page
            self._add_cover_page(pdf, comic_title, story)
            
            # Add each scene as a page
            for i, scene in enumerate(story.scenes):
                self._add_comic_page(pdf, scene, i + 1, len(story.scenes))
            
            # Add ending page
            self._add_end_page(pdf)
            
            # Output to bytes (convert bytearray to bytes for Streamlit compatibility)
            return bytes(pdf.output())
            
        except Exception as e:
            print(f"⚠ PDF export failed: {e}")
            return None
    
    def _add_cover_page(self, pdf: FPDF, title: str, story: Story) -> None:
        """Add cover page to PDF."""
        pdf.add_page()
        
        # Sanitize text
        title = sanitize_text_for_pdf(title)
        
        # Cover background
        pdf.set_fill_color(30, 30, 60)
        pdf.rect(0, 0, self.page_width, self.page_height, 'F')
        
        # Title
        pdf.set_font('Helvetica', 'B', 32)
        pdf.set_text_color(255, 215, 0)  # Gold
        pdf.set_y(80)
        pdf.cell(0, 20, title, align='C', ln=True)
        
        # Subtitle
        pdf.set_font('Helvetica', 'I', 14)
        pdf.set_text_color(200, 200, 200)
        pdf.cell(0, 10, "An Interactive Comic Story", align='C', ln=True)
        
        # Stats
        pdf.set_y(180)
        pdf.set_font('Helvetica', '', 12)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 8, f"Scenes: {story.get_scene_count()}", align='C', ln=True)
        pdf.cell(0, 8, f"Created: {datetime.now().strftime('%B %d, %Y')}", align='C', ln=True)
        
        # Initial prompt
        pdf.set_y(220)
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(120, 120, 120)
        prompt_text = sanitize_text_for_pdf(f"Story Prompt: {story.initial_prompt}")
        pdf.multi_cell(0, 6, prompt_text, align='C')
    
    def _add_comic_page(
        self, 
        pdf: FPDF, 
        scene, 
        page_num: int, 
        total_pages: int
    ) -> None:
        """Add a comic page with panel and text."""
        pdf.add_page()
        
        # White background
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(0, 0, self.page_width, self.page_height, 'F')
        
        # Page number header
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.set_y(5)
        pdf.cell(0, 5, f"Page {page_num} of {total_pages}", align='R')
        
        # Panel border
        panel_x = self.margin
        panel_y = 15
        panel_width = self.page_width - (2 * self.margin)
        panel_height = 160
        
        # Add image if available
        if scene.image_path and Path(scene.image_path).exists():
            try:
                pdf.image(
                    scene.image_path,
                    x=panel_x,
                    y=panel_y,
                    w=panel_width,
                    h=panel_height
                )
            except Exception as e:
                # If image fails, draw placeholder
                self._draw_placeholder_panel(pdf, panel_x, panel_y, panel_width, panel_height)
        else:
            self._draw_placeholder_panel(pdf, panel_x, panel_y, panel_width, panel_height)
        
        # Draw panel border
        pdf.set_draw_color(30, 30, 30)
        pdf.set_line_width(1)
        pdf.rect(panel_x, panel_y, panel_width, panel_height)
        
        # Text box
        text_y = panel_y + panel_height + 10
        pdf.set_fill_color(255, 255, 240)
        pdf.set_draw_color(50, 50, 50)
        pdf.rect(panel_x, text_y, panel_width, 80, 'DF')
        
        # Scene text
        pdf.set_xy(panel_x + 5, text_y + 5)
        pdf.set_font('Helvetica', '', 12)
        pdf.set_text_color(20, 20, 20)
        scene_text = sanitize_text_for_pdf(scene.content)
        pdf.multi_cell(panel_width - 10, 7, scene_text)
        
        # Show choice made (if any)
        if scene.selected_choice_id is not None:
            choice = scene.get_selected_choice()
            if choice:
                pdf.set_y(text_y + 65)
                pdf.set_font('Helvetica', 'I', 10)
                pdf.set_text_color(60, 60, 60)
                choice_text = sanitize_text_for_pdf(f"Choice: {choice.text}")
                pdf.cell(0, 5, choice_text, align='C')
    
    def _draw_placeholder_panel(
        self, 
        pdf: FPDF, 
        x: float, 
        y: float, 
        w: float, 
        h: float
    ) -> None:
        """Draw a placeholder when image is not available."""
        pdf.set_fill_color(240, 240, 245)
        pdf.rect(x, y, w, h, 'F')
        
        # Placeholder text
        pdf.set_font('Helvetica', 'I', 14)
        pdf.set_text_color(150, 150, 150)
        pdf.set_xy(x, y + h/2 - 5)
        pdf.cell(w, 10, "[Comic Panel Image]", align='C')
    
    def _add_end_page(self, pdf: FPDF) -> None:
        """Add THE END page."""
        pdf.add_page()
        
        # Dark background
        pdf.set_fill_color(30, 30, 60)
        pdf.rect(0, 0, self.page_width, self.page_height, 'F')
        
        # THE END text
        pdf.set_font('Helvetica', 'B', 48)
        pdf.set_text_color(255, 215, 0)
        pdf.set_y(120)
        pdf.cell(0, 30, "THE END", align='C', ln=True)
        
        # Thank you message
        pdf.set_font('Helvetica', 'I', 14)
        pdf.set_text_color(180, 180, 180)
        pdf.cell(0, 20, "Thank you for reading!", align='C', ln=True)
        
        # Generator credit
        pdf.set_y(250)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Created with Interactive Story Generator", align='C')


def export_story_pdf(story: Story, title: Optional[str] = None) -> Optional[bytes]:
    """
    Convenience function to export story to PDF.
    
    Args:
        story: The story to export
        title: Optional title
        
    Returns:
        bytes: PDF content or None
    """
    exporter = ComicPDFExporter()
    return exporter.export_story_to_pdf(story, title)


def get_pdf_download_name(story: Story) -> str:
    """Generate a filename for the PDF download."""
    # Clean the prompt for filename
    clean_prompt = "".join(c for c in story.initial_prompt[:30] if c.isalnum() or c == ' ')
    clean_prompt = clean_prompt.replace(' ', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    return f"comic_{clean_prompt}_{timestamp}.pdf"
