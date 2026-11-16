"""Hisse detayi sayfasi (Plan gorev D-5) icin birim testleri."""

import importlib.util
from pathlib import Path

import pandas as pd


def _sayfa_modulunu_yukle():
    """pages/ altindaki hisse detayi modulunu dosya adindan bagimsiz yukler."""
    pages_dizini = Path(__file__).resolve().parent.parent / "pages"
    adaylar = sorted(pages_dizini.glob("*hisse*.py"))
    assert adaylar, "pages/ klasorunde hisse detayi dosyasi bulunamadi."
    spec = importlib.util.spec_from_file_location("hisse_detayi_sayfasi", adaylar[0])
    modul = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(modul)
    return modul


def test_plotly_fiyat_grafigi_al_sat_isaretleri():
    """Fiyat grafiginin kapanis cizgisi ile AL ve SAT marker izlerini ekledigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    fiyat = pd.DataFrame({
        "tarih": ["2026-11-01", "2026-11-02", "2026-11-03"],
        "kapanis": [100.0, 105.0, 102.0],
    })
    gecmis = pd.DataFrame({
        "tarih": ["2026-11-01", "2026-11-03"],
        "sonuc": ["AL", "SAT"],
        "ayarli_skor": [0.75, -0.60],
    })

    fig = modul.plotly_fiyat_grafigi(fiyat, gecmis, "THYAO")
    trace_isimleri = [t.name for t in fig.data]

    assert "Kapanış Fiyatı" in trace_isimleri
    assert "AL Sinyali" in trace_isimleri
    assert "SAT Sinyali" in trace_isimleri


def test_en_buyuk_uc_katki_siralamasi():
    """Son kayittan mutlak degerce en buyuk 3 katkinin dogru secildigini test eder."""
    modul = _sayfa_modulunu_yukle()
    gecmis = pd.DataFrame([
        {
            "tarih": "2026-11-03",
            "sonuc": "AL",
            "ayarli_skor": 0.65,
            "katkilar": {
                "Momentum": 0.42,
                "Hacim": -0.31,
                "Trend": 0.55,
                "Volatilite": 0.08,
            },
        }
    ])

    top3 = modul.en_buyuk_uc_katki(gecmis)

    assert len(top3) == 3
    assert top3[0] == ("Trend", 0.55)
    assert top3[1] == ("Momentum", 0.42)
    assert top3[2] == ("Hacim", -0.31)


def test_plotly_skor_grafigi_veri_olusturma():
    """Ayarli skor gecmisinin Plotly grafigine dogru aktarildigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    gecmis = pd.DataFrame({
        "tarih": ["2026-11-01", "2026-11-02", "2026-11-03"],
        "ayarli_skor": [0.20, 0.55, -0.15],
    })

    fig = modul.plotly_skor_grafigi(gecmis, "ASELS")

    assert len(fig.data) == 1
    assert fig.data[0].name == "Ayarlı Skor"
    assert list(fig.data[0].y) == [0.20, 0.55, -0.15]