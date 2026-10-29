"""M2 - Veri katmani. SORUMLU: B (Plan gorev B-3, B-4, B-5).

Kurallar (Kapsam belgesi "Varlik evreni ve veri kaynaklari", SRS FG-01..03):
- Yahoo kodu: hisse kodu + ".IS"; piyasa serileri config/hisseler.yaml'da.
- Bosluklar yalniz ILERIYE dogru doldurulur (ffill). Geriye doldurma YASAK.
- Makro veri yayin_tarihi'nden once kullanilamaz.
"""

from datetime import date

import pandas as pd


def fiyat_indir(yahoo_kodu: str, baslangic: date, bitis: date | None = None) -> pd.DataFrame:
    """TODO(B): yfinance ile gunluk OHLCV indir.

    Donus: index=tarih, sutunlar = acilis, yuksek, dusuk, kapanis, hacim (duzeltilmis fiyat).
    """
    raise NotImplementedError("B: veri.fiyat_indir")


def hepsini_guncelle(baslangic: date) -> None:
    """TODO(B): 20 hisse + 8 seriyi indir; veritabaninda olan son gunden sonrasini ekle."""
    raise NotImplementedError("B: veri.hepsini_guncelle")


def temizle(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """TODO(B): tekrarlari sil, ffill uygula, sifir hacim ve |z|>6 degerleri isaretle.

    Donus: (temiz tablo, sorun listesi [{'tarih':..., 'sorun_turu':...}])
    """
    raise NotImplementedError("B: veri.temizle")


def kalite_raporu() -> pd.DataFrame:
    """TODO(B): seri basina eksik gun orani, aykiri sayisi, son tarih, askida mi?

    Bitti olcutu: her seride eksik gun < %2 (B1).
    """
    raise NotImplementedError("B: veri.kalite_raporu")


def fiyat_oku(kod: str) -> pd.DataFrame:
    """TODO(B): veritabanindan bir hissenin/serinin fiyat tablosunu oku."""
    raise NotImplementedError("B: veri.fiyat_oku")


def makro_oku(seri: str, bugun: date) -> pd.Series:
    """TODO(B, Should): EVDS'den (yedek: CSV) gelen seri; yalniz yayin_tarihi <= bugun olanlar."""
    raise NotImplementedError("B: veri.makro_oku")
