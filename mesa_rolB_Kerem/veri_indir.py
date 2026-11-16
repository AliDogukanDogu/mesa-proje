import time

import pandas as pd
import yfinance as yf
from db import Fiyat, Hisse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Veritabanına bağlan
engine = create_engine('sqlite:///mesa.db')
Session = sessionmaker(bind=engine)
session = Session()

# 20 BIST Hissesi ve Sektörleri
hisseler = {
    "AKBNK.IS": "Bankacılık", "GARAN.IS": "Bankacılık", "ISCTR.IS": "Bankacılık", "YKBNK.IS": "Bankacılık",
    "KCHOL.IS": "Holding", "SAHOL.IS": "Holding", "ARCLK.IS": "Dayanıklı tüketim", "FROTO.IS": "Otomotiv",
    "TOASO.IS": "Otomotiv", "ASELS.IS": "Savunma", "BIMAS.IS": "Perakende", "EREGL.IS": "Demir-çelik",
    "SISE.IS": "Cam", "PETKM.IS": "Petrokimya", "TUPRS.IS": "Rafineri", "THYAO.IS": "Havacılık",
    "PGSUS.IS": "Havacılık", "TCELL.IS": "Telekomünikasyon", "TTKOM.IS": "Telekomünikasyon", "ENKAI.IS": "İnşaat"
}

print("1. Hisseler veritabanına ekleniyor...")
for kod, sektor in hisseler.items():
    # Hisse zaten var mı kontrol et
    mevcut_hisse = session.query(Hisse).filter_by(kod=kod).first()
    if not mevcut_hisse:
        yeni_hisse = Hisse(kod=kod, sektor=sektor)
        session.add(yeni_hisse)
session.commit()

print("2. Yahoo Finance'ten fiyat verileri indiriliyor (2014'ten bugüne)...")
for kod in hisseler.keys():
    print(f"{kod} indiriliyor...")
    time.sleep(2)
    veri = yf.download(kod, start="2014-01-02")
    
    # Verileri veritabanına uygun formata getir ve kaydet
    for tarih, satir in veri.iterrows():
        # Fiyat zaten var mı kontrol et (artımlı güncelleme için)
        mevcut_fiyat = session.query(Fiyat).filter_by(hisse_kod=kod, tarih=tarih.date()).first()
        if not mevcut_fiyat:
            yeni_fiyat = Fiyat(
                hisse_kod=kod,
                tarih=tarih.date(),
                kapanis=float(satir['Close'].iloc[0]) if isinstance(satir['Close'], pd.Series) else float(satir['Close']),
                hacim=float(satir['Volume'].iloc[0]) if isinstance(satir['Volume'], pd.Series) else float(satir['Volume'])
            )
            session.add(yeni_fiyat)
    session.commit()

print("İşlem tamamlandı! Bütün fiyatlar veritabanına yazıldı.")  
