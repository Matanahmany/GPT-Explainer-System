"""
file_manager.py

This module contains functions for managing file paths, getting explanations,
and saving explanations to JSON files.
"""

from Explainer.presentation_parser import parse
from Explainer.openai_request import send_prompt
import asyncio
import os
import json
import argparse
from typing import Any


def get_file_path() -> str:
    """
    Parses command line arguments to get the file path.

    Returns:
        str: The path to the PowerPoint file.
    """

    parser = argparse.ArgumentParser(description="Explain PowerPoint presentation using GPT-3.5")
    parser.add_argument("file_path", type=str, help="Path to the .pptx file")
    return parser.parse_args().file_path


async def get_explanations(file_path: str, timeout: int = 15) -> tuple[Any]:
    """
    Gets explanations for each slide in the PowerPoint file.

    Args:
        file_path (str): Path to the PowerPoint file.
        timeout (int, optional): The timeout duration for the API call. Defaults to 15 seconds.

    Returns:
        tuple[Any]: A tuple containing the explanations or error messages for each slide.
    """
    slides_text = parse(file_path)
    tasks = [send_prompt(f"Give a short explanation of this slide:\n{slide}", timeout=timeout) for slide in slides_text]
    return await asyncio.gather(*tasks)


def save_explanations(file_path: str, explanations: tuple[Any]) -> None:
    """
    Saves the explanations to a JSON file.

    Args:
        file_path (str): Path to the PowerPoint file.
        explanations (tuple[Any]): The explanations to save.

    Returns:
        None
    """
    output_file = os.path.splitext(file_path)[0] + ".json"
    with open(output_file, 'w') as f:
        json.dump(explanations, f, indent=2)
    print(f"Explanations saved to {output_file}")