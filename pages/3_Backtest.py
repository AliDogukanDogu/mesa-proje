"""Backtest raporu. SORUMLU: D (Plan gorev D-7)."""

import streamlit as st

from mesa import YASAL_UYARI, servis

st.title("Backtest raporu")
egri, m = servis.backtest_ozeti()

c = st.columns(5)
c[0].metric("İsabet", f"{m.isabet_orani:.0%}")
c[1].metric("Kâr faktörü", f"{m.kar_faktoru:.2f}")
c[2].metric("Sharpe", f"{m.sharpe:.2f}")
c[3].metric("Maks. düşüş", f"{m.max_dusus:.0%}")
c[4].metric("İşlem", m.islem_sayisi)

# TODO(D): XU100 ile karsilastirma, pencere bazli sonuclar, rastgele kiyas dagilimi.
st.line_chart(egri)

st.caption(YASAL_UYARI)
