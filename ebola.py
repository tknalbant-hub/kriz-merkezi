import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# AYARLAR
st.set_page_config(page_title="5A48K V5.0 VISUAL", layout="wide")

# CSS ile Modern Koyu Tema ve Stil
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c24; padding: 20px; border-radius: 12px; border: 1px solid #2d2f3b; }
    h1 { color: #00f2ff; font-family: 'Urbanist', sans-serif; text-transform: uppercase; }
    h2 { color: #deff9a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 5A48K GLOBAL CRISIS OBSERVATORY v5.0")
st.sidebar.header("📡 KONTROL MERKEZİ")

# VERİ KAYNAKLARI (API)
sources = {
    "COVID-19": "https://disease.sh/v3/covid-19/all",
    "Mpox": "https://disease.sh/v3/covid-19/mpox/all",
    "Influenza (Grip)": "https://disease.sh/v3/covid-19/influenza/all"
}

# 1. VERİ ÇEKME MOTORU
@st.cache_data(ttl=3600)
def get_patojen_data():
    data_list = []
    # Tarih aralığı (Son 8 hafta)
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=8)
    dates = pd.date_range(start=start_date, end=end_date, freq='W').strftime('%Y-%m-%d').tolist()

    for name, url in sources.items():
        try:
            # Gerçek zamanlı veri
            res = requests.get(url, timeout=10).json()
            total_cases = res.get('cases', 0)
            today_cases = res.get('todayCases', 0)
            
            # Artış Hızı (%) Hesaplama (Bugünkü vaka / Toplam Vaka)
            growth = (today_cases / (total_cases + 1)) * 100
            
            # Çizgi grafik için simüle edilmiş haftalık trend verisi (Gerçek API haftalık veri vermiyor)
            # Burada trendi gösteren bir veri seti oluşturuyoruz.
            base = total_cases * 0.9
            trend = [base + (total_cases - base) * (i / (len(dates)-1)) for i in range(len(dates))]
            
            # Ana veriyi ekle
            data_list.append({
                "Patojen": name,
                "Toplam Vaka": total_cases,
                "Artış Hızı (%)": round(growth, 4),
                "dates": dates,
                "trend": trend
            })
        except:
            pass
    return data_list

# 2. VERİYİ İŞLE VE GÖSTER
patojen_data = get_patojen_data()

if not patojen_data:
    st.error("Veri kaynaklarına ulaşılamıyor. Lütfen daha sonra tekrar deneyin.")
else:
    # --- Üst Bölüm: Metrik Kartları ---
    st.header("⚡ Anlık Küresel Durum")
    cols = st.columns(len(patojen_data))
    for i, data in enumerate(patojen_data):
        cols[i].metric(
            label=f"{data['Patojen']} Toplam",
            value=f"{data['Toplam Vaka']:,}",
            delta=f"{data['Artış Hızı (%)']:.4f}% Hız",
            delta_color="off" if data['Artış Hızı (%)'] < 1 else "normal"
        )
    st.divider()

    # --- Orta Bölüm: Çizgi Grafikler (Trendler) ---
    st.header("📈 Haftalık Yayılım Trendleri (Son 8 Hafta)")
    
    # Veriyi grafiğe uygun formata dönüştür
    plot_df_list = []
    for data in patojen_data:
        for d, t in zip(data['dates'], data['trend']):
            plot_df_list.append({"Patojen": data['Patojen'], "Tarih": d, "Vaka Sayısı": t})
    
    plot_df = pd.DataFrame(plot_df_list)

    # Plotly Çizgi Grafiği
    fig = px.line(plot_df, x="Tarih", y="Vaka Sayısı", color="Patojen", 
                  title="Patojen Yayılım Hızı Karşılaştırması",
                  template="plotly_dark",
                  labels={"Vaka Sayısı": "Tahmini Vaka Sayısı", "Tarih": "Haftalık Dönem"})
    
    fig.update_layout(
        font_family="Urbanist",
        hovermode="x unified",
        legend_title_text="Patojen Türü"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # --- Alt Bölüm: Detaylı Tablo ---
    st.header("📋 Detaylı Veri Tablosu")
    
    # Tablo için veriyi temizle (trend listesini çıkar)
    table_data = []
    for d in patojen_data:
        table_data.append({
            "Patojen": d["Patojen"],
            "Toplam Vaka": d["Toplam Vaka"],
            "Artış Hızı (%)": d["Artış Hızı (%)"]
        })
    
    # Tabloyu göster
    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True,
        hide_index=True
    )

    st.sidebar.success(f"Sistem Operasyonel. {len(patojen_data)} patojen izleniyor.")
    st.sidebar.write(f"Son Güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
