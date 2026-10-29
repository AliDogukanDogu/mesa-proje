"""M6 - Sinyal motoru. SORUMLU: A (Plan gorev A-4).

Formuller Kapsam belgesi "Skorlama, risk ayari ve sinyal kurallari".
Kural sirasi: rejim -> esik -> tuzak -> uyum -> haber.
"""

from datetime import date

import pandas as pd

from mesa.tipler import Sinyal


def degisken_skoru(yuzdelik: float, ic_isareti: int) -> float:
    """s = sign(IC) * (2 * yuzdelik - 1), -1..+1"""
    raise NotImplementedError("A: sinyal.degisken_skoru")


def bilesik_skor(skorlar: dict[str, float], agirliklar: dict[str, float]) -> float:
    """S = toplam(w * s)"""
    raise NotImplementedError("A: sinyal.bilesik_skor")


def risk_ayari(skor: float, sigma20: float, sigma_medyan252: float) -> float:
    """S-sapka = S * (1 - 0,5 * rho), rho = min(1, max(0, sigma20/medyan - 1))"""
    raise NotImplementedError("A: sinyal.risk_ayari")


def rejim_aktif_mi(piyasa: pd.DataFrame, tarih: date) -> bool:
    """VIX > 30 veya son 5 gunde XU100 <= -%5 veya USD/TRY >= +%3."""
    raise NotImplementedError("A: sinyal.rejim_aktif_mi")


def sinyal_uret(kod: str, tarih: date) -> Sinyal:
    """Tek hisse, tek gun: skor, risk, filtreler, 6 sonuctan biri, en buyuk 3 katki."""
    raise NotImplementedError("A: sinyal.sinyal_uret")
