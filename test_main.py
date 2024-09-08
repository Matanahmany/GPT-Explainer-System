"""
test_main.py

This module contains tests for the main program using pytest.
"""

import os
import time
import pytest
from Explainer.main import main
from Client import client


def test_explain_presentation() -> None:
    """Test function for explaining a PowerPoint presentation."""

    demo_presentation_path = "AsyncIO.pptx"
    main(demo_presentation_path)
    output_file = os.path.splitext(demo_presentation_path)[0] + ".json"
    assert os.path.exists(output_file), f"{output_file} does not exist"

    # Clean up the output file after the test
    if os.path.exists(output_file):
        os.remove(output_file)


def test_all_the_system() -> None:
    """Test the entire system, including file upload and status checking."""
    file_uid = client.upload("AsyncIO.pptx")
    print(f"File UID: {file_uid}")
    running = True
    while running:
        try:
            status = client.check_status(file_uid)
            assert status.status == 'done'
            assert status.timestamp
            assert status.filename == "AsyncIO.pptx"
            assert status.explanation
            running = False
        except RuntimeError:
            time.sleep(5)


if __name__ == "__main__":
    pytest.main()
