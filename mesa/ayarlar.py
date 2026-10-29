"""Config dosyalarini okur. Hazir - degistirme."""

from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

KOK = Path(__file__).resolve().parent.parent
CONFIG = KOK / "config"
ISTANBUL = ZoneInfo("Europe/Istanbul")


def bugun() -> date:
    """Istanbul saatine gore bugunun tarihi. date.today() yerine bunu kullan."""
    return datetime.now(tz=ISTANBUL).date()


@lru_cache
def ayarlar() -> dict:
    """config/ayarlar.yaml icerigi."""
    return yaml.safe_load((CONFIG / "ayarlar.yaml").read_text(encoding="utf-8"))


@lru_cache
def hisseler() -> dict:
    """config/hisseler.yaml icerigi: hisseler, yedekler, piyasa_serileri."""
    return yaml.safe_load((CONFIG / "hisseler.yaml").read_text(encoding="utf-8"))


def hisse_kodlari() -> list[str]:
    """20 hissenin kodu, ornek: ['AKBNK', 'GARAN', ...]."""
    return [h["kod"] for h in hisseler()["hisseler"]]
