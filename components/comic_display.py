"""
Comic display component.

Renders story scenes as comic book panels with images.
"""

import streamlit as st
import base64
from pathlib import Path
from typing import Optional
from models.story import Scene


def get_image_base64(image_path: str) -> Optional[str]:
    """Convert image file to base64 for embedding."""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        return None


def display_comic_panel(scene: Scene, scene_number: int) -> None:
    """
    Display a story scene as a comic book panel.
    
    Args:
        scene: The scene to display
        scene_number: The scene number
    """
    # Panel header with comic styling
    st.markdown(f"""
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, #ff5252 0%, #d32f2f 100%);
        color: #fff;
        padding: 8px 20px;
        border: 3px solid #000;
        border-radius: 5px;
        font-family: 'Bangers', cursive;
        font-size: 1.3rem;
        box-shadow: 3px 3px 0px #000;
        margin-bottom: 10px;
    ">📖 PANEL {scene_number}</div>
    """, unsafe_allow_html=True)
    
    # Display the comic panel image if available
    if scene.image_path and Path(scene.image_path).exists():
        # Create comic frame around image
        image_base64 = get_image_base64(scene.image_path)
        if image_base64:
            st.markdown(f"""
            <div style="
                border: 5px solid #000;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 8px 8px 0px #000;
                margin: 10px 0;
                position: relative;
            ">
                <img src="data:image/png;base64,{image_base64}" style="
                    width: 100%;
                    display: block;
                ">
                <!-- Halftone overlay -->
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: radial-gradient(circle, rgba(0,0,0,0.05) 1px, transparent 1px);
                    background-size: 4px 4px;
                    pointer-events: none;
                "></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.image(scene.image_path, width="stretch", caption=None)
    else:
        # Placeholder if no image - comic style
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 300px;
                border: 5px solid #000;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin: 10px 0;
                box-shadow: 8px 8px 0px #000;
                position: relative;
            ">
                <span style="
                    font-size: 48px;
                    animation: pulse 1.5s ease-in-out infinite;
                ">🎨</span>
                <span style="
                    color: white;
                    font-family: 'Bangers', cursive;
                    font-size: 1.5rem;
                    margin-top: 10px;
                    text-shadow: 2px 2px 0px #000;
                ">GENERATING ARTWORK...</span>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    # Display caption/narration box - speech bubble style with tail at BOTTOM
    st.markdown(
        f"""
        <div style="
            background: #ffffff;
            padding: 20px 25px;
            border-radius: 20px;
            border: 4px solid #000;
            margin: 15px 0 30px 0;
            font-size: 1.1rem;
            color: #1a1a1a;
            font-family: 'Comic Neue', cursive;
            line-height: 1.7;
            box-shadow: 6px 6px 0px #000;
            position: relative;
        ">
            {scene.content}
            <!-- Speech bubble tail at BOTTOM -->
            <div style="
                position: absolute;
                bottom: -20px;
                left: 30px;
                width: 0;
                height: 0;
                border-left: 15px solid transparent;
                border-right: 15px solid transparent;
                border-top: 20px solid #000;
            "></div>
            <div style="
                position: absolute;
                bottom: -14px;
                left: 33px;
                width: 0;
                height: 0;
                border-left: 12px solid transparent;
                border-right: 12px solid transparent;
                border-top: 17px solid #fff;
            "></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")


