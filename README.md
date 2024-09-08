# GPT Explainer System

This project is a GPT-based explainer system designed to process PowerPoint presentations. It involves multiple components including a web API for file uploads and status checking, a client for interacting with the system, and various utility scripts for managing files and generating explanations.

## Project Structure

- `main.py`: Main entry point for processing PowerPoint files and saving explanations.
- `openai_request.py`: Contains functions to send prompts to the OpenAI API and handle responses.
- `explainer.py`: Continuously processes files in the upload directory, generates explanations, and saves them.
- `file_manager.py`: Manages file paths, gets explanations, and saves explanations to JSON files.
- `presentation_parser.py`: Parses PowerPoint files and extracts text from slides.
- `client.py`: A small Python client for developers to upload files and check the status of their processing.
- `app.py`: A Flask web application with endpoints for file uploads and status checking.

## Setup

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Flask

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
Install required Python packages:

bash
Copy code
pip install Flask request
Set up environment variables:

bash
Copy code
export OPENAI_API_KEY='your_openai_api_key'
Usage
Running the Web API
Navigate to the project directory.
Run the Flask app:
bash
Copy code
python app.py
The API will be available at http://127.0.0.1:5000.

Using the Client
To upload a file and get its UID:

bash
Copy code
python client.py upload <file_path>
To check the status of a file using its UID:

bash
Copy code
python client.py status <uid>
Processing Files with the Explainer
Ensure the upload folder (uploads) exists in the project directory.
Run the explainer script:
bash
Copy code
python explainer.py
The explainer script will continuously process files in the upload folder, generate explanations, and save them in the output folder (outputs).

openai_request.py
Handles sending prompts to the OpenAI API and managing responses.

explainer.py
Continuously processes files from the upload directory, generates explanations, and saves them to the output directory.

file_manager.py
Manages file paths, retrieves explanations, and saves explanations to JSON files.

presentation_parser.py
Parses PowerPoint files and extracts text from slides for explanation.

client.py
Provides a command-line interface for uploading files and checking their processing status.

app.py
Flask web application for handling file uploads and checking their processing status.

Logging
The system logs activities to the logs folder. Separate logs are maintained for the web server and the explainer.






