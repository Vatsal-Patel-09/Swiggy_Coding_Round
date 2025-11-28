"""
Prompt templates for AI story generation.

Contains carefully crafted prompts for different generation tasks.
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
        return f"""You are a creative storytelling AI. Create an engaging opening scene for an interactive story.

User's Story Prompt: {user_prompt}

Instructions:
1. Write a brief, engaging opening scene (3-5 sentences max)
2. Set the atmosphere and introduce the situation concisely
3. End at a decision point where the reader must make a choice
4. Make it vivid but concise
5. Use present tense for immediacy
6. Don't include any choices in the scene text itself

Write ONLY the scene narrative in 3-5 sentences. Do not include choices, options, or meta-commentary."""
    
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
        return f"""You are continuing an interactive story. Write the next scene based on the user's choice.

{story_context}

The user chose: "{selected_choice}"

Instructions:
1. Write the next scene (3-5 sentences max) that follows naturally from the choice
2. Show the consequences and developments from the decision
3. Maintain consistency with previous events
4. End at another decision point
5. Use vivid, descriptive language but keep it concise
6. Keep the tension and engagement high
7. Use present tense

Write ONLY the scene narrative in 3-5 sentences. Do not include choices, options, or meta-commentary."""
    
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
        return f"""You are creating choices for an interactive story. Generate exactly 2 distinct, interesting options.

Story Context:
{story_context}

Current Scene:
{scene_content}

Instructions:
1. Create exactly 2 different choices
2. Each choice should be 8-15 words
3. Make choices meaningful and lead to different outcomes
4. Choices should be action-oriented
5. Make both options interesting (avoid obvious good/bad choices)
6. Choices should feel natural to the situation

Format your response EXACTLY as:
CHOICE_1: [first choice text here]
CHOICE_2: [second choice text here]

Do not add any other text, explanations, or formatting."""
    
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
        return f"""You are concluding an interactive story. Write a satisfying ending scene.

{story_context}

The user's final choice: "{selected_choice}"

Instructions:
1. Write a conclusive scene (4-6 sentences max)
2. Resolve the main story threads
3. Provide a satisfying emotional payoff
4. Reference key moments from the journey briefly
5. Use vivid, impactful language but keep it concise
6. Make it memorable
7. Use present tense

This is the final scene - do not end with a cliffhanger or new choices.
Write ONLY the ending scene narrative in 4-6 sentences."""


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
