"""
openai_request.py

This module contains functions to send prompts to the OpenAI API and handle responses.
"""
import openai
from typing import Union


async def send_prompt(prompt: str, timeout: int = 15) -> Union[str, dict]:
    """
    Sends a prompt to the OpenAI API and returns the response or an error.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        timeout (int, optional): The timeout duration for the API call. Defaults to 15 seconds.

    Returns:
        Union[str, dict]: The response from the OpenAI API as a string, or an error message as a dictionary.
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return {"error": str(e)}