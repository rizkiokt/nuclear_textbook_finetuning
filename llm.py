from langchain_google_genai import ChatGoogleGenerativeAI
import os

MODEL = "gemini-2.5-flash-preview-04-17"

class LLM:
    def __init__(self, model_name: str = MODEL):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=os.getenv("GEMINI_API_KEY"))
        