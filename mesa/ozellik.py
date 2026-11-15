"""M3 - Ozellik uretici. SORUMLU: C (Plan gorev C-3).

Her degisken once ham olarak hesaplanir, sonra z-skoruna ve
son 252 gune gore yuzdelik siraya cevrilir.

KURAL: t gunundeki deger yalniz t ve onceki gunlerin verisiyle hesaplanir.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from mesa import ayarlar, kayit, veri

# Resmi dini/milli tatil ve bayram donemleri icin yaklasik takvim yardimcisi
_SABIT_TATILLER = {(1, 1), (4, 23), (5, 1), (5, 19), (7, 15), (8, 30), (10, 29)}


def _piyasa_kapanis(piyasa: dict[str, pd.DataFrame], anahtar: str, indeks: pd.Index) -> pd.Series:
    """Piyasa sozlugunden ilgili serinin kapanis sutununu hisse indeksine hizalar (yalniz ffill)."""
    df = piyasa.get(anahtar)
    if df is None or df.empty or "kapanis" not in df.columns:
        return pd.Series(np.nan, index=indeks, dtype=float)
    seri = df["kapanis"].astype(float)
    return seri.reindex(indeks, method="ffill")


def _rsi_hesapla(kapanis: pd.Series, periyot: int = 14) -> pd.Series:
    """Wilder usulu RSI(14), gelecege bakmadan hesaplanir."""
    fark = kapanis.diff()
    kazanc = fark.clip(lower=0.0)
    kayip = (-fark).clip(lower=0.0)
    ort_kazanc = kazanc.ewm(alpha=1.0 / periyot, min_periods=periyot, adjust=False).mean()
    ort_kayip = kayip.ewm(alpha=1.0 / periyot, min_periods=periyot, adjust=False).mean()
    rs = ort_kazanc / ort_kayip.replace(0.0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.where(ort_kayip != 0.0, 100.0)


def ham_degisken(
    degisken_id: str,
    fiyat: pd.DataFrame,
    piyasa: dict[str, pd.DataFrame],
    makro: dict[str, pd.Series] | None = None,
    haber: pd.Series | None = None,
) -> pd.Series:
    """Bir hisse icin secilen degiskenin ham degerini hesaplar.

    t gunundeki deger yalniz t ve onceki gunlerin verisiyle hesaplanir.
    """
    if fiyat.empty or "kapanis" not in fiyat.columns:
        return pd.Series(dtype=float)

    indeks = fiyat.index
    kapanis = fiyat["kapanis"].astype(float)
    hacim = fiyat["hacim"].astype(float) if "hacim" in fiyat.columns else pd.Series(np.nan, index=indeks)
    makro = makro or {}

    # --- Dalga 1: Fiyat ve Piyasa Degiskenleri ---
    if degisken_id in ("z_sapma_5", "z_sapma_20", "z_sapma_60", "z_sapma_250"):
        pencere = int(degisken_id.split("_")[-1])
        ort = kapanis.rolling(pencere, min_periods=pencere).mean()
        std = kapanis.rolling(pencere, min_periods=pencere).std(ddof=1).replace(0.0, np.nan)
        return (kapanis - ort) / std

    if degisken_id == "rsi_14":
        return _rsi_hesapla(kapanis, periyot=14)

    if degisken_id == "bollinger_konum":
        ort = kapanis.rolling(20, min_periods=20).mean()
        std = kapanis.rolling(20, min_periods=20).std(ddof=1)
        ust_bant = ort + 2.0 * std
        alt_bant = ort - 2.0 * std
        genislik = (ust_bant - alt_bant).replace(0.0, np.nan)
        return (kapanis - alt_bant) / genislik

    if degisken_id == "hacim_oran":
        ort_hacim = hacim.rolling(20, min_periods=20).mean().replace(0.0, np.nan)
        return hacim / ort_hacim

    if degisken_id == "vix_seviye":
        return _piyasa_kapanis(piyasa, "VIX", indeks)

    if degisken_id == "vix_5g":
        vix = _piyasa_kapanis(piyasa, "VIX", indeks)
        return vix.pct_change(5)

    if degisken_id == "dxy_20g":
        dxy = _piyasa_kapanis(piyasa, "DXY", indeks)
        return dxy.pct_change(20)

    if degisken_id == "abd10y_20g":
        abd10y = _piyasa_kapanis(piyasa, "ABD10Y", indeks)
        # Yuzde puan farkini baz puana (bp) cevir
        return (abd10y - abd10y.shift(20)) * 100.0

    if degisken_id == "brent_1h":
        brent = _piyasa_kapanis(piyasa, "BRENT", indeks)
        return brent.pct_change(5)

    if degisken_id == "altin_1h":
        altin = _piyasa_kapanis(piyasa, "ALTIN", indeks)
        return altin.pct_change(5)

    if degisken_id == "bakir_1h":
        bakir = _piyasa_kapanis(piyasa, "BAKIR", indeks)
        return bakir.pct_change(5)

    if degisken_id == "beta_60":
        xu100 = _piyasa_kapanis(piyasa, "XU100", indeks)
        r_hisse = kapanis.pct_change()
        r_piyasa = xu100.pct_change()
        kov = r_hisse.rolling(60, min_periods=60).cov(r_piyasa)
        var = r_piyasa.rolling(60, min_periods=60).var(ddof=1).replace(0.0, np.nan)
        return kov / var

    # --- Dalga 2: Makroekonomi Degiskenleri ---
    if degisken_id == "usdtry_20g":
        usdtry = _piyasa_kapanis(piyasa, "USDTRY", indeks)
        return usdtry.pct_change(20)

    if degisken_id == "politika_faizi_deg":
        faiz = makro.get("politika_faizi")
        if faiz is None or faiz.empty:
            return pd.Series(np.nan, index=indeks, dtype=float)
        hizali = faiz.astype(float).reindex(indeks, method="ffill")
        # Son karar degisimi (bp): degisim oldugu gun farki al, sonra ileri tasi
        fark = hizali.diff()
        degisim_anlari = fark.where(fark != 0.0)
        return degisim_anlari.ffill().fillna(0.0) * 100.0

    if degisken_id == "reel_faiz":
        faiz = makro.get("politika_faizi")
        tufe = makro.get("tufe")
        if faiz is None or tufe is None or faiz.empty or tufe.empty:
            return pd.Series(np.nan, index=indeks, dtype=float)
        faiz_h = faiz.astype(float).reindex(indeks, method="ffill")
        tufe_h = tufe.astype(float).reindex(indeks, method="ffill")
        return faiz_h - tufe_h

    if degisken_id == "tufe_deg":
        tufe = makro.get("tufe")
        if tufe is None or tufe.empty:
            return pd.Series(np.nan, index=indeks, dtype=float)
        hizali = tufe.astype(float).reindex(indeks, method="ffill")
        fark = hizali.diff()
        degisim_anlari = fark.where(fark != 0.0)
        return degisim_anlari.ffill().fillna(0.0)

    # --- Dalga 3: Haber ve Olay Degiskenleri ---
    if degisken_id == "haber_skoru":
        if haber is None or haber.empty:
            return pd.Series(0.0, index=indeks, dtype=float)
        # 5 gunluk ustel sonumlu haber skoru toplami
        hizali = haber.astype(float).reindex(indeks).fillna(0.0)
        return hizali.ewm(halflife=5, adjust=False).mean()

    # --- Dalga 4: Takvim ve Duygu Degiskenleri ---
    if degisken_id == "takvim_bayram":
        tarihler = pd.to_datetime(indeks)
        kuklalar = []
        for t in tarihler:
            aktif = 0.0
            for ofset in range(-5, 6):
                gun = t + pd.Timedelta(days=ofset)
                if (gun.month, gun.day) in _SABIT_TATILLER:
                    aktif = 1.0
                    break
            kuklalar.append(aktif)
        return pd.Series(kuklalar, index=indeks, dtype=float)

    if degisken_id == "takvim_tatil":
        tarihler = pd.to_datetime(indeks)
        # Yaz tatili (Haziran ortasi - Eylul basi) ve somestr (Ocak sonu - Subat basi)
        tatil = [
            1.0
            if (
                (t.month in (7, 8))
                or (t.month == 6 and t.day >= 15)
                or (t.month == 9 and t.day <= 10)
                or (t.month == 1 and t.day >= 20)
                or (t.month == 2 and t.day <= 5)
            )
            else 0.0
            for t in tarihler
        ]
        return pd.Series(tatil, index=indeks, dtype=float)

    if degisken_id == "tuketici_guven":
        guven = makro.get("tuketici_guven")
        if guven is None or guven.empty:
            return pd.Series(np.nan, index=indeks, dtype=float)
        hizali = guven.astype(float).reindex(indeks, method="ffill")
        fark = hizali.diff()
        degisim_anlari = fark.where(fark != 0.0)
        return degisim_anlari.ffill().fillna(0.0)

    # --- Kontrol Degiskeni (Oz-Sinav) ---
    if degisken_id == "rastgele_kontrol":
        tohum = int(ayarlar.ayarlar().get("degerlendirme", {}).get("tohum", 42))
        rng = np.random.default_rng(tohum)
        return pd.Series(rng.standard_normal(len(indeks)), index=indeks, dtype=float)

    raise ValueError(f"Tanimsiz degisken_id: '{degisken_id}'")


def z_skoru(seri: pd.Series, pencere: int = 252) -> pd.Series:
    """Kayan pencerede (seri - ortalama) / std. Yalniz gecmis ve t kullanilir."""
    min_gozlem = min(20, pencere)
    ort = seri.rolling(pencere, min_periods=min_gozlem).mean()
    std = seri.rolling(pencere, min_periods=min_gozlem).std(ddof=1).replace(0.0, np.nan)
    return (seri - ort) / std


def yuzdelik_sira(seri: pd.Series, pencere: int = 252) -> pd.Series:
    """Son `pencere` gun icindeki yuzdelik sira, 0..1 arasinda. Gelecege bakmaz."""
    min_gozlem = min(20, pencere)

    def _son_eleman_yuzdeligi(arr: np.ndarray) -> float:
        gecerli = arr[~np.isnan(arr)]
        if len(gecerli) == 0 or np.isnan(arr[-1]):
            return np.nan
        return float(np.mean(gecerli <= arr[-1]))

    return seri.rolling(pencere, min_periods=min_gozlem).apply(_son_eleman_yuzdeligi, raw=True)


def ozellik_tablosu(
    fiyatlar: dict[str, pd.DataFrame] | None = None,
    piyasa: dict[str, pd.DataFrame] | None = None,
    makro: dict[str, pd.Series] | None = None,
    degisken_listesi: list[dict] | None = None,
) -> pd.DataFrame:
    """Tum hisseler ve aday degiskenler icin z-skorlu ozellik tablosu uretir.

    Donus: MultiIndex (tarih, kod), sutunlar = degisken id, degerler = z-skoru.
    """
    if fiyatlar is None:
        fiyatlar = {kod: veri.fiyat_oku(kod) for kod in ayarlar.hisse_kodlari()}

    if piyasa is None:
        piyasa_anahtarlari = ayarlar.hisseler().get("piyasa_serileri", {}).keys()
        piyasa = {}
        for anahtar in piyasa_anahtarlari:
            try:
                piyasa[anahtar] = veri.fiyat_oku(anahtar)
            except NotImplementedError:
                piyasa[anahtar] = pd.DataFrame()

    if makro is None:
        makro = {}
        bugun_tarih = ayarlar.bugun()
        for seri_adi in ("politika_faizi", "tufe", "tuketici_guven"):
            try:
                makro[seri_adi] = veri.makro_oku(seri_adi, bugun_tarih)
            except NotImplementedError:
                makro[seri_adi] = pd.Series(dtype=float)

    if degisken_listesi is None:
        degisken_listesi = kayit.dogrula(kayit.degiskenleri_oku())

    degisken_idleri = [d["id"] for d in degisken_listesi]
    hisse_parcalari: list[pd.DataFrame] = []

    for kod, fiyat_df in fiyatlar.items():
        if fiyat_df is None or fiyat_df.empty:
            continue

        sutunlar: dict[str, pd.Series] = {}
        for deg_id in degisken_idleri:
            ham = ham_degisken(deg_id, fiyat_df, piyasa, makro=makro)
            sutunlar[deg_id] = z_skoru(ham, pencere=252)

        hisse_tablo = pd.DataFrame(sutunlar, index=fiyat_df.index)
        hisse_tablo["kod"] = kod
        hisse_tablo.index.name = "tarih"
        hisse_tablo = hisse_tablo.reset_index().set_index(["tarih", "kod"])
        hisse_parcalari.append(hisse_tablo)

    if not hisse_parcalari:
        bos_index = pd.MultiIndex.from_arrays([[], []], names=["tarih", "kod"])
        return pd.DataFrame(columns=degisken_idleri, index=bos_index)

    sonuc = pd.concat(hisse_parcalari).sort_index()
    return sonuc[degisken_idleri]


def ileri_getiri(fiyatlar: dict[str, pd.DataFrame], ufuk: int = 5) -> pd.Series:
    """r = P(t+ufuk)/P(t) - 1, MultiIndex (tarih, kod). Yalniz test hesaplarinda kullanilir."""
    parcalar: list[pd.Series] = []
    for kod, df in fiyatlar.items():
        if df is None or df.empty or "kapanis" not in df.columns:
            continue
        kapanis = df["kapanis"].astype(float)
        getiri = kapanis.shift(-ufuk) / kapanis - 1.0
        getiri.index.name = "tarih"
        seri_df = getiri.rename("getiri").reset_index()
        seri_df["kod"] = kod
        parcalar.append(seri_df.set_index(["tarih", "kod"])["getiri"])

    if not parcalar:
        bos_index = pd.MultiIndex.from_arrays([[], []], names=["tarih", "kod"])
        return pd.Series(dtype=float, index=bos_index, name="getiri")

    return pd.concat(parcalar).sort_index()