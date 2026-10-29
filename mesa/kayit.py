"""M1 - Degisken kayit defteri. SORUMLU: C (Plan gorev C-2).

Okuma fonksiyonu hazir; dogrulama C'nin.
"""

import yaml

from mesa.ayarlar import CONFIG

ZORUNLU_ALANLAR = ("id", "grup", "kaynak", "hesap", "beklenen_yon", "dalga", "durum")


def degiskenleri_oku() -> list[dict]:
    """config/degiskenler.yaml icindeki kayitlar. Hazir."""
    veri = yaml.safe_load((CONFIG / "degiskenler.yaml").read_text(encoding="utf-8"))
    return veri["degiskenler"]


def dogrula(kayitlar: list[dict]) -> list[dict]:
    """TODO(C): zorunlu alani eksik, id'si tekrarlanan veya beklenen_yon'u gecersiz
    kaydi reddet (ValueError). Gecerli listeyi dondur. (SRS FG-04)
    """
    raise NotImplementedError("C: kayit.dogrula")
