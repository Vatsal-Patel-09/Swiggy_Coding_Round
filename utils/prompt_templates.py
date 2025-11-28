"""
Prompt templates for AI story generation.

Contains carefully crafted prompts for different generation tasks.
Third-person narrative style for immersive storytelling.
"""

from typing import Dict


class PromptTemplates:
    """Collection of prompt templates for story generation."""
    
    @staticmethod
    def get_initial_scene_prompt(user_prompt: str) -> str:
        """
        Generate prompt for creating the first scene.
        
        Args:
            user_prompt: User's initial story idea
            
        Returns:
            str: Formatted prompt for AI
        """
        return f"""You are a master storyteller crafting an engaging comic book narrative. Create a captivating opening scene.

Story Concept: {user_prompt}

NARRATIVE STYLE:
- Write in THIRD PERSON perspective (he/she/they, character names)
- The reader is an OBSERVER watching the story unfold, NOT a character in it
- Focus on what the CHARACTERS do, feel, and experience
- Create vivid, cinematic moments perfect for comic panels

STORYTELLING GUIDELINES:
1. Open with a hook that grabs attention immediately
2. Introduce the protagonist(s) through action or compelling situation
3. Set the atmosphere with sensory details (sights, sounds, mood)
4. Build intrigue - hint at conflict or mystery
5. End at a dramatic moment where the story could branch two ways
6. Keep it to 3-5 punchy sentences - every word counts!
7. Use present tense for immediacy ("She runs..." not "She ran...")

Write ONLY the scene narrative. No choices, no questions to reader, no meta-commentary.
Make it visual, dramatic, and impossible to look away from!"""
    
    @staticmethod
    def get_continuation_prompt(story_context: str, selected_choice: str) -> str:
        """
        Generate prompt for continuing the story based on a choice.
        
        Args:
            story_context: Previous story content
            selected_choice: The choice the user made
            
        Returns:
            str: Formatted prompt for AI
        """
        return f"""You are continuing an epic comic book narrative. The reader has chosen what happens next.

{story_context}

WHAT HAPPENS NEXT: "{selected_choice}"

NARRATIVE STYLE:
- Write in THIRD PERSON perspective (he/she/they, character names)
- The reader OBSERVES the story - they are NOT a character in it
- Show the consequences of the chosen direction unfolding
- Create vivid, cinematic moments perfect for comic panels

STORYTELLING GUIDELINES:
1. Seamlessly continue from the chosen direction
2. Show immediate consequences and new developments
3. Maintain character consistency and story logic
4. Raise the stakes or deepen the intrigue
5. Add a twist, revelation, or escalation to keep readers hooked
6. End at another dramatic branching point
7. Keep it to 3-5 impactful sentences
8. Use present tense ("He discovers..." not "He discovered...")

Write ONLY the scene narrative. No choices, no questions, no meta-commentary.
Make every panel count - drama, emotion, action!"""
    
    @staticmethod
    def get_choices_prompt(scene_content: str, story_context: str) -> str:
        """
        Generate prompt for creating 2 distinct choices.
        
        Args:
            scene_content: The current scene text
            story_context: Previous story for context
            
        Returns:
            str: Formatted prompt for AI
        """
        return f"""You are creating story branches for a comic narrative. Generate 2 exciting directions the story could take.

Story So Far:
{story_context}

Current Scene:
{scene_content}

IMPORTANT - These are STORY DIRECTIONS, not reader actions:
- Describe what HAPPENS NEXT in the story (third person)
- Focus on plot developments, character actions, or events
- NOT "You decide to..." but rather "The hero chooses to..." or "Suddenly..."

GUIDELINES:
1. Create exactly 2 different story directions
2. Each should be 8-15 words describing what happens
3. Both paths should be genuinely interesting (no obvious good/bad)
4. They should lead to meaningfully different story outcomes
5. Make them dramatic, intriguing, or surprising
6. Use action verbs and vivid language

EXAMPLES OF GOOD CHOICES:
- "The detective follows the mysterious figure into the abandoned warehouse"
- "A sudden explosion rocks the building, trapping everyone inside"
- "She reveals her true identity to the shocked crowd"

Format your response EXACTLY as:
CHOICE_1: [what happens in direction 1]
CHOICE_2: [what happens in direction 2]

No other text or explanations."""
    
    @staticmethod
    def get_story_ending_prompt(story_context: str, selected_choice: str) -> str:
        """
        Generate prompt for a satisfying story conclusion.
        
        Args:
            story_context: All previous story content
            selected_choice: Final choice made by user
            
        Returns:
            str: Formatted prompt for AI
        """
        return f"""You are crafting the epic conclusion to a comic book narrative. Make it unforgettable.

{story_context}

FINAL DIRECTION: "{selected_choice}"

NARRATIVE STYLE:
- Write in THIRD PERSON perspective
- The reader observes the grand finale unfold
- Create a powerful, cinematic conclusion

STORYTELLING GUIDELINES:
1. Resolve the main conflict with emotional impact
2. Give the protagonist(s) a defining moment
3. Tie up story threads satisfyingly
4. Deliver an emotional payoff - triumph, sacrifice, revelation, or transformation
5. End with a memorable final image or moment
6. Keep it to 4-6 powerful sentences
7. Use present tense for immediacy

This is THE END - no cliffhangers, no new questions.
Write ONLY the finale. Make readers feel something!"""


