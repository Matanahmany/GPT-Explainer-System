import json
import os
import time
import asyncio
from pathlib import Path
from file_manager import get_explanations
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Any

LOG_FOLDER = 'logs'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)

# Set up logging
logger = logging.getLogger('explainer')
handler = TimedRotatingFileHandler(
    os.path.join(LOG_FOLDER, "explainer.log"), when="midnight", interval=1, backupCount=5
)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def save_files(file_path: str, explanations: tuple[Any]) -> None:
    """Save the explanations to a JSON file."""
    output_file = file_path + ".json"
    with open(output_file, 'w') as f:
        json.dump(explanations, f, indent=2)


def main() -> None:
    """Run the explainer script to process files continuously."""
    running = True
    while running:
        for filename in os.listdir(UPLOAD_FOLDER):
            print(filename + " has identified by explainer ")
            uploads_file = os.path.join(UPLOAD_FOLDER, filename)
            logger.info(f"Processing file: {filename}")
            explain = asyncio.run(get_explanations(uploads_file))
            if explain is not None:
                output_file = os.path.join(OUTPUT_FOLDER, filename)
                save_files(output_file, explain)
                print(filename + " has explained by explainer successfully  ")
                logger.info(f"File processed successfully: {filename}")
                os.remove(uploads_file)
            else:
                logger.warning(f"No explanations generated for file: {filename}")
        time.sleep(10)


if __name__ == "__main__":
    main()
