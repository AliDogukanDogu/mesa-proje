"""M1 Degisken kayit defteri birim testleri. SORUMLU: C."""

import copy
import pytest
from mesa import kayit


def test_24_degisken_okunur_ve_dogrulanir():
    kayitlar = kayit.degiskenleri_oku()
    assert len(kayitlar) == 24
    dogrulanmis = kayit.dogrula(kayitlar)
    assert len(dogrulanmis) == 24
    assert any(k["id"] == "rastgele_kontrol" for k in dogrulanmis)


def test_eksik_zorunlu_alan_reddedilir():
    ornek = copy.deepcopy(kayit.degiskenleri_oku()[:1])
    del ornek[0]["hesap"]
    with pytest.raises(ValueError, match="zorunlu alanlar eksik"):
        kayit.dogrula(ornek)


def test_tekrarlanan_id_reddedilir():
    ornek = copy.deepcopy(kayit.degiskenleri_oku()[:1])
    tekrar = copy.deepcopy(ornek[0])
    with pytest.raises(ValueError, match="Tekrarlanan degisken id"):
        kayit.dogrula([ornek[0], tekrar])


def test_gecersiz_beklenen_yon_reddedilir():
    ornek = copy.deepcopy(kayit.degiskenleri_oku()[:1])
    ornek[0]["beklenen_yon"] = "yukari_yonlu"
    with pytest.raises(ValueError, match="gecersiz beklenen_yon"):
        kayit.dogrula(ornek)


def test_gecersiz_durum_reddedilir():
    ornek = copy.deepcopy(kayit.degiskenleri_oku()[:1])
    ornek[0]["durum"] = "bilinmeyen_durum"
    with pytest.raises(ValueError, match="gecersiz durum"):
        kayit.dogrula(ornek)
