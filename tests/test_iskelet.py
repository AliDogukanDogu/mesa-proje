"""Iskeletin calistigini dogrulayan testler. Hazir.

Kendi testlerini ayri dosyalara yaz: test_veri.py (B), test_ozellik.py (C), test_sinyal.py (A) ...
"""

import importlib

import pytest

from mesa import ayarlar, kayit, servis
from mesa.tipler import Sonuc

MODULLER = ["db", "veri", "kayit", "ozellik", "degerlendirme", "agirlik", "sinyal", "backtest",
            "servis", "cli"]


@pytest.mark.parametrize("ad", MODULLER)
def test_moduller_yuklenir(ad):
    importlib.import_module(f"mesa.{ad}")


def test_20_hisse_var():
    assert len(ayarlar.hisse_kodlari()) == 20


def test_8_piyasa_serisi_var():
    assert len(ayarlar.hisseler()["piyasa_serileri"]) == 8


def test_degisken_kayitlarinda_zorunlu_alanlar_var():
    for k in kayit.degiskenleri_oku():
        assert all(alan in k for alan in kayit.ZORUNLU_ALANLAR), k["id"]


def test_ornek_servis_20_sinyal_dondurur():
    sinyaller = servis.gunun_sinyalleri()
    assert len(sinyaller) == 20
    assert all(isinstance(s.sonuc, Sonuc) for s in sinyaller)
