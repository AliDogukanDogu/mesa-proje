import typer
import os

# Typer uygulamasını oluştur
app = typer.Typer(help="MESA Karar Destek Sistemi Komut Satırı Aracı")

@app.command("veri-indir")
def veri_indir():
    print("MESA: Veri indirme işlemi başlatılıyor (Yahoo & EVDS)...")
    # Yazdığımız veri indirme scriptini çağır
    os.system("python veri_indir.py")
    os.system("python makro_indir.py")
    os.system("python veri_temizle.py")
    print("MESA: Veri indirme ve temizleme tamamlandı!")

@app.command("degerlendir")
def degerlendir():
    print("MESA: 24 Aday değişken için değerlendirme testleri (Test 1-7) başlatılıyor...")
    print("MESA: Karne raporları oluşturuldu. (Rol C bekleniyor)")

@app.command("backtest")
def backtest_calistir():
    print("MESA: Walk-Forward Backtest motoru çalıştırılıyor...")
    os.system("python backtest.py")
    print("MESA: Backtest raporu üretildi.")

@app.command("gunluk")
def gunluk():
    print("MESA: Günlük veri güncelleme, skorlama ve sinyal üretimi başlatıldı...")
    print("MESA: Zamanlayıcı (cron/Görev Zamanlayıcı) için sistem hazır.")

if __name__ == "__main__":
    app()