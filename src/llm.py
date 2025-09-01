import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY env var is required.")

class Gemini:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=GOOGLE_API_KEY,
            temperature=0.1
        )

    def complete(self, system: str, user: str, **kwargs) -> str:
        messages = []
        if system.strip():
            messages.append({"role": "system", "content": system.strip()})
        messages.append({"role": "user", "content": user.strip()})
        resp = self.model.invoke(messages)
        return resp.content if hasattr(resp, "content") else str(resp)

LLM = Gemini()