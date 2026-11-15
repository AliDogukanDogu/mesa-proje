"""M1 - Degisken kayit defteri. SORUMLU: C (Plan gorev C-2).

Okuma ve dogrulama fonksiyonlari.
"""

import yaml
from mesa.ayarlar import CONFIG

ZORUNLU_ALANLAR = ("id", "grup", "kaynak", "hesap", "beklenen_yon", "dalga", "durum")
GECERLI_YONLER = ("negatif", "pozitif", "belirsiz")
GECERLI_DURUMLAR = ("aday", "aktif", "izleme", "emekli")


def degiskenleri_oku() -> list[dict]:
    """config/degiskenler.yaml icindeki kayitlar. Hazir."""
    veri = yaml.safe_load((CONFIG / "degiskenler.yaml").read_text(encoding="utf-8"))
    return veri["degiskenler"]


def dogrula(kayitlar: list[dict]) -> list[dict]:
    """Zorunlu alani eksik, id'si tekrarlanan veya beklenen_yon'u gecersiz
    kaydi reddet (ValueError). Gecerli listeyi dondur. (SRS FG-04)
    """
    if not kayitlar:
        raise ValueError("Degisken kayit listesi bos olamaz.")

    gorulen_idler: set[str] = set()
    gecerli_kayitlar: list[dict] = []

    for indeks, kayit in enumerate(kayitlar):
        if not isinstance(kayit, dict):
            raise ValueError(f"Kayit #{indeks} sozluk (dict) tipinde olmalidir.")

        eksik_alanlar = [
            alan for alan in ZORUNLU_ALANLAR if alan not in kayit or kayit[alan] is None or kayit[alan] == ""
        ]
        if eksik_alanlar:
            kimlik = kayit.get("id", f"indeks_{indeks}")
            raise ValueError(f"'{kimlik}' kaydinda zorunlu alanlar eksik: {eksik_alanlar}")

        degisken_id = str(kayit["id"]).strip()
        if degisken_id in gorulen_idler:
            raise ValueError(f"Tekrarlanan degisken id tespit edildi: '{degisken_id}'")
        gorulen_idler.add(degisken_id)

        beklenen_yon = str(kayit["beklenen_yon"]).strip()
        if beklenen_yon not in GECERLI_YONLER:
            raise ValueError(
                f"'{degisken_id}' icin gecersiz beklenen_yon: '{beklenen_yon}'. "
                f"Gecerli degerler: {GECERLI_YONLER}"
            )

        durum = str(kayit["durum"]).strip()
        if durum not in GECERLI_DURUMLAR:
            raise ValueError(
                f"'{degisken_id}' icin gecersiz durum: '{durum}'. "
                f"Gecerli degerler: {GECERLI_DURUMLAR}"
            )

        gecerli_kayitlar.append(kayit)

    return gecerli_kayitlar