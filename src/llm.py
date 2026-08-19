from groq import Groq
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

client = Groq(api_key=settings.groq_api_key)

def generate_response(prompt):

    if not isinstance(prompt, str):
        raise TypeError("The prompt should be a String.")

    if prompt.strip()  == "":
        raise ValueError("Please enter the prompt.")

    model_check = client.chat.completions.create(
        model=settings.model,
        messages = [
           { 
            "role" : "user",
            "content" : prompt
            }
        ],
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        reasoning_effort="low"
    )

    logger.info("LLM response generated successfully.")
    return model_check.choices[0].message.content