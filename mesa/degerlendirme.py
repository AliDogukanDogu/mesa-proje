"""M4 - Degerlendirme motoru: 7 test. SORUMLU: C (Test 1-6, karne), A (Test 7).

Esikler config/ayarlar.yaml -> degerlendirme. Yontemler Kapsam belgesindeki test tablosunda.
"""

import pandas as pd

from mesa.tipler import Karne


def test1_ic(ozellik: pd.Series, getiri: pd.Series) -> float:
    """TODO(C): havuzlanmis Spearman IC."""
    raise NotImplementedError("C: test1_ic")


def test2_anlamlilik(ozellikler: pd.DataFrame, getiri: pd.Series) -> dict[str, float]:
    """TODO(C): 20 gunluk blok permutasyon (5.000) + Benjamini-Hochberg. Donus: {degisken: q}."""
    raise NotImplementedError("C: test2_anlamlilik")


def test3_istikrar(ozellik: pd.Series, getiri: pd.Series) -> tuple[float, float]:
    """TODO(C): 6 aylik pencerelerde IC listesi. Donus: (ort/std, isaret tutarliligi)."""
    raise NotImplementedError("C: test3_istikrar")


def test4_bozunma(ozellik: pd.Series, fiyatlar: dict) -> dict[int, float]:
    """TODO(C): ufuk 1, 5, 10, 20, 60 icin IC."""
    raise NotImplementedError("C: test4_bozunma")


def test5_rejim(ozellik: pd.Series, getiri: pd.Series, rejim: pd.Series) -> dict[str, float]:
    """TODO(C): VIX <20 / 20-30 / >30 ve boga/ayi/yatay rejimlerinde ayri IC."""
    raise NotImplementedError("C: test5_rejim")


def test6_tekrar(ozellikler: pd.DataFrame, aktifler: list[str]) -> dict[str, str | None]:
    """TODO(C): |korelasyon| > 0,8 olan ciftleri bul. Donus: {degisken: tekrar ettigi ya da None}."""
    raise NotImplementedError("C: test6_tekrar")


def test7_marjinal_katki(aday: str, mevcut: list[str]) -> tuple[float, tuple[float, float]]:
    """TODO(A): walk-forward mevcut model vs model+aday; blok bootstrap %95 GA.
    Donus: (Sharpe farki, (alt, ust)).
    """
    raise NotImplementedError("A: test7_marjinal_katki")


def karneleri_uret() -> list[Karne]:
    """TODO(C): her aday icin 7 testi calistirip Karne listesi dondur (karar = A'nin fonksiyonu)."""
    raise NotImplementedError("C: karneleri_uret")
