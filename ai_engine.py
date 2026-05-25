# ai_engine.py
import google.generativeai as genai
import streamlit as st

class AIEngine:
    def __init__(self):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 'gemini-1.5-flash' yerine en güncel ve standart model ismini kullanıyoruz:
        self.model = genai.GenerativeModel('gemini-pro') 

    def generate_logic(self, topic):
        response = self.model.generate_content(f"Sen otonom bir yazılımcısın. {topic} konusunu araştır ve üzerinde çalışılabilir, profesyonel bir Python kodu yaz.")
        return response.text