def display_comic_panel_ending(scene: Scene, scene_number: int) -> None:
    """
    Display the final scene as a special ending panel.
    
    Args:
        scene: The ending scene
        scene_number: The scene number
    """
    # Ending header with dramatic styling
    st.markdown("""
    <div style="
        text-align: center;
        margin: 20px 0;
    ">
        <span style="
            display: inline-block;
            background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
            color: #000;
            padding: 12px 30px;
            border: 4px solid #000;
            border-radius: 8px;
            font-family: 'Bangers', cursive;
            font-size: 1.8rem;
            box-shadow: 5px 5px 0px #000;
            text-shadow: 1px 1px 0px #fff;
        ">🎬 FINAL PANEL 🎬</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the image if available
    if scene.image_path and Path(scene.image_path).exists():
        image_base64 = get_image_base64(scene.image_path)
        if image_base64:
            st.markdown(f"""
            <div style="
                border: 6px solid #ffd700;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 20px rgba(255,215,0,0.5), 10px 10px 0px #000;
                margin: 15px 0;
                position: relative;
            ">
                <img src="data:image/png;base64,{image_base64}" style="
                    width: 100%;
                    display: block;
                ">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.image(scene.image_path, width="stretch", caption=None)
    else:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                height: 300px;
                border: 5px solid #ffd700;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 10px 0;
                box-shadow: 0 0 20px rgba(255,215,0,0.5), 8px 8px 0px #000;
            ">
                <span style="
                    color: white;
                    font-family: 'Bangers', cursive;
                    font-size: 2rem;
                    text-shadow: 3px 3px 0px #000;
                ">🎬 FINAL SCENE 🎬</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Ending narration box with special styling
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(180deg, #fffef0 0%, #fff8dc 100%);
            padding: 25px 30px;
            border-radius: 15px;
            border: 4px solid #ffd700;
            margin: 15px 0;
            font-size: 1.15rem;
            color: #1a1a1a;
            font-family: 'Comic Neue', cursive;
            line-height: 1.8;
            box-shadow: 0 0 15px rgba(255,215,0,0.3), 6px 6px 0px #000;
        ">
            {scene.content}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # THE END badge - comic book style
    st.markdown(
        """
        <div style="
            text-align: center;
            margin: 30px 0;
            animation: popIn 0.5s ease-out;
        ">
            <div style="
                display: inline-block;
                position: relative;
            ">
                <!-- Starburst background -->
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 250px;
                    height: 250px;
                    background: 
                        conic-gradient(
                            from 0deg,
                            #ffeb3b 0deg 20deg,
                            #ff5252 20deg 40deg,
                            #ffeb3b 40deg 60deg,
                            #ff5252 60deg 80deg,
                            #ffeb3b 80deg 100deg,
                            #ff5252 100deg 120deg,
                            #ffeb3b 120deg 140deg,
                            #ff5252 140deg 160deg,
                            #ffeb3b 160deg 180deg,
                            #ff5252 180deg 200deg,
                            #ffeb3b 200deg 220deg,
                            #ff5252 220deg 240deg,
                            #ffeb3b 240deg 260deg,
                            #ff5252 260deg 280deg,
                            #ffeb3b 280deg 300deg,
                            #ff5252 300deg 320deg,
                            #ffeb3b 320deg 340deg,
                            #ff5252 340deg 360deg
                        );
                    clip-path: polygon(
                        50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%,
                        50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%
                    );
                    z-index: 0;
                "></div>
                <span style="
                    position: relative;
                    z-index: 1;
                    display: inline-block;
                    background: linear-gradient(180deg, #1a1a1a 0%, #333 100%);
                    color: #ffd700;
                    padding: 15px 40px;
                    border-radius: 10px;
                    font-size: 2.5rem;
                    font-weight: bold;
                    font-family: 'Bangers', cursive;
                    letter-spacing: 5px;
                    border: 4px solid #ffd700;
                    box-shadow: 6px 6px 0px #000;
                    text-shadow: 2px 2px 0px #000;
                ">THE END</span>
            </div>
        </div>
        <style>
            @keyframes popIn {
                0% { transform: scale(0); opacity: 0; }
                70% { transform: scale(1.1); }
                100% { transform: scale(1); opacity: 1; }
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def display_loading_panel() -> None:
    """Display a loading placeholder for panel generation."""
    st.markdown(
        """
        <div style="
            background: linear-gradient(45deg, #1a1a2e, #16213e);
            height: 350px;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 10px 0;
            border: 5px solid #000;
            box-shadow: 8px 8px 0px #000;
            position: relative;
            overflow: hidden;
        ">
            <!-- Animated action words -->
            <div style="
                position: absolute;
                top: 20px;
                left: 20px;
                font-family: 'Bangers', cursive;
                font-size: 1.5rem;
                color: #ff5252;
                text-shadow: 2px 2px 0px #000;
                animation: shake 0.5s ease-in-out infinite;
            ">POW!</div>
            <div style="
                position: absolute;
                bottom: 20px;
                right: 20px;
                font-family: 'Bangers', cursive;
                font-size: 1.5rem;
                color: #ffeb3b;
                text-shadow: 2px 2px 0px #000;
                animation: shake 0.5s ease-in-out infinite 0.25s;
            ">ZAP!</div>
            
            <div style="
                font-size: 64px;
                animation: pulse 1s ease-in-out infinite;
            ">🎨</div>
            <span style="
                color: #fff;
                font-family: 'Bangers', cursive;
                font-size: 1.5rem;
                margin-top: 15px;
                text-shadow: 2px 2px 0px #000;
            ">CREATING YOUR PANEL...</span>
            <span style="
                color: #aaa;
                font-family: 'Comic Neue', cursive;
                font-size: 1rem;
                margin-top: 8px;
            ">This may take a few seconds</span>
        </div>
        <style>
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.15); opacity: 0.8; }
            }
            @keyframes shake {
                0%, 100% { transform: translateX(0) rotate(-5deg); }
                50% { transform: translateX(5px) rotate(5deg); }
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def display_comic_page_number(current: int, total: int) -> None:
    """Display page number indicator."""
    st.markdown(
        f"""
        <div style="
            text-align: center;
            margin: 15px 0;
        ">
            <span style="
                background: #1a1a1a;
                color: #fff;
                padding: 8px 20px;
                border-radius: 20px;
                font-family: 'Bangers', cursive;
                font-size: 1rem;
                border: 2px solid #ffd700;
            ">PAGE {current} OF {total}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
