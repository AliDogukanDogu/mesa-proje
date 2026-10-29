"""M3 - Ozellik uretici. SORUMLU: C (Plan gorev C-3).

Her degisken once ham olarak hesaplanir, sonra z-skoruna ve
son 252 gune gore yuzdelik siraya cevrilir. Formuller Kapsam belgesindeki
"Degisken seti" tablosunda.

KURAL: t gunundeki deger yalniz t ve onceki gunlerin verisiyle hesaplanir.
"""

import pandas as pd


def ham_degisken(degisken_id: str, fiyat: pd.DataFrame, piyasa: dict[str, pd.DataFrame]) -> pd.Series:
    """TODO(C): bir hisse icin degiskenin ham degeri (z_sapma_20, rsi_14, bollinger_konum ...)."""
    raise NotImplementedError("C: ozellik.ham_degisken")


def z_skoru(seri: pd.Series, pencere: int = 252) -> pd.Series:
    """TODO(C): kayan pencerede (seri - ortalama) / std."""
    raise NotImplementedError("C: ozellik.z_skoru")


def yuzdelik_sira(seri: pd.Series, pencere: int = 252) -> pd.Series:
    """TODO(C): son `pencere` gun icindeki yuzdelik sira, 0..1."""
    raise NotImplementedError("C: ozellik.yuzdelik_sira")


def ozellik_tablosu() -> pd.DataFrame:
    """TODO(C): tum hisseler ve adaylar icin tablo.
    Donus: MultiIndex (tarih, kod), sutunlar = degisken id, degerler = z-skoru.
    """
    raise NotImplementedError("C: ozellik.ozellik_tablosu")


def ileri_getiri(fiyatlar: dict[str, pd.DataFrame], ufuk: int = 5) -> pd.Series:
    """TODO(C): r = P(t+ufuk)/P(t) - 1, MultiIndex (tarih, kod). Yalniz test hesaplarinda kullanilir."""
    raise NotImplementedError("C: ozellik.ileri_getiri")
