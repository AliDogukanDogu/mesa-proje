"""Streamlit ana sayfasi (Pano). SORUMLU: D (Plan gorev D-5).

Calistir: streamlit run app.py
Veri YALNIZ mesa.servis fonksiyonlarindan alinir.
"""

import pandas as pd
import streamlit as st

from mesa import YASAL_UYARI, servis

st.set_page_config(page_title="MESA", page_icon="📈", layout="wide")
st.title("MESA — Günün sinyalleri")

if servis.ORNEK_MOD:
    st.info("Örnek veri gösteriliyor (gerçek motor henüz bağlı değil).")

sinyaller = servis.gunun_sinyalleri()
tablo = pd.DataFrame([
    {"Hisse": s.kod, "Sonuç": s.sonuc.value, "Ayarlı skor": round(s.ayarli_skor, 2)}
    for s in sinyaller
])
# TODO(D): AL/SAT/BEKLE renk + ikon + metinle gosterilsin; rejim durumu ve veri tazeligi eklensin.
st.dataframe(tablo, hide_index=True, use_container_width=True)

st.caption(YASAL_UYARI)