class PromptFormatter:
    """Helper class for formatting prompts with context."""
    
    @staticmethod
    def format_story_context(scenes_data: list, initial_prompt: str) -> str:
        """
        Format story scenes into a coherent context string.
        
        Args:
            scenes_data: List of scene dictionaries with content and choices
            initial_prompt: Original user prompt
            
        Returns:
            str: Formatted context
        """
        context_parts = [f"Initial Prompt: {initial_prompt}\n"]
        
        for i, scene_data in enumerate(scenes_data, 1):
            context_parts.append(f"\nScene {i}:")
            context_parts.append(scene_data.get('content', ''))
            
            if scene_data.get('selected_choice'):
                context_parts.append(f"[User chose: {scene_data['selected_choice']}]")
        
        return "\n".join(context_parts)
    
    @staticmethod
    def extract_choices(ai_response: str) -> tuple[str, str]:
        """
        Extract two choices from AI response.
        
        Args:
            ai_response: Raw AI response containing choices
            
        Returns:
            tuple: (choice1_text, choice2_text)
            
        Raises:
            ValueError: If choices cannot be parsed
        """
        lines = [line.strip() for line in ai_response.strip().split('\n') if line.strip()]
        
        choice1 = None
        choice2 = None
        
        for line in lines:
            if line.startswith('CHOICE_1:'):
                choice1 = line.replace('CHOICE_1:', '').strip()
            elif line.startswith('CHOICE_2:'):
                choice2 = line.replace('CHOICE_2:', '').strip()
        
        if not choice1 or not choice2:
            raise ValueError(f"Could not extract both choices from response: {ai_response}")
        
        return choice1, choice2
    
    @staticmethod
    def clean_scene_text(scene_text: str) -> str:
        """
        Clean and format scene text.
        
        Args:
            scene_text: Raw scene text from AI
            
        Returns:
            str: Cleaned scene text
        """
        # Remove any markdown formatting
        scene_text = scene_text.replace('**', '').replace('*', '')
        
        # Remove any accidental choice text
        lines = scene_text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip lines that look like choices or meta-commentary
            if line.startswith('CHOICE') or line.startswith('Option') or line.startswith('['):
                continue
            if line.lower().startswith('what do you') or line.lower().startswith('what will you'):
                continue
            cleaned_lines.append(line)
        
        return '\n\n'.join(line for line in cleaned_lines if line).strip()
