import sys
import time

import requests
from datetime import datetime
from typing import Optional

API_URL = "http://127.0.0.1:5000"
TIME_FORMAT = '%Y-%m-%d-%H-%M-%S'
NOT_FOUND = 404
OK = 200


class Status:
    def __init__(self, status: str, filename: str, timestamp: datetime, explanation: Optional[str]):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation

    def is_done(self) -> bool:
        """Check if the processing status is 'done'."""
        return self.status == 'done'


def upload(file_path: str) -> str:
    """Upload a file to the server and return the UID."""
    with open(file_path, 'rb') as file:
        response = requests.post(f"{API_URL}/upload", files={'file': file})
    if response.status_code != OK:
        raise RuntimeError(f"Failed to upload file: {response.json().get('error', 'Unknown error')}")

    return response.json()['uid']


def check_status(uid: str) -> Status:
    """Check the status of a file by its UID."""
    response = requests.get(f"{API_URL}/status/{uid}")

    if response.status_code == NOT_FOUND:
        raise RuntimeError("UID not found")
    elif response.status_code != OK:
        raise RuntimeError(f"Failed to check status: {response.json().get('error', 'Unknown error')}")
    data = response.json()
    status = Status(
        status=data['status'],
        filename=data['filename'],
        timestamp=datetime.strptime(data['timestamp'], TIME_FORMAT),
        explanation=data.get('explanation')
    )
    if not status.is_done():
        raise RuntimeError(f"{status.status}")
    return status


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python client.py <command> <arguments>")
        print("Commands:")
        print("  upload <file_path>  - Upload a file")
        print("  status <uid>       - Check the status of a file by UID")
        return
    command = sys.argv[1]
    if command == 'upload':
        file_path = sys.argv[2]
        try:
            uid = upload(file_path)
            print(f"File uploaded successfully. UID: {uid}")
            running = True
            while running:
                try:
                    status = check_status(uid)
                    if status.is_done():
                        print(f"Processing completed for file {status.filename} at {status.timestamp}")
                        print(f"Explanation: {status.explanation}")
                        running = False
                    else:
                        print(f"Status: {status.status}. Retrying in 10 seconds...")
                        time.sleep(10)
                except RuntimeError as e:
                    print(f"Error: {e}. Retrying in 10 seconds...")
                    time.sleep(10)
        except Exception as e:
            print(f"Error uploading file: {e}")

    elif command == 'status':
        uid = sys.argv[2]
        try:
            status = check_status(uid)
            if status.is_done():
                print(f"Processing completed for file {status.filename} at {status.timestamp}")
                print(f"Explanation: {status.explanation}")
            else:
                print(f"Status: {status.status}")
        except Exception as e:
            print(f"Error checking status: {e}")
    else:
        print("Unknown command. Use 'upload' or 'status'.")


if __name__ == "__main__":
    main()
