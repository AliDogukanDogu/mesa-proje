"""M5 - Karar matrisi (A) ve agirliklar (C)."""

from mesa.tipler import Karar, Karne


def karar_ver(karne: Karne) -> Karar:
    """TODO(A): karar matrisi.
    AKTIF: 7 test gecti | KOSULLU: yalniz bir rejimde | IZLEME: anlamli ama istikrarsiz
    veya 0,01 <= q < 0,05 | RED: q >= 0,05 veya marjinal katki <= 0 |
    INCELEME: beklenen yonle ters.
    """
    raise NotImplementedError("A: agirlik.karar_ver")


def agirliklari_hesapla(karneler: list[Karne], onceki: dict[str, float] | None = None) -> dict[str, float]:
    """TODO(C): AKTIF/KOSULLU degiskenlere |IC| x istikrar ile agirlik.
    Sinirlar: tek degisken <= %15, tek grup <= %35. Yumusatma: 0,7 x yeni + 0,3 x onceki.
    Toplam = 1.
    """
    raise NotImplementedError("C: agirlik.agirliklari_hesapla")
