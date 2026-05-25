import streamlit as st
import requests

class AIEngine:
    def __init__(self):
        # API anahtarını alıyoruz
        self.api_key = st.secrets["GEMINI_API_KEY"]
        # HATA BURADAYDI: v1beta yerine artık tam sürüm olan v1 kullanıyoruz
        self.url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={self.api_key}"

    def generate_logic(self, topic):
        # Gemini'a göndereceğimiz komut paketi
        payload = {
            "contents": [{
                "parts": [{"text": f"Sen otonom bir yazılımcısın. {topic} konusunu araştır ve üzerinde çalışılabilir, profesyonel bir Python kodu yaz. Sadece kodu ver, hiçbir açıklama veya markdown (```) işareti ekleme."}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            # İsteği gönder
            response = requests.post(self.url, headers=headers, json=payload)
            data = response.json()
            
            # Eğer Google'dan beklenmedik bir hata dönerse (örn: kota aşımı) ajanın çökmemesi için kontrol:
            if 'candidates' not in data:
                return f"# Google API Yanıt Hatası:\n# {data}"
            
            # Gelen verinin içinden sadece yazılan kodu çek
            kod_metni = data['candidates'][0]['content']['parts'][0]['text']
            
            # Eğer AI inat edip ```python gibi işaretler koyarsa onları temizle ki hata vermesin
            kod_metni = kod_metni.replace("```python", "").replace("```", "").strip()
            
            return kod_metni
            
        except Exception as e:
            # İnternet kopması vb. durumlarda sistemi koru
            return f"# Sistemsel Bağlantı Hatası:\n# {str(e)}"
