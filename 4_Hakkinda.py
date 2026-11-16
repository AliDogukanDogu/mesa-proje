"""Ayarlar ve hakkinda. SORUMLU: D (Plan gorev D-6)."""

from typing import Any

import pandas as pd
import streamlit as st

from mesa import YASAL_UYARI
from mesa.ayarlar import ayarlar


def veri_kaynaklari_listesi() -> list[dict[str, str]]:
    """Projede kullanilan veri kaynaklari ve kapsam bilgilerini dondurur."""
    return [
        {
            "Kaynak": "Borsa İstanbul (BIST) Fiyat Verileri",
            "Kapsam": "Günlük açılış, yüksek, düşük, kapanış (OHLC) ve işlem hacmi serileri",
            "Güncelleme Sıklığı": "Gün sonu (EOD)",
        },
        {
            "Kaynak": "XU100 Kıyas Endeksi",
            "Kapsam": "BIST 100 endeks kapanış değerleri ve dönem bazlı kıyas getirileri",
            "Güncelleme Sıklığı": "Gün sonu (EOD)",
        },
        {
            "Kaynak": "MESA Sinyal ve İstatistik Motoru (mesa.servis)",
            "Kapsam": "Değişken karneleri (IC, q-değeri, 7 test), ayarlı skorlar ve backtest metrikleri",
            "Güncelleme Sıklığı": "Model çalıştırma döngüsü",
        },
    ]


def proje_ekibi_listesi() -> list[dict[str, str]]:
    """Proje gelistirme ekibi ve gorev dagilimini dondurur."""
    return [
        {
            "Rol": "Sorumlu A",
            "Sorumluluk Alanı": "Veri Toplama ve Ön İşleme",
            "Kapsam": "Fiyat/hacim veri boru hattı, temizlik ve eksik veri kontrolü",
        },
        {
            "Rol": "Sorumlu B",
            "Sorumluluk Alanı": "Değişken Üretimi ve İstatistiksel Eleme",
            "Kapsam": "Teknik/temel göstergeler, IC analizi ve 7 testlik karne değerlendirmesi",
        },
        {
            "Rol": "Sorumlu C",
            "Sorumluluk Alanı": "Skorlama, Rejim ve Backtest Motoru",
            "Kapsam": "Ayarlı skor hesabı, AL/SAT/BEKLE karar kuralları ve geçmiş performans simülasyonu",
        },
        {
            "Rol": "Sorumlu D (Berkay Öztürk)",
            "Sorumluluk Alanı": "Streamlit Arayüzleri ve Görselleştirme (D-5, D-6, D-7)",
            "Kapsam": "Ana pano, hisse detayı, değişken karneleri, backtest raporu ve ayarlar ekranları",
        },
    ]


def parametre_aciklama_tablosu(parametre_sozlugu: dict[str, Any]) -> pd.DataFrame:
    """ayarlar() ciktisindaki her parametreyi degeri ve aciklamasiyla tabloya donusturur."""
    bilinen_aciklamalar: dict[str, str] = {
        "hisse_kodlari": "Model kapsamında izlenen ve analiz edilen BIST hisse senedi sembolleri.",
        "esik_al": "Ayarlı skorun AL sinyali üretebilmesi için aşması gereken minimum pozitif eşik değeri.",
        "esik_sat": "Ayarlı skorun SAT sinyali üretebilmesi için altına inmesi gereken negatif eşik değeri.",
        "ic_esik": "Bir değişkenin istatistiksel olarak anlamlı kabul edilmesi için gereken minimum Bilgi Katsayısı (IC).",
        "q_esik": "Çoklu hipotez düzeltmesi (FDR) sonrası kabul edilen maksimum anlamlılık düzeyi.",
        "pencere": "Gösterge ve getiri hesaplamalarında kullanılan geriye dönük işlem günü penceresi.",
        "komisyon": "Backtest simülasyonunda alış/satış işlemlerine uygulanan işlem maliyeti oranı.",
        "kayma": "Backtest simülasyonunda emir gerçekleşme fiyatına uygulanan kayma (slippage) payı.",
        "baslangic_sermayesi": "Backtest portföy simülasyonunun başlangıç anapara tutarı.",
        "ornek_mod": "Gerçek motor bağlı değilken örnek veri setlerinin kullanılıp kullanılmayacağını belirler.",
    }

    satirlar: list[dict[str, str]] = []
    for anahtar, deger in parametre_sozlugu.items():
        norm_anahtar = str(anahtar).strip().lower()
        aciklama = bilinen_aciklamalar.get(
            norm_anahtar,
            f"Sistem yapılandırma parametresi ({anahtar}) — model ve arayüz davranışını kontrol eder.",
        )
        satirlar.append({
            "Parametre": str(anahtar),
            "Değer": str(deger),
            "Açıklama": aciklama,
        })

    return pd.DataFrame(satirlar, columns=["Parametre", "Değer", "Açıklama"])


def ayarlar_ve_hakkinda_sayfasi() -> None:
    """Ayarlar ve hakkinda arayuzunu cizer."""
    st.title("Ayarlar ve hakkında")
    st.warning(YASAL_UYARI)

    # 1. Veri kaynaklari
    st.subheader("Veri Kaynakları")
    st.dataframe(pd.DataFrame(veri_kaynaklari_listesi()), hide_index=True, use_container_width=True)

    # 2. Proje ekibi
    st.subheader("Proje Ekibi")
    st.dataframe(pd.DataFrame(proje_ekibi_listesi()), hide_index=True, use_container_width=True)

    # 3. Parametrelerin aciklamasi + salt okunur JSON
    st.subheader("Parametrelerin Açıklaması")
    mevcut_ayarlar = ayarlar()
    param_df = parametre_aciklama_tablosu(mevcut_ayarlar)
    st.dataframe(param_df, hide_index=True, use_container_width=True)

    with st.expander("Parametreler (salt okunur JSON)", expanded=False):
        st.json(mevcut_ayarlar)

    st.caption(YASAL_UYARI)


ayarlar_ve_hakkinda_sayfasi()
