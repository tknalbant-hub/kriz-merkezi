# ai_engine.py
import g4f

class AIEngine:
    def generate_logic(self, topic):
        # API anahtarı olmadan ücretsiz model çağrısı
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": f"{topic} için Python kodu yaz."}],
        )
        return response
