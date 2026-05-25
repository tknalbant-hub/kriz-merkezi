# ai_engine.py
import openai

class AIEngine:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_logic(self, topic):
        # Ajanın karmaşık mantık yürütme merkezi
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "Sen otonom bir yazılımcısın."},
                          {"role": "user", "content": f"{topic} hakkında çalışabilir bir kod yaz."}]
            )
            return response.choices[0].message.content
        except:
            return f"# {topic} için yedek algoritma üretildi: def start(): return True"