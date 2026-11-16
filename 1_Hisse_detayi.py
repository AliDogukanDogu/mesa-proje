"""Hisse detayi. SORUMLU: D (Plan gorev D-5)."""

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from mesa import YASAL_UYARI, servis
from mesa.ayarlar import hisse_kodlari


def en_buyuk_uc_katki(gecmis: pd.DataFrame) -> list[tuple[str, float]]:
    """Gecmis tablosundaki son kayittan sinyale etki eden en buyuk 3 katkiyi cikarir."""
    if gecmis is None or gecmis.empty:
        return []

    son_satir = gecmis.iloc[-1]

    # 1. Durum: 'katkilar' adinda dict veya liste/tuple iceren bir kolon varsa
    if "katkilar" in gecmis.columns and pd.notna(son_satir["katkilar"]):
        ham = son_satir["katkilar"]
        if isinstance(ham, dict):
            sirali = sorted(ham.items(), key=lambda x: abs(float(x[1])), reverse=True)
            return [(str(k), round(float(v), 4)) for k, v in sirali[:3]]
        if isinstance(ham, (list, tuple)):
            sirali = sorted(ham, key=lambda x: abs(float(x[1])), reverse=True)
            return [(str(k), round(float(v), 4)) for k, v in sirali[:3]]

    # 2. Durum: Sayisal gosterge/faktor kolonlarindan en yuksek mutlak katkili 3 tanesi
    haric_kolonlar = {"tarih", "date", "kod", "hisse", "sonuc", "sinyal", "ayarli_skor", "skor", "fiyat", "kapanis"}
    sayisal_katkilar: list[tuple[str, float]] = []
    for kol in gecmis.columns:
        if kol.lower() in haric_kolonlar:
            continue
        deger = son_satir[kol]
        if isinstance(deger, (int, float)) and pd.notna(deger):
            sayisal_katkilar.append((str(kol), round(float(deger), 4)))

    sayisal_katkilar.sort(key=lambda x: abs(x[1]), reverse=True)
    return sayisal_katkilar[:3]


def plotly_fiyat_grafigi(fiyat: pd.DataFrame, gecmis: pd.DataFrame, kod: str) -> go.Figure:
    """Kapanis fiyat grafigini ve uzerindeki AL/SAT sinyal isaretlerini olusturur."""
    fig = go.Figure()

    if fiyat is None or fiyat.empty or "kapanis" not in fiyat.columns:
        fig.update_layout(title=f"{kod} — Fiyat verisi bulunamadı")
        return fig

    x_ekseni = fiyat["tarih"] if "tarih" in fiyat.columns else fiyat.index

    fig.add_trace(
        go.Scatter(
            x=x_ekseni,
            y=fiyat["kapanis"],
            mode="lines",
            name="Kapanış Fiyatı",
            line={"color": "#2563eb", "width": 2},
        )
    )

    if gecmis is not None and not gecmis.empty:
        sinyal_kol = next((c for c in ("sonuc", "sinyal", "Sonuç") if c in gecmis.columns), None)
        tarih_kol = "tarih" if "tarih" in gecmis.columns else None

        if sinyal_kol is not None:
            g_df = gecmis.copy()
            g_df["_norm_sinyal"] = g_df[sinyal_kol].astype(str).str.strip().str.upper()

            if tarih_kol and "tarih" in fiyat.columns:
                birlesik = pd.merge(g_df, fiyat[["tarih", "kapanis"]], on="tarih", how="inner")
                x_kaynak = birlesik["tarih"]
                y_kaynak = birlesik["kapanis"]
            else:
                birlesik = g_df.join(fiyat[["kapanis"]], how="inner")
                x_kaynak = birlesik.index
                y_kaynak = birlesik["kapanis"]

            if not birlesik.empty:
                al_mask = birlesik["_norm_sinyal"] == "AL"
                sat_mask = birlesik["_norm_sinyal"] == "SAT"

                if al_mask.any():
                    fig.add_trace(
                        go.Scatter(
                            x=x_kaynak[al_mask],
                            y=y_kaynak[al_mask],
                            mode="markers",
                            name="AL Sinyali",
                            marker={"symbol": "triangle-up", "size": 12, "color": "#16a34a"},
                        )
                    )
                if sat_mask.any():
                    fig.add_trace(
                        go.Scatter(
                            x=x_kaynak[sat_mask],
                            y=y_kaynak[sat_mask],
                            mode="markers",
                            name="SAT Sinyali",
                            marker={"symbol": "triangle-down", "size": 12, "color": "#dc2626"},
                        )
                    )

    fig.update_layout(
        title=f"{kod} — Kapanış Fiyatı ve AL/SAT Sinyalleri",
        xaxis_title="Tarih",
        yaxis_title="Fiyat (TL)",
        hovermode="x unified",
        margin={"l": 20, "r": 20, "t": 45, "b": 20},
    )
    return fig


def plotly_skor_grafigi(gecmis: pd.DataFrame, kod: str) -> go.Figure:
    """Hissenin gecmis ayarli skor degisimini cizen Plotly grafigini dondurur."""
    fig = go.Figure()

    if gecmis is None or gecmis.empty:
        fig.update_layout(title=f"{kod} — Skor geçmişi bulunamadı")
        return fig

    skor_kol = next((c for c in ("ayarli_skor", "skor", "Ayarlı skor") if c in gecmis.columns), None)
    if skor_kol is None:
        fig.update_layout(title=f"{kod} — Skor kolonu bulunamadı")
        return fig

    x_ekseni = gecmis["tarih"] if "tarih" in gecmis.columns else gecmis.index

    fig.add_trace(
        go.Scatter(
            x=x_ekseni,
            y=gecmis[skor_kol],
            mode="lines+markers",
            name="Ayarlı Skor",
            line={"color": "#7c3aed", "width": 2},
        )
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.6)
    fig.update_layout(
        title=f"{kod} — Ayarlı Skor Geçmişi",
        xaxis_title="Tarih",
        yaxis_title="Skor",
        hovermode="x unified",
        margin={"l": 20, "r": 20, "t": 45, "b": 20},
    )
    return fig


def hisse_detay_sayfasi() -> None:
    """Hisse detayi arayuzunu cizer."""
    st.title("Hisse detayı")
    kod = st.selectbox("Hisse", hisse_kodlari())
    fiyat, gecmis = servis.hisse_gecmisi(kod)

    # 1. Plotly fiyat grafigi + AL/SAT isaretleri
    fig_fiyat = plotly_fiyat_grafigi(fiyat, gecmis, kod)
    st.plotly_chart(fig_fiyat, use_container_width=True)

    # 2. En buyuk 3 katki
    st.subheader("Son Sinyale En Büyük 3 Katkı")
    katkilar = en_buyuk_uc_katki(gecmis)
    if katkilar:
        kolonlar = st.columns(len(katkilar))
        for idx, (ad, deger) in enumerate(katkilar):
            with kolonlar[idx]:
                st.metric(label=ad, value=f"{deger:+.4f}")
    else:
        st.info("Bu hisse için ayrıştırılabilir bileşen katkısı bulunamadı.")

    # 3. Skor gecmisi grafigi ve tablosu
    st.subheader("Skor Geçmişi")
    fig_skor = plotly_skor_grafigi(gecmis, kod)
    st.plotly_chart(fig_skor, use_container_width=True)
    st.dataframe(gecmis, hide_index=True, use_container_width=True)

    st.caption(YASAL_UYARI)


hisse_detay_sayfasi()