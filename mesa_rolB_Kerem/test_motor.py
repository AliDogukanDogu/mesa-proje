import os
import sqlite3


def test_veritabani_olustu_mu():
    """Test 1: mesa.db dosyasının başarıyla oluşturulduğunu kontrol eder."""
    assert os.path.exists("mesa.db") == True

def test_makro_csv_olustu_mu():
    """Test 2: B planı olan makro_veri.csv dosyasının varlığını kontrol eder."""
    assert os.path.exists("makro_veri.csv") == True

def test_veritabani_tablolari():
    """Test 3: SQLite veritabanına bağlanıp tabloların varlığını teyit eder."""
    baglanti = sqlite3.connect("mesa.db")
    imlec = baglanti.cursor()
    imlec.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablolar = [tablo[0] for tablo in imlec.fetchall()]
    baglanti.close()
    
    # Aradığımız tabloların veritabanında olup olmadığını doğrula
    assert "hisse" in tablolar
    assert "fiyat" in tablolar
    assert "islem" in tablolar
