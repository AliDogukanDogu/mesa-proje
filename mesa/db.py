"""M2 - SQLite veritabani. SORUMLU: B (Plan gorev B-1, B-2).

Tablolar SRS bolum 5.4'te: hisse, fiyat, makro, degisken, ozellik, karne,
sinyal, backtest_calisma, islem, kalite. SQLAlchemy 2 ile modelleri yaz.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def veritabani_yolu() -> Path:
    return Path(os.getenv("MESA_DB", "data/mesa.db"))


def baglanti() -> Engine:
    """SQLite motoru dondurur; klasor yoksa olusturur. Hazir."""
    yol = veritabani_yolu()
    yol.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{yol}")


def tablolari_olustur() -> None:
    """TODO(B): SRS 5.4'teki 10 tabloyu olustur. Bitti: calisinca mesa.db olusur."""
    raise NotImplementedError("B: db.tablolari_olustur")
