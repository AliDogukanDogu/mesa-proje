"""Backtest raporu sayfasi (Plan gorev D-7) icin birim testleri."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pandas as pd


def _sayfa_modulunu_yukle():
    """pages/ altindaki backtest raporu modulunu dosya adindan bagimsiz yukler."""
    pages_dizini = Path(__file__).resolve().parent.parent / "pages"
    adaylar = sorted(pages_dizini.glob("*backtest*.py"))
    assert adaylar, "pages/ klasorunde backtest raporu dosyasi bulunamadi."
    spec = importlib.util.spec_from_file_location("backtest_raporu_sayfasi", adaylar[0])
    modul = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(modul)
    return modul


def test_xu100_karsilastirma_grafigi_izleri():
    """Strateji ve XU100 endeks serilerinin ayni bazda grafige eklendigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    egri = pd.DataFrame(
        {
            "tarih": ["2026-01-01", "2026-06-01", "2026-11-01"],
            "strateji": [100.0, 118.0, 135.0],
            "xu100": [100.0, 108.0, 115.0],
        }
    )
    metrik = SimpleNamespace(
        isabet_orani=0.6, kar_faktoru=1.5, sharpe=1.2, max_dusus=0.1, islem_sayisi=40
    )

    fig = modul.xu100_karsilastirma_grafigi(egri, metrik)
    iz_adlari = [t.name for t in fig.data]

    assert "MESA Stratejisi (Baz=100)" in iz_adlari
    assert "XU100 Endeksi (Baz=100)" in iz_adlari
    assert list(fig.data[0].y) == [100.0, 118.0, 135.0]


def test_pencere_bazli_sonuclar_alfa_hesabi():
    """Zaman pencereleri icin strateji, XU100 ve gorece alfa farkinin dogru hesaplandigini test eder."""
    modul = _sayfa_modulunu_yukle()
    egri = pd.DataFrame(
        {
            "tarih": ["2026-01", "2026-02", "2026-03", "2026-04"],
            "strateji": [100.0, 110.0, 120.0, 132.0],
            "xu100": [100.0, 105.0, 110.0, 115.5],
        }
    )

    sonuc_df = modul.pencere_bazli_sonuclar(egri, pencere_sayisi=2)

    assert len(sonuc_df) == 2
    assert list(sonuc_df.columns) == [
        "Pencere",
        "Strateji Getirisi (%)",
        "XU100 Getirisi (%)",
        "Görece Fark (Alfa %)",
    ]
    assert sonuc_df.loc[0, "Strateji Getirisi (%)"] == 10.0
    assert sonuc_df.loc[0, "XU100 Getirisi (%)"] == 5.0
    assert sonuc_df.loc[0, "Görece Fark (Alfa %)"] == 5.0


def test_rastgele_kiyas_dagilimi_grafigi_yuzdelik():
    """Rastgele kiyas dagilim grafigi ve strateji yuzdelik diliminin dogru uretildigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    egri = pd.Series([100.0, 105.0, 112.0, 120.0])  # +%20 toplam getiri
    metrik = SimpleNamespace(rastgele_dagilim=[-5.0, 0.0, 4.0, 8.0, 12.0, 15.0, 18.0, 25.0])

    fig, yuzdelik = modul.rastgele_kiyas_dagilimi_grafigi(egri, metrik)

    assert len(fig.data) == 1
    assert fig.data[0].type == "histogram"
    assert yuzdelik == 87.5  # 8 degerden 7 tanesi 20.0'den kucuk/esit
