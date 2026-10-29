"""Ayarlar ve hakkinda. SORUMLU: D (Plan gorev D-6)."""

import streamlit as st

from mesa import YASAL_UYARI
from mesa.ayarlar import ayarlar

st.title("Ayarlar ve hakkında")
st.warning(YASAL_UYARI)

# TODO(D): veri kaynaklari, proje ekibi, parametrelerin aciklamasi.
st.subheader("Parametreler (salt okunur)")
st.json(ayarlar())

st.caption(YASAL_UYARI)
