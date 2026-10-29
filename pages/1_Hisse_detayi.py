"""Hisse detayi. SORUMLU: D (Plan gorev D-5)."""

import streamlit as st

from mesa import YASAL_UYARI, servis
from mesa.ayarlar import hisse_kodlari

st.title("Hisse detayı")
kod = st.selectbox("Hisse", hisse_kodlari())
fiyat, gecmis = servis.hisse_gecmisi(kod)

# TODO(D): Plotly fiyat grafigi + AL/SAT isaretleri; en buyuk 3 katki; skor gecmisi.
st.line_chart(fiyat["kapanis"])
st.dataframe(gecmis, hide_index=True)

st.caption(YASAL_UYARI)
