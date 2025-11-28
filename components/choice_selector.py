"""
Choice selector component.

Handles user choice selection with interactive buttons.
"""

import streamlit as st
from typing import Optional, Callable
from models.story import Choice, Scene


def display_choices(
    scene: Scene,
    on_choice_selected: Optional[Callable[[int], None]] = None,
    disabled: bool = False
) -> Optional[int]:
    """
    Display choice buttons for user selection.
    
    Args:
        scene: The scene containing choices
        on_choice_selected: Callback function when choice is selected
        disabled: Whether choices should be disabled
        
    Returns:
        Optional[int]: Selected choice ID or None
    """
    if not scene.choices:
        return None
    
    # Create two columns for the two choices
    col1, col2 = st.columns(2)
    
    selected_choice_id = None
    
    with col1:
        choice1 = scene.choices[0]
        # Custom styled button container
        st.markdown(f"""
        <div style="
            background: linear-gradient(180deg, #4caf50 0%, #388e3c 100%);
            border: 4px solid #000;
            border-radius: 10px;
            padding: 5px;
            box-shadow: 5px 5px 0px #000;
            text-align: center;
            margin-bottom: 10px;
        ">
            <span style="
                font-family: 'Bangers', cursive;
                color: #fff;
                font-size: 0.9rem;
                text-shadow: 1px 1px 0px #000;
            ">OPTION A</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            f"👈 {choice1.text}",
            key=f"choice_1_{scene.id}",
            disabled=disabled,
            width="stretch",
            type="primary"
        ):
            selected_choice_id = choice1.id
            if on_choice_selected:
                on_choice_selected(choice1.id)
    
    with col2:
        if len(scene.choices) > 1:
            choice2 = scene.choices[1]
            st.markdown(f"""
            <div style="
                background: linear-gradient(180deg, #2196f3 0%, #1976d2 100%);
                border: 4px solid #000;
                border-radius: 10px;
                padding: 5px;
                box-shadow: 5px 5px 0px #000;
                text-align: center;
                margin-bottom: 10px;
            ">
                <span style="
                    font-family: 'Bangers', cursive;
                    color: #fff;
                    font-size: 0.9rem;
                    text-shadow: 1px 1px 0px #000;
                ">OPTION B</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(
                f"👉 {choice2.text}",
                key=f"choice_2_{scene.id}",
                disabled=disabled,
                width="stretch",
                type="secondary"
            ):
                selected_choice_id = choice2.id
                if on_choice_selected:
                    on_choice_selected(choice2.id)
    
    return selected_choice_id


def display_selected_choice(choice: Choice) -> None:
    """
    Display the choice that was selected.
    
    Args:
        choice: The selected choice
    """
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #c8e6c9 0%, #a5d6a7 100%);
            padding: 15px 20px;
            border-radius: 10px;
            border: 4px solid #000;
            margin: 15px 0;
            font-family: 'Bangers', cursive;
            font-size: 1.1rem;
            box-shadow: 4px 4px 0px #000;
        ">
            ✓ YOU CHOSE: {choice.text}
        </div>
        """,
        unsafe_allow_html=True
    )


def display_choice_prompt(custom_text: Optional[str] = None) -> None:
    """
    Display a prompt encouraging the user to make a choice.
    
    Args:
        custom_text: Optional custom prompt text
    """
    prompt = custom_text or "Choose your path to continue the adventure..."
    
    st.markdown(f"""
    <div style="
        background: #fff;
        border: 3px solid #000;
        border-radius: 50px;
        padding: 10px 25px;
        margin: 15px auto;
        max-width: 400px;
        text-align: center;
        box-shadow: 4px 4px 0px #000;
    ">
        <span style="
            font-family: 'Comic Neue', cursive;
            font-size: 1rem;
            color: #333;
        ">💭 {prompt}</span>
    </div>
    """, unsafe_allow_html=True)
