import streamlit as st
import requests

class AIEngine:
    def __init__(self):
        # API anahtarını Streamlit'in güvenli alanından alıyoruz
        self.api_key = st.secrets["GEMINI_API_KEY"]
        # En güncel v1 sürümü ve stabil modeli kullanıyoruz
        self.url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.api_key}"

    def generate_logic(self, topic):
        payload = {
            "contents": [{
                "parts": [{"text": f"Sen otonom bir yazılımcısın. {topic} konusunu araştır ve üzerinde çalışılabilir, profesyonel bir Python kodu yaz. Sadece kodu ver, açıklama yapma."}]
            }]
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            data = response.json()
            
            # Gelen cevabı güvenli bir şekilde çekiyoruz
            return data['candidates'][0]['content']['parts'][0]['text'].replace("```python", "").replace("```", "").strip()
            
        except Exception as e:
            return f"# Hata: {str(e)}"
