"""Degisken karneleri sayfasi (Plan gorev D-7) icin birim testleri."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pandas as pd


def _sayfa_modulunu_yukle():
    """pages/ altindaki degisken karneleri modulunu dosya adindan bagimsiz yukler."""
    pages_dizini = Path(__file__).resolve().parent.parent / "pages"
    adaylar = sorted(pages_dizini.glob("*karne*.py"))
    assert adaylar, "pages/ klasorunde degisken karneleri dosyasi bulunamadi."
    spec = importlib.util.spec_from_file_location("degisken_karneleri_sayfasi", adaylar[0])
    modul = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(modul)
    return modul


def test_karne_tablosu_yedi_test_sutunu():
    """7 istatistiksel testin her birinin ayri sutun olarak tabloya eklendigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    ornek_karneler = [
        SimpleNamespace(
            degisken_id="RSI_14",
            ic=0.045,
            q_degeri=0.012,
            karar=SimpleNamespace(value="KABUL"),
            agirlik=0.25,
            testler={
                "T1_IC": True,
                "T2_tStat": True,
                "T3_FDR": True,
                "T4_Stabilite": True,
                "T5_Monoton": False,
                "T6_Rejim": True,
                "T7_Devir": True,
            },
        )
    ]

    df = modul.karne_tablosu_olustur(ornek_karneler)

    for test_adi in ["T1_IC", "T2_tStat", "T3_FDR", "T4_Stabilite", "T5_Monoton", "T6_Rejim", "T7_Devir"]:
        assert test_adi in df.columns
    assert df.loc[0, "T1_IC"] == "✅"
    assert df.loc[0, "T5_Monoton"] == "❌"


def test_karar_satir_rengi_stilleri():
    """KABUL ve RED kararlarina gore farkli renk stilleri uretildigini test eder."""
    modul = _sayfa_modulunu_yukle()
    satir_kabul = pd.Series({"Değişken": "MOM_20", "Karar": "KABUL", "IC": 0.05})
    satir_red = pd.Series({"Değişken": "VOL_10", "Karar": "RED", "IC": -0.01})

    stil_kabul = modul.karar_satir_rengi(satir_kabul)
    stil_red = modul.karar_satir_rengi(satir_red)

    assert len(stil_kabul) == 3
    assert "#15803d" in stil_kabul[0]
    assert "#b91c1c" in stil_red[0]


def test_ic_bozunma_grafigi_olusturma():
    """IC bozunma verilerinin Plotly grafigine dogru aktarildigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    ornek_karneler = [
        SimpleNamespace(
            degisken_id="MACD_HIST",
            ic=0.06,
            q_degeri=0.005,
            karar=SimpleNamespace(value="KABUL"),
            agirlik=0.30,
            ic_bozunma={"1G": 0.06, "5G": 0.045, "10G": 0.03, "20G": 0.015},
        )
    ]

    fig = modul.ic_bozunma_grafigi(ornek_karneler, secili_degisken="MACD_HIST")

    assert len(fig.data) == 1
    assert fig.data[0].name == "MACD_HIST"
    assert list(fig.data[0].x) == ["1G", "5G", "10G", "20G"]
    assert list(fig.data[0].y) == [0.06, 0.045, 0.03, 0.015]