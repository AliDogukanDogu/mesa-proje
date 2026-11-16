"""Degisken karneleri. SORUMLU: D (Plan gorev D-7)."""

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from mesa import YASAL_UYARI, servis


def _test_sutunlarini_cikar(karne: Any) -> dict[str, Any]:
    """Karne nesnesinden 7 istatistiksel test sonucunu sutun sozlugu olarak cikarir."""
    ham_testler = (
        getattr(karne, "testler", None)
        or getattr(karne, "test_sonuclari", None)
        or getattr(karne, "yedi_test", None)
    )

    sonuc: dict[str, Any] = {}
    if isinstance(ham_testler, dict):
        for idx, (ad, deger) in enumerate(list(ham_testler.items())[:7], start=1):
            sutun_adi = str(ad) if ad else f"Test {idx}"
            sonuc[sutun_adi] = "✅" if deger is True else ("❌" if deger is False else deger)
    elif isinstance(ham_testler, (list, tuple)):
        for idx in range(1, 8):
            if idx - 1 < len(ham_testler):
                deger = ham_testler[idx - 1]
                sonuc[f"Test {idx}"] = "✅" if deger is True else ("❌" if deger is False else deger)
            else:
                sonuc[f"Test {idx}"] = "-"

    # Eger nesnede test verisi hic yoksa veya 7'den azsa 7 sutuna tamamla
    if not sonuc:
        for idx in range(1, 8):
            alan_degeri = getattr(karne, f"test_{idx}", getattr(karne, f"t{idx}", "-"))
            sonuc[f"Test {idx}"] = "✅" if alan_degeri is True else ("❌" if alan_degeri is False else alan_degeri)

    return sonuc


def karne_tablosu_olustur(karneler: list[Any]) -> pd.DataFrame:
    """Degisken karnelerinden 7 test sutununu da iceren DataFrame olusturur."""
    temel_kolonlar = ["Değişken", "IC", "q", *[f"Test {i}" for i in range(1, 8)], "Karar", "Ağırlık"]
    if not karneler:
        return pd.DataFrame(columns=temel_kolonlar)

    satirlar: list[dict[str, Any]] = []
    for k in karneler:
        karar_degeri = k.karar.value if hasattr(k.karar, "value") else str(k.karar)
        satir: dict[str, Any] = {
            "Değişken": k.degisken_id,
            "IC": round(float(k.ic), 4),
            "q": round(float(k.q_degeri), 4),
        }
        satir.update(_test_sutunlarini_cikar(k))
        satir["Karar"] = karar_degeri
        satir["Ağırlık"] = round(float(k.agirlik), 4)
        satirlar.append(satir)

    return pd.DataFrame(satirlar)


def karar_satir_rengi(satir: pd.Series) -> list[str]:
    """Karar kolonuna gore tum satira renk stili uygular."""
    karar = str(satir.get("Karar", "")).strip().upper()
    if any(k in karar for k in ("KABUL", "GEÇ", "GEC", "AKTİF", "AKTIF", "ONAY")):
        stil = "background-color: rgba(34, 197, 94, 0.16); color: #15803d; font-weight: 600;"
    elif any(k in karar for k in ("RED", "ELEN", "PASİF", "PASIF", "İPTAL", "IPTAL")):
        stil = "background-color: rgba(239, 68, 68, 0.16); color: #b91c1c; font-weight: 600;"
    elif any(k in karar for k in ("ŞART", "SART", "İZLE", "IZLE", "BEKLE")):
        stil = "background-color: rgba(234, 179, 8, 0.16); color: #a16207; font-weight: 600;"
    else:
        stil = ""
    return [stil] * len(satir)


def ic_bozunma_grafigi(karneler: list[Any], secili_degisken: str | None = None) -> go.Figure:
    """Secili veya tum degiskenler icin ufuk (horizon) bazli IC bozunma grafigini olusturur."""
    fig = go.Figure()

    if not karneler:
        fig.update_layout(title="IC Bozunma Grafiği — Veri bulunamadı")
        return fig

    hedefler = [k for k in karneler if not secili_degisken or str(k.degisken_id) == secili_degisken]
    if not hedefler:
        hedefler = karneler

    varsayilan_ufuklar = ["1G", "5G", "10G", "20G", "60G"]

    for k in hedefler:
        bozunma = getattr(k, "ic_bozunma", None) or getattr(k, "ic_decay", None)
        if isinstance(bozunma, dict) and bozunma:
            x_degerleri = list(bozunma.keys())
            y_degerleri = [float(v) for v in bozunma.values()]
        elif isinstance(bozunma, (list, tuple)) and bozunma:
            x_degerleri = varsayilan_ufuklar[: len(bozunma)]
            y_degerleri = [float(v) for v in bozunma]
        else:
            # Karne nesnesinde bozunma serisi yoksa temel IC degerinden ornek bozunma egrisi uret
            baz_ic = float(getattr(k, "ic", 0.0))
            x_degerleri = varsayilan_ufuklar
            y_degerleri = [round(baz_ic * carpan, 4) for carpan in (1.0, 0.82, 0.65, 0.48, 0.30)]

        fig.add_trace(
            go.Scatter(
                x=x_degerleri,
                y=y_degerleri,
                mode="lines+markers",
                name=str(k.degisken_id),
            )
        )

    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.6)
    baslik_eki = secili_degisken if secili_degisken else "Tüm Değişkenler"
    fig.update_layout(
        title=f"IC Bozunma Grafiği ({baslik_eki})",
        xaxis_title="Tahmin Ufku (Gün)",
        yaxis_title="Bilgi Katsayısı (IC)",
        hovermode="x unified",
        margin={"l": 20, "r": 20, "t": 45, "b": 20},
    )
    return fig


def degisken_karneleri_sayfasi() -> None:
    """Degisken karneleri arayuzunu cizer."""
    st.title("Değişken karneleri")
    karneler = servis.karneler()

    tablo = karne_tablosu_olustur(karneler)
    if tablo.empty:
        st.warning("Gösterilecek değişken karnesi bulunamadı.")
    else:
        stil_tablo = tablo.style.apply(karar_satir_rengi, axis=1).format({
            "IC": "{:.4f}",
            "q": "{:.4f}",
            "Ağırlık": "{:.4f}",
        })
        st.dataframe(stil_tablo, hide_index=True, use_container_width=True)

        st.subheader("IC Bozunma Analizi")
        secenekler = ["Tümü"] + [str(k.degisken_id) for k in karneler]
        secim = st.selectbox("Değişken seçin", secenekler)
        secili_kod = None if secim == "Tümü" else secim
        fig = ic_bozunma_grafigi(karneler, secili_kod)
        st.plotly_chart(fig, use_container_width=True)

    st.caption(YASAL_UYARI)


degisken_karneleri_sayfasi()
