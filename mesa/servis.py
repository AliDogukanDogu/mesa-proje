"""Servis katmani: arayuzun ve komut satirinin cagirdigi TEK giris noktasi. SORUMLU: A.

D (arayuz) yalniz bu dosyadaki fonksiyonlari kullanir.
Gercek motorlar hazir olana kadar ornek_* fonksiyonlari sahte veri dondurur;
boylece arayuz Gun 6'dan itibaren bagimsiz gelistirilebilir.
"""

from datetime import timedelta

import numpy as np
import pandas as pd

from mesa.ayarlar import bugun, hisse_kodlari
from mesa.tipler import Karar, Karne, Metrikler, Sinyal, Sonuc

ORNEK_MOD = True  # Gun 9'da A gercek motorlara baglayinca False olur.


# ---------- Arayuzun kullandigi fonksiyonlar ----------

def gunun_sinyalleri() -> list[Sinyal]:
    """Pano sayfasi: 20 hissenin bugunku sinyali."""
    return _ornek_sinyaller() if ORNEK_MOD else _gercek_sinyaller()


def hisse_gecmisi(kod: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Hisse detayi: (fiyat tablosu, gecmis sinyaller tablosu)."""
    return _ornek_gecmis(kod) if ORNEK_MOD else _gercek_gecmis(kod)


def karneler() -> list[Karne]:
    """Karne sayfasi."""
    return _ornek_karneler() if ORNEK_MOD else _gercek_karneler()


def backtest_ozeti() -> tuple[pd.Series, Metrikler]:
    """Backtest sayfasi: (ozsermaye egrisi, metrikler)."""
    return _ornek_backtest() if ORNEK_MOD else _gercek_backtest()


# ---------- Komut satirinin kullandigi fonksiyonlar ----------

def degerlendirmeyi_calistir() -> None:
    raise NotImplementedError("A: servis.degerlendirmeyi_calistir (Gun 9)")


def backtesti_calistir(holdout: bool = False) -> None:
    raise NotImplementedError("A: servis.backtesti_calistir (Gun 9)")


def gunluk_calistir() -> None:
    raise NotImplementedError("A: servis.gunluk_calistir (Gun 9)")


# ---------- Gercek baglantilar (A, Gun 9) ----------

def _gercek_sinyaller() -> list[Sinyal]:
    raise NotImplementedError


def _gercek_gecmis(kod: str):
    raise NotImplementedError


def _gercek_karneler() -> list[Karne]:
    raise NotImplementedError


def _gercek_backtest():
    raise NotImplementedError


# ---------- Ornek (sahte) veri: yalniz gelistirme icin ----------

_rng = np.random.default_rng(42)


def _ornek_sinyaller() -> list[Sinyal]:
    tarih = bugun()
    sonuclar = [Sonuc.GUCLU_AL, Sonuc.TEMKINLI_AL, Sonuc.BEKLE, Sonuc.BEKLE, Sonuc.SAT, Sonuc.TUZAK]
    sinyaller = []
    for i, kod in enumerate(hisse_kodlari()):
        s = float(_rng.uniform(-1, 1))
        sinyaller.append(Sinyal(
            kod=kod, tarih=tarih, skor=s, ayarli_skor=s * 0.8,
            sonuc=sonuclar[i % len(sonuclar)],
            katkilar=[("z_sapma_20", 0.21), ("rsi_14", 0.12), ("vix_5g", -0.05)],
        ))
    return sinyaller


def _ornek_gecmis(kod: str):
    gunler = pd.bdate_range(end=bugun(), periods=250)
    kapanis = 100 * np.exp(np.cumsum(_rng.normal(0, 0.02, len(gunler))))
    fiyat = pd.DataFrame({"kapanis": kapanis}, index=gunler)
    secilen = gunler[::25]
    gecmis = pd.DataFrame({
        "tarih": secilen,
        "sonuc": [Sonuc.GUCLU_AL.value if i % 2 == 0 else Sonuc.SAT.value for i in range(len(secilen))],
    })
    return fiyat, gecmis


def _ornek_karneler() -> list[Karne]:
    return [
        Karne("z_sapma_20", ic=-0.06, q_degeri=0.004, istikrar=0.9, isaret_tutarlilik=0.8,
              karar=Karar.AKTIF, agirlik=0.15),
        Karne("rsi_14", ic=-0.04, q_degeri=0.008, istikrar=0.6, isaret_tutarlilik=0.7,
              karar=Karar.AKTIF, agirlik=0.10),
        Karne("rastgele_kontrol", ic=0.002, q_degeri=0.81, istikrar=0.1, isaret_tutarlilik=0.5,
              karar=Karar.RED, agirlik=0.0),
    ]


def _ornek_backtest():
    gunler = pd.bdate_range(end=bugun() - timedelta(days=365), periods=1500)
    egri = pd.Series(100_000 * np.exp(np.cumsum(_rng.normal(0.0003, 0.01, len(gunler)))), index=gunler)
    return egri, Metrikler(isabet_orani=0.54, kar_faktoru=1.35, sharpe=0.8, max_dusus=-0.12,
                           islem_sayisi=240)
