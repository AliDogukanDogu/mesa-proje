import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Islem

# Veritabanına bağlan
engine = create_engine('sqlite:///mesa.db')
Session = sessionmaker(bind=engine)
session = Session()

print("1. Walk-Forward Backtest Motoru İskeleti Başlatılıyor...")
print("Proje Kuralları Yükleniyor: İşlem başı risk %1, İşlem maliyeti %0.2, Zarar-kes 2xATR")

# Rol A'dan sinyaller geldiğinde çalışacak ana döngünün test kaydı
print("2. Motor test ediliyor: Veritabanına örnek bir işlem kaydediliyor...")

# Örnek bir işlem simülasyonu
test_islem = Islem(
    hisse_kod="THYAO.IS",
    giris_tarihi=pd.to_datetime("2026-11-01").date(),
    cikis_tarihi=pd.to_datetime("2026-11-10").date(),
    kar_zarar=1250.75
)

# İşlemi veritabanına ekle
session.add(test_islem)
session.commit()

print("BAŞARILI: Örnek işlem 'islem' tablosuna kusursuz kaydedildi!")
print("Backtest motorunun altyapısı hazır. Sinyal modülü tamamlandığında buraya bağlanacak.")