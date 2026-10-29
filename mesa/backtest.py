"""M7 - Walk-forward backtest. SORUMLU: B (motor, gorev B-6), A (metrikler, hold-out).

Kurallar (Kapsam belgesi "Degerlendirme motoru ve walk-forward backtest"):
- Egitim 3 yil, test 6 ay, 6 ay kaydirma.
- Sinyal ertesi gunun ACILIS fiyatiyla islenir.
- Cikis: SAT, S<=0, zarar-kes (2 x ATR) veya 20 islem gunu.
- Islem basi risk %1; toplam maruziyet <= %100; aciga satis yok.
- Maliyet yon basina %0,2. Bostaki nakit politika faizi kadar kazanir.
"""

import pandas as pd

from mesa.tipler import Islem, Metrikler


def pencereler(baslangic: str, bitis: str) -> list[tuple[str, str, str, str]]:
    """TODO(B): (egitim_bas, egitim_bit, test_bas, test_bit) listesi. En az 17 pencere."""
    raise NotImplementedError("B: backtest.pencereler")


def islemleri_simule_et(sinyaller: pd.DataFrame, fiyatlar: dict[str, pd.DataFrame]) -> list[Islem]:
    """TODO(B): sinyallere gore al-sat yapilmis gibi hesapla; her islemi kaydet."""
    raise NotImplementedError("B: backtest.islemleri_simule_et")


def ozsermaye_egrisi(islemler: list[Islem], baslangic_sermaye: float = 100_000) -> pd.Series:
    """TODO(B): gunluk ozsermaye serisi."""
    raise NotImplementedError("B: backtest.ozsermaye_egrisi")


def metrikleri_hesapla(egri: pd.Series, islemler: list[Islem], risksiz: pd.Series) -> Metrikler:
    """TODO(A): isabet, kar faktoru, Sharpe (risksize gore), max dusus, islem sayisi."""
    raise NotImplementedError("A: backtest.metrikleri_hesapla")


def rastgele_kiyas(sinyaller: pd.DataFrame, n: int = 1000) -> list[float]:
    """TODO(A): sinyalleri karistirip n kez backtest; Sharpe dagilimini dondur."""
    raise NotImplementedError("A: backtest.rastgele_kiyas")


def holdout_calistir() -> Metrikler:
    """TODO(A): hold-out donemini YALNIZ BIR KEZ calistir; ikinci denemede uyar ve kaydet."""
    raise NotImplementedError("A: backtest.holdout_calistir")
