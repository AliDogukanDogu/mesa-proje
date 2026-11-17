from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

# Veritabanı bağlantısı (mesa.db dosyasını oluşturur)
engine = create_engine('sqlite:///mesa.db', echo=True)
Base = declarative_base()

# 1. Hisse Tablosu
class Hisse(Base):
    __tablename__ = 'hisse'
    id = Column(Integer, primary_key=True)
    kod = Column(String, unique=True, nullable=False)
    sektor = Column(String)

# 2. Fiyat Tablosu
class Fiyat(Base):
    __tablename__ = 'fiyat'
    id = Column(Integer, primary_key=True)
    hisse_kod = Column(String, ForeignKey('hisse.kod'))
    tarih = Column(Date, nullable=False)
    kapanis = Column(Float)
    hacim = Column(Float)

# 3. Değişken Tablosu
class Degisken(Base):
    __tablename__ = 'degisken'
    id = Column(Integer, primary_key=True)
    hisse_kod = Column(String, ForeignKey('hisse.kod'))
    tarih = Column(Date)
    deger = Column(Float)

# 4. Sinyal Tablosu
class Sinyal(Base):
    __tablename__ = 'sinyal'
    id = Column(Integer, primary_key=True)
    hisse_kod = Column(String, ForeignKey('hisse.kod'))
    tarih = Column(Date)
    karar = Column(String) # AL, SAT, BEKLE

# 5. İşlem Tablosu
class Islem(Base):
    __tablename__ = 'islem'
    id = Column(Integer, primary_key=True)
    hisse_kod = Column(String, ForeignKey('hisse.kod'))
    giris_tarihi = Column(Date)
    cikis_tarihi = Column(Date)
    kar_zarar = Column(Float)

# Tabloları veritabanına yaz
Base.metadata.create_all(engine)
print("mesa.db başarıyla oluşturuldu!")