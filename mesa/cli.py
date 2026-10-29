"""Komut satiri. SORUMLU: B (Plan gorev B-7).

Komutlar hazir; her biri servis/veri fonksiyonlarini cagirir.
Cagirdigi fonksiyon henuz yazilmadiysa anlasilir bir mesaj verir.
"""

from datetime import date

import typer

from mesa import YASAL_UYARI

app = typer.Typer(help="MESA komutlari. " + YASAL_UYARI)


def _calistir(is_adi: str, fonk, *args) -> None:
    try:
        fonk(*args)
        typer.echo(f"✓ {is_adi} tamamlandi")
    except NotImplementedError as e:
        typer.echo(f"… {is_adi}: henuz yazilmadi ({e})")
        raise typer.Exit(code=1)


@app.command("veri-indir")
def veri_indir(baslangic: str = "2014-01-02") -> None:
    """Gecmis veriyi indirir ve kalite raporu yazar."""
    from mesa import db, veri

    _calistir("tablolar", db.tablolari_olustur)
    _calistir("veri indirme", veri.hepsini_guncelle, date.fromisoformat(baslangic))


@app.command()
def degerlendir() -> None:
    """Ozellikler, 7 test, karneler ve agirliklar."""
    from mesa import servis

    _calistir("degerlendirme", servis.degerlendirmeyi_calistir)


@app.command()
def backtest(holdout: bool = False) -> None:
    """Walk-forward raporu (veya --holdout ile tek seferlik hold-out)."""
    from mesa import servis

    _calistir("backtest", servis.backtesti_calistir, holdout)


@app.command()
def gunluk() -> None:
    """Yeni gunu indirir, sinyalleri uretir, sinyal gunlugune yazar."""
    from mesa import servis

    _calistir("gunluk calisma", servis.gunluk_calistir)


if __name__ == "__main__":
    app()
