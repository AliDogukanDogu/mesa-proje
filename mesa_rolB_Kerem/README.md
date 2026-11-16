# MESA: Çok Varlıklı Al/Sat Sinyal Asistanı (BIST Pilot)

Bu proje, Borsa İstanbul'daki 20 hisse için günlük AL/SAT/BEKLE sinyali üreten bir karar destek yazılımıdır.

## Kurulum Adımları (Süre: < 15 dk)

1. Proje klasörünü bilgisayarınıza indirin ve terminalde (PowerShell) bu klasörü açın.
2. Bu komutlar ile sanal ortam oluşturun ve aktif edin :
   python -m venv .venv
   .venv\Scripts\activate
3. Gerekli kütüphaneleri bu komutla kurun:
   pip install -r requirements.txt
4. Veritabanını oluşturmak ve geçmiş verileri indirmek için bu komutları kullanın:
   python db.py
   python cli.py veri-indir
5. Backtest motorunu çalıştırmak için bu komutu kullanın:
   python cli.py backtest
6. Otomatik birim testlerini doğrulamak için bu komutu kullanın:
   pytest -v
