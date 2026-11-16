import pandas as pd
from sqlalchemy import create_engine

# Veritabanına bağlan
engine = create_engine('sqlite:///mesa.db')

print("1. Veritabanından fiyat verileri okunuyor...")
df = pd.read_sql("SELECT * FROM fiyat", engine)

if df.empty:
    print("Hata: Veritabanında henüz hiç fiyat verisi yok! (Yahoo Finance engeli)")
else:
    toplam_satir = len(df)
    eksik_kapanis = df['kapanis'].isnull().sum()
    
    print("\n--- Veri Kalite Raporu ---")
    print(f"Toplam Kayıt: {toplam_satir}")
    print(f"Kapanış Fiyatı Eksik Kayıt Sayısı: {eksik_kapanis}")
    
    # Eksik gün oranı (Proje hedefi: %2'den az olmalı)
    eksik_oran = (eksik_kapanis / toplam_satir) * 100 if toplam_satir > 0 else 100
    print(f"Eksik Gün Oranı: %{eksik_oran:.2f} (Hedef: <%2)")
    
    if eksik_oran < 2.0:
        print("Durum: BAŞARILI (Eksik gün hedefi sağlandı)")
    else:
        print("Durum: BAŞARISIZ (Veri kalitesi yetersiz)")

    print("\n2. Eksik veriler ileriye dönük (forward-fill) dolduruluyor...")
    # Verileri hisse koduna ve tarihe göre sıralayıp eksikleri bir önceki günün fiyatıyla doldur
    df = df.sort_values(by=['hisse_kod', 'tarih'])
    df['kapanis'] = df.groupby('hisse_kod')['kapanis'].ffill()
    df['hacim'] = df.groupby('hisse_kod')['hacim'].ffill()
    
    print("Temizleme işlemi tamamlandı! Veriler analize hazır.")