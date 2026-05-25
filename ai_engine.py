# ai_engine.py
import google.generativeai as genai
import streamlit as st

class AIEngine:
    def __init__(self):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Güncel ve stabil model:
        self.model = genai.GenerativeModel('gemini-1.5-flash') 

    def generate_logic(self, topic):
        response = self.model.generate_content(f"Sen otonom bir yazılımcısın. {topic} konusunu araştır ve üzerinde çalışılabilir, profesyonel bir Python kodu yaz. Sadece kodu ver.")
        return response.text
