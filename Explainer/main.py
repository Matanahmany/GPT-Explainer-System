"""
main.py

This is the main entry point of the program, orchestrating the overall process
of explaining PowerPoint presentations.
"""
import os
from typing import Optional
import asyncio
from file_manager import get_file_path, save_explanations, get_explanations


def main(file_path: Optional[str] = None) -> None:
    """
    Main function to process the PowerPoint file and save explanations.

    Args:
        file_path (Optional[str], optional): Path to the PowerPoint file. Defaults to None.

    Returns:
        None
    """
    if file_path is None:
        file_path = get_file_path()

    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return

    explanations = asyncio.run(get_explanations(file_path))
    save_explanations(file_path, explanations)


if __name__ == "__main__":
    main()