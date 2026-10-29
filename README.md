# MESA — Çok Varlıklı Al/Sat Sinyal Asistanı (BIST pilotu)

> Bu bir yatırım tavsiyesi değildir. MESA yalnız eğitim amaçlı bir karar destek aracıdır.

## Kurulum (≈15 dk)

```bash
git clone <depo-adresi> mesa && cd mesa
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env          # EVDS anahtarını yaz (isteğe bağlı)
```

## Kullanım

```bash
mesa veri-indir --baslangic 2014-01-02   # geçmiş veriyi indirir (bir kez)
mesa degerlendir                         # karneler ve ağırlıklar
mesa backtest                            # walk-forward raporu
mesa gunluk                              # her akşam: yeni gün + sinyaller
streamlit run app.py                     # arayüz
pytest                                   # testler
```

## Klasörler

| Klasör / dosya | Ne var | Sahibi |
| --- | --- | --- |
| `config/` | hisse listesi, değişken listesi, parametreler | C, A |
| `mesa/veri.py` | indirme, temizleme, kalite raporu | B |
| `mesa/db.py` | SQLite tabloları | B |
| `mesa/kayit.py` | değişken kayıt defteri | C |
| `mesa/ozellik.py` | değişken hesapları | C |
| `mesa/degerlendirme.py` | 7 test, karne | C (Test 1–6), A (Test 7) |
| `mesa/agirlik.py` | karar matrisi ve ağırlıklar | A, C |
| `mesa/sinyal.py` | skor, risk ayarı, filtre, sonuç | A |
| `mesa/backtest.py` | walk-forward, metrikler | B, A |
| `mesa/servis.py` | arayüzün çağırdığı fonksiyonlar | A |
| `mesa/cli.py` | `mesa` komutları | B |
| `app.py`, `pages/` | Streamlit sayfaları | D |
| `tests/` | testler | herkes |

## Nereden başlarım?

1. Proje Planı'nda kendi harfinin altındaki ilk işi bul.
2. Yukarıdaki tablodan dosyanı aç. İçinde `TODO(<harfin>)` yazan fonksiyonlar senin.
3. Fonksiyonun açıklamasını (docstring) ve Kapsam belgesindeki ilgili bölümü yapay zekâya ver:
   "Bu fonksiyonu yaz ve tests/ klasörüne 3 testini ekle."
4. `pytest` yeşilse yeni bir dal aç, GitHub'a yükle, Pull Request aç.

**Kural:** Fonksiyon adlarını ve parametrelerini değiştirme. Başkaları onlara göre kod yazıyor.
Değiştirmen gerekiyorsa gruba önce yaz.
