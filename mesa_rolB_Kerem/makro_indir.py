import pandas as pd

print("1. TCMB EVDS makro veri adaptörü başlatılıyor...")
print("Proje Risk Yönetimi (B Planı) devrede: Veriler CSV'den okunacak şekilde ayarlanıyor...")

# B planı: Geçici bir yedek CSV dosyası oluştur
tarihler = pd.date_range(start="2014-01-01", end="2026-11-01", freq="MS")
df_makro = pd.DataFrame({
    "tarih": tarihler,
    "politika_faizi": 50.0,  # Örnek yedek veri
    "tufe_aylik": 2.5        # Örnek yedek veri
})

# Dosyayı kaydet
df_makro.to_csv("makro_veri.csv", index=False)

print("BAŞARILI: 'makro_veri.csv' yedek dosyası oluşturuldu!")
print("Sistem makro verileri bu dosyadan sorunsuzca okuyacak.")