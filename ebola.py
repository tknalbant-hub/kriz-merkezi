import requests
from bs4 import BeautifulSoup
import json
import os

# Beynin öğrendiklerini saklayacağı "Uzun Süreli Bellek" (JSON dosyası)
MEMORY_FILE = "dijital_beyin_hafizasi.json"

def web_tara(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Sitenin sadece ana metnini al
        metin = soup.get_text(separator=' ', strip=True)[:1000] 
        return metin
    except:
        return None

def hafizaya_kaydet(yeni_bilgi):
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            hafiza = json.load(f)
    else:
        hafiza = []
    
    hafiza.append({"bilgi": yeni_bilgi, "zaman": time.time()})
    with open(MEMORY_FILE, 'w') as f:
        json.dump(hafiza, f)

# Dijital Beyin İçinde "İrade" Mekanizması
def irade_mekanizmasi(G):
    # Eğer ağdaki bağlantılar (öğrenme) çok güçlüyse, 
    # beyin "yeni bilgiye aç" demektir.
    toplam_w = sum(G[u][v].get('w', 0.1) for u, v in G.edges())
    
    if toplam_w > 50: # Beyin yeterince olgunlaştıysa
        url = "https://www.wikipedia.org/" # Burayı dinamik yapabilirsin
        yeni_veri = web_tara(url)
        if yeni_veri:
            hafizaya_kaydet(yeni_veri)
            return f"Yeni bilgi depolandı: {url}"
    return "Sistem beklemede..."
