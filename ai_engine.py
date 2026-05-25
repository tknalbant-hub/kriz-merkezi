# ai_engine.py
import google.generativeai as genai

class AIEngine:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_logic(self, topic):
        response = self.model.generate_content(f"Sen otonom bir yazılımcısın. {topic} konusunda çalışabilir, verimli bir Python kodu yaz.")
        return response.text
