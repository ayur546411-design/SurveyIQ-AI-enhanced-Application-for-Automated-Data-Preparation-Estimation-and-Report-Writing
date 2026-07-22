import os
from typing import Optional

# You can use google.generativeai or langchain based on your requirements
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini Service.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is missing. Please set the GEMINI_API_KEY environment variable.")
        
        # Configure the genai client
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_insight(self, prompt: str) -> str:
        """
        Generate insights using the Gemini model based on the given prompt.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insight: {str(e)}"

# Initialize a default service instance to be imported elsewhere
gemini_service = GeminiService()
