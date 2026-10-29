"""Moduller arasinda tasinan ortak veri tipleri. Hazir - degistirmeden once gruba yaz.

Tablo verisi icin ortak bicim (pandas DataFrame):
- Fiyat:   index = tarih, sutunlar = acilis, yuksek, dusuk, kapanis, hacim
- Ozellik: MultiIndex (tarih, kod), sutunlar = degisken id'leri, degerler = z-skoru
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Karar(str, Enum):
    AKTIF = "AKTIF"
    KOSULLU = "KOSULLU"
    IZLEME = "IZLEME"
    RED = "RED"
    INCELEME = "INCELEME"


class Sonuc(str, Enum):
    GUCLU_AL = "Güçlü AL"
    TEMKINLI_AL = "Temkinli AL"
    BEKLE = "BEKLE"
    TUZAK = "Tuzak uyarısı"
    SAT = "SAT / azalt"
    DEVRE_DISI = "Sistem devre dışı"


@dataclass
class Karne:
    """Bir degiskenin 7 test sonucu."""

    degisken_id: str
    ic: float = 0.0                 # Test 1
    q_degeri: float = 1.0           # Test 2 (FDR duzeltmeli)
    istikrar: float = 0.0           # Test 3: ort/std
    isaret_tutarlilik: float = 0.0  # Test 3
    en_iyi_ufuk: int = 5            # Test 4
    rejim_ic: dict[str, float] = field(default_factory=dict)  # Test 5
    tekrar_ile: str | None = None   # Test 6: yuksek korelasyonlu oldugu degisken
    marjinal_sharpe_farki: float = 0.0          # Test 7
    marjinal_guven_araligi: tuple[float, float] = (0.0, 0.0)  # Test 7, %95
    karar: Karar = Karar.RED
    agirlik: float = 0.0


@dataclass
class Sinyal:
    """Bir hissenin bir gunluk sinyali."""

    kod: str
    tarih: date
    skor: float              # S
    ayarli_skor: float       # S-sapka
    sonuc: Sonuc
    katkilar: list[tuple[str, float]] = field(default_factory=list)  # en buyuk 3 (degisken, katki)


@dataclass
class Islem:
    kod: str
    giris_tarihi: date
    giris_fiyati: float
    cikis_tarihi: date
    cikis_fiyati: float
    getiri: float            # maliyet sonrasi
    cikis_nedeni: str        # SAT | skor<=0 | zarar-kes | sure


@dataclass
class Metrikler:
    isabet_orani: float
    kar_faktoru: float
    sharpe: float
    max_dusus: float
    islem_sayisi: int
