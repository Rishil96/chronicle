import logging
import os
from openai import OpenAI
from src.llm.prompts import system_prompt


logger = logging.getLogger("chronicle")


class LLM:
    def __init__(self):
        base_url = os.getenv("LLM_BASE_URL")
        api_key = os.getenv("LLM_API_KEY")
        self.model_name = os.getenv("LLM_MODEL_NAME")
        self.llm_instance = OpenAI(api_key=api_key, base_url=base_url)

    def generate_response(self, log_message: str) -> str:
        """
        Method to generate an LLM response for input log message
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": log_message},
        ]
        logger.info("Sending log message to LLM for processing")
        try:
            response = self.llm_instance.chat.completions.create(
                messages=messages,  # type: ignore
                model=self.model_name,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM Processing failed: {e}")
            return log_message
