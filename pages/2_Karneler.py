"""Degisken karneleri. SORUMLU: D (Plan gorev D-7)."""

import pandas as pd
import streamlit as st

from mesa import YASAL_UYARI, servis

st.title("Değişken karneleri")
karneler = servis.karneler()

# TODO(D): 7 testin hepsi sutun olsun; karara gore renk; IC bozunma grafigi.
st.dataframe(pd.DataFrame([{
    "Değişken": k.degisken_id, "IC": k.ic, "q": k.q_degeri,
    "Karar": k.karar.value, "Ağırlık": k.agirlik,
} for k in karneler]), hide_index=True, use_container_width=True)

st.caption(YASAL_UYARI)
