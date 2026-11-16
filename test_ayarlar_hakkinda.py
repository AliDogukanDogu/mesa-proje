"""Ayarlar ve hakkinda sayfasi (Plan gorev D-6) icin birim testleri."""

import importlib.util
from pathlib import Path

def _sayfa_modulunu_yukle():
    """pages/ altindaki ayarlar ve hakkinda modulunu dosya adindan bagimsiz yukler."""
    pages_dizini = Path(__file__).resolve().parent.parent / "pages"
    adaylar = sorted(
        p for p in pages_dizini.glob("*.py")
        if "ayarlar" in p.name.lower() or "hakkinda" in p.name.lower()
    )
    assert adaylar, f"pages/ klasorunde ayarlar dosyasi bulunamadi. Mevcut dosyalar: {[p.name for p in pages_dizini.glob('*.py')]}"
    spec = importlib.util.spec_from_file_location("ayarlar_hakkinda_sayfasi", adaylar[0])
    modul = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(modul)
    return modul

def test_veri_kaynaklari_listesi_yapisi():
    """Veri kaynaklari listesinin bos olmadigini ve gerekli alanlari icerdigini dogrular."""
    modul = _sayfa_modulunu_yukle()
    kaynaklar = modul.veri_kaynaklari_listesi()

    assert len(kaynaklar) >= 2
    for kayit in kaynaklar:
        assert {"Kaynak", "Kapsam", "Güncelleme Sıklığı"}.issubset(kayit.keys())
        assert kayit["Kaynak"].strip() != ""


def test_proje_ekibi_listesi_rolleri():
    """Proje ekibi tablosunda A, B, C ve D sorumlularinin yer aldigini test eder."""
    modul = _sayfa_modulunu_yukle()
    ekip = modul.proje_ekibi_listesi()

    roller = " ".join(k["Rol"] for k in ekip)
    assert "Sorumlu A" in roller
    assert "Sorumlu B" in roller
    assert "Sorumlu C" in roller
    assert "Sorumlu D" in roller


def test_parametre_aciklama_tablosu_olusturma():
    """ayarlar() sozlugundeki parametrelerin deger ve aciklamalariyla tabloya donustugunu dogrular."""
    modul = _sayfa_modulunu_yukle()
    ornek_ayarlar = {
        "esik_al": 0.5,
        "komisyon": 0.001,
        "ozel_parametre": 42,
    }

    df = modul.parametre_aciklama_tablosu(ornek_ayarlar)

    assert list(df.columns) == ["Parametre", "Değer", "Açıklama"]
    assert len(df) == 3
    assert df.loc[0, "Parametre"] == "esik_al"
    assert df.loc[0, "Değer"] == "0.5"
    assert "AL sinyali" in df.loc[0, "Açıklama"]
    assert df.loc[2, "Parametre"] == "ozel_parametre"
