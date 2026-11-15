"""M3 Ozellik uretici birim testleri. SORUMLU: C."""

import numpy as np
import pandas as pd
import pytest

from mesa import kayit, ozellik


def _sentetik_veri(gun_sayisi: int = 320):
    rng = np.random.default_rng(123)
    tarihler = pd.bdate_range("2024-01-02", periods=gun_sayisi)

    def _ohlcv(baslangic: float) -> pd.DataFrame:
        getiriler = rng.normal(0.0005, 0.02, size=gun_sayisi)
        kapanis = baslangic * np.cumprod(1.0 + getiriler)
        return pd.DataFrame(
            {
                "acilis": kapanis * 0.995,
                "yuksek": kapanis * 1.01,
                "dusuk": kapanis * 0.99,
                "kapanis": kapanis,
                "hacim": rng.integers(1_000_000, 5_000_000, size=gun_sayisi).astype(float),
            },
            index=tarihler,
        )

    fiyatlar = {"AKBNK": _ohlcv(50.0), "THYAO": _ohlcv(280.0)}
    piyasa = {
        "XU100": _ohlcv(9000.0),
        "VIX": _ohlcv(18.0),
        "DXY": _ohlcv(104.0),
        "ABD10Y": _ohlcv(4.2),
        "BRENT": _ohlcv(80.0),
        "ALTIN": _ohlcv(2300.0),
        "BAKIR": _ohlcv(4.3),
        "USDTRY": _ohlcv(32.0),
    }
    makro = {
        "politika_faizi": pd.Series(np.linspace(45.0, 50.0, gun_sayisi), index=tarihler),
        "tufe": pd.Series(np.linspace(65.0, 48.0, gun_sayisi), index=tarihler),
        "tuketici_guven": pd.Series(np.linspace(78.0, 82.0, gun_sayisi), index=tarihler),
    }
    return fiyatlar, piyasa, makro


def test_tum_24_degisken_hesaplanir():
    fiyatlar, piyasa, makro = _sentetik_veri(300)
    tum_kayitlar = kayit.degiskenleri_oku()
    assert len(tum_kayitlar) == 24

    for d in tum_kayitlar:
        seri = ozellik.ham_degisken(d["id"], fiyatlar["AKBNK"], piyasa, makro=makro)
        assert isinstance(seri, pd.Series)
        assert len(seri) == 300
        assert seri.dropna().shape[0] > 0, f"{d['id']} tamamen NaN dondu"


def test_gelecege_bakmama_kurali():
    """t+1 gunundeki fiyat degisikligi t ve oncesindeki ozellik degerini degistirmemeli."""
    fiyatlar, piyasa, makro = _sentetik_veri(100)
    fiyat_orijinal = fiyatlar["AKBNK"].copy()
    fiyat_degismis = fiyatlar["AKBNK"].copy()
    fiyat_degismis.iloc[-1, fiyat_degismis.columns.get_loc("kapanis")] *= 5.0

    for deg_id in ("z_sapma_20", "rsi_14", "bollinger_konum", "hacim_oran"):
        ham1 = ozellik.ham_degisken(deg_id, fiyat_orijinal, piyasa, makro=makro)
        ham2 = ozellik.ham_degisken(deg_id, fiyat_degismis, piyasa, makro=makro)
        pd.testing.assert_series_equal(ham1.iloc[:-1], ham2.iloc[:-1])

        z1 = ozellik.z_skoru(ham1, pencere=60)
        z2 = ozellik.z_skoru(ham2, pencere=60)
        pd.testing.assert_series_equal(z1.iloc[:-1], z2.iloc[:-1])


def test_yuzdelik_sira_araligi():
    s = pd.Series(np.arange(1.0, 101.0))
    ys = ozellik.yuzdelik_sira(s, pencere=50).dropna()
    assert (ys >= 0.0).all() and (ys <= 1.0).all()
    assert ys.iloc[-1] == pytest.approx(1.0)


def test_ozellik_tablosu_multiindex_ve_sutunlar():
    fiyatlar, piyasa, makro = _sentetik_veri(120)
    tablo = ozellik.ozellik_tablosu(fiyatlar=fiyatlar, piyasa=piyasa, makro=makro)
    assert isinstance(tablo.index, pd.MultiIndex)
    assert tablo.index.names == ["tarih", "kod"]
    assert len(tablo.columns) == 24
    assert len(tablo) == 240  # 120 gun x 2 hisse


def test_ileri_getiri_hesabi():
    fiyatlar, _, _ = _sentetik_veri(20)
    getiri = ozellik.ileri_getiri(fiyatlar, ufuk=5)
    assert isinstance(getiri.index, pd.MultiIndex)
    # Son 5 gun gelecek bilinmedigi icin NaN olmali
    assert getiri.xs("AKBNK", level="kod").iloc[-5:].isna().all()
