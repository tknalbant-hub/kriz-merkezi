import streamlit as st
import os
import shutil
import openai
from duckduckgo_search import DDGS

# --- MODÜL 1: DUYU (İnternet) ---
def arastir(konu):
    with DDGS() as ddgs:
        return list(ddgs.text(konu, max_results=2))

# --- MODÜL 2: BEYİN (Kod Üretimi) ---
def kod_uret(konu, bilgi):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"Konu: {konu}. Bilgi: {bilgi}. Bu konuda mevcut app.py dosyamı daha verimli hale getirecek yeni fonksiyon kodları yaz. Sadece Python kodunu ver."
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

# --- MODÜL 3: EVRİM (Kod Değişimi) ---
def evrimles(yeni_kod):
    # Yedek al
    shutil.copyfile("app.py", "app.py.bak")
    # Kodu ekle
    with open("app.py", "a") as f:
        f.write(f"\n\n# --- OTONOM GÜNCELLEME ---\n{yeni_kod}")

# --- ARAYÜZ ---
st.title("🧠 Otonom Yazılım Mühendisi")

hedef = st.text_input("Ajanın üzerinde çalışmasını istediğin yeni özellik:")

if st.button("Araştır, Öğren ve Kendini Güncelle"):
    with st.spinner("İnternette öğreniyorum..."):
        bilgi = arastir(hedef)
        yeni_kod = kod_uret(hedef, bilgi)
        evrimles(yeni_kod)
        st.success("Kodum güncellendi! Yeni yeteneklerimi yüklemek için sayfayı yenile.")
        st.code(yeni_kod)