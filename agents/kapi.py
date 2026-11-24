"""
Doğrulama kapısı.

Kural tek cümle: `flutter analyze` 0 hata VE `flutter test` yeşil değilse
o uygulama GitHub'a gitmez.

Bu modül kodu DÜZELTMEZ. Yalnızca ölçer ve raporlar.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List

# `flutter analyze` çıktısındaki hata satırları:
#   error • Undefined name 'MyApp' • test/widget_test.dart:14:33 • undefined_identifier
# warning / info satırları geçişi engellemez.
_HATA_SATIRI = re.compile(r"^\s*error\s*[•\-]\s", re.MULTILINE)

# Her adım için makul üst sınırlar (saniye)
SURE_PUB_GET = 300
SURE_ANALYZE = 300
SURE_TEST = 600
SURE_CREATE = 300

# analyze hiç ölçülemediğinde (pub get patladı, flutter yok, timeout...)
# 0 döndürmek "temiz" gibi okunur; bunun yerine ÖLÇÜLEMEDİ kullanılır.
OLCULEMEDI = -1


def paket_adi_uret(slug: str) -> str:
    """
    Slug'ı geçerli bir Dart paket adına çevirir.
    'mood-journal' -> 'mood_journal', '3d-notes' -> 'app_3d_notes'
    """
    ad = re.sub(r"[^a-z0-9_]+", "_", (slug or "app").lower()).strip("_")
    if not ad or not re.match(r"^[a-z_]", ad):
        ad = f"app_{ad}" if ad else "app"
    return ad


def _komut_calistir(komut: List[str], cwd: str, sure: int) -> Dict:
    """Tek bir komutu çalıştırır, çıktısını ve sonucunu döndürür."""
    etiket = " ".join(komut)
    try:
        sonuc = subprocess.run(
            komut,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=sure,
            env={**os.environ, "PUB_CACHE": os.environ.get("PUB_CACHE", str(Path.home() / ".pub-cache"))},
        )
        cikti = (sonuc.stdout or "") + (sonuc.stderr or "")
        return {
            "calisti": True,
            "kod": sonuc.returncode,
            "cikti": cikti,
            "log": f"$ {etiket}\n[çıkış kodu: {sonuc.returncode}]\n{cikti}\n",
        }
    except FileNotFoundError:
        return {
            "calisti": False,
            "kod": 127,
            "cikti": "",
            "log": f"$ {etiket}\nHATA: '{komut[0]}' bulunamadı. Flutter SDK kurulu değil "
                   f"veya PATH'te değil. Doğrulama yapılamadı.\n",
        }
    except subprocess.TimeoutExpired:
        return {
            "calisti": False,
            "kod": 124,
            "cikti": "",
            "log": f"$ {etiket}\nHATA: {sure} saniyede bitmedi (timeout).\n",
        }


def flutter_var_mi() -> bool:
    """PATH'te flutter var mı?"""
    return shutil.which("flutter") is not None


def proje_iskeleti_kur(proje_yolu: str, paket_adi: str) -> Dict:
    """
    `flutter create` ile GERÇEK bir Flutter projesi açar.

    Elle yazılan pubspec.yaml yetmiyor: analyze/test çalışabilmek için
    .dart_tool, analysis_options.yaml, platform klasörleri gerekiyor.

    flutter create'in bıraktığı test/widget_test.dart silinir: o dosya
    bizim üretmediğimiz `MyApp` sınıfını çağırır ve her zaman kırmızıdır.
    """
    if not flutter_var_mi():
        return {
            "success": False,
            "error": "flutter bulunamadı (PATH'te yok). Gerçek proje iskeleti kurulamadı.",
        }

    # MUTLAK yola çevir: göreli yol + cwd birleşince hedef iki kez eklenip
    # proje yanlış yere (output/batch/output/batch/...) kuruluyordu.
    hedef = Path(proje_yolu).expanduser().resolve()
    hedef.mkdir(parents=True, exist_ok=True)

    sonuc = _komut_calistir(
        ["flutter", "create", "--project-name", paket_adi, str(hedef)],
        cwd=str(hedef.parent),
        sure=SURE_CREATE,
    )

    if sonuc["kod"] != 0:
        return {
            "success": False,
            "error": f"flutter create başarısız: {sonuc['log'][:800]}",
            "log": sonuc["log"],
        }

    if not (hedef / "pubspec.yaml").is_file():
        return {
            "success": False,
            "error": f"flutter create 0 döndürdü ama pubspec.yaml yok: {hedef}",
            "log": sonuc["log"],
        }

    # flutter create'in varsayılan testi olmayan MyApp'i çağırıyor -> her zaman kırmızı.
    varsayilan_test = hedef / "test" / "widget_test.dart"
    if varsayilan_test.exists():
        varsayilan_test.unlink()

    return {"success": True, "path": str(hedef), "paket_adi": paket_adi, "log": sonuc["log"]}


def analyze_hatalarini_say(cikti: str) -> int:
    """`flutter analyze` çıktısındaki 'error •' satırlarını sayar."""
    return len(_HATA_SATIRI.findall(cikti or ""))


def kapidan_gecir(proje_yolu: str) -> Dict:
    """
    Projeyi doğrulama kapısından geçirir.

    Sırayla: flutter pub get -> flutter analyze -> flutter test

    Döner:
        {
          "gecti": bool,          # analyze_hata == 0 ve test_gecti
          "analyze_hata": int,    # 'error •' satır sayısı; -1 = ölçülemedi
          "test_gecti": bool,
          "log": str,
        }
    """
    loglar = [f"# Doğrulama kapısı: {proje_yolu}\n"]

    def rapor(analyze_hata: int, test_gecti: bool) -> Dict:
        return {
            "gecti": analyze_hata == 0 and test_gecti,
            "analyze_hata": analyze_hata,
            "test_gecti": test_gecti,
            "log": "\n".join(loglar),
        }

    # 0) Proje var mı?
    if not Path(proje_yolu).is_dir():
        loglar.append(f"HATA: proje dizini yok: {proje_yolu}")
        return rapor(OLCULEMEDI, False)

    if not Path(proje_yolu, "pubspec.yaml").is_file():
        loglar.append("HATA: pubspec.yaml yok. Burası bir Flutter projesi değil.")
        return rapor(OLCULEMEDI, False)

    # 1) flutter kurulu mu? Kurulu değilse SESSİZCE GEÇİRME.
    if not flutter_var_mi():
        loglar.append(
            "HATA: 'flutter' PATH'te bulunamadı. Doğrulama yapılamadı, "
            "bu yüzden kapı KIRMIZI sayılıyor (doğrulanmamış kod geçmez)."
        )
        return rapor(OLCULEMEDI, False)

    # 2) flutter pub get
    pub = _komut_calistir(["flutter", "pub", "get"], proje_yolu, SURE_PUB_GET)
    loglar.append(pub["log"])
    if pub["kod"] != 0:
        loglar.append("HATA: 'flutter pub get' başarısız. analyze/test koşulamadı.")
        return rapor(OLCULEMEDI, False)

    # 3) flutter analyze  (warning/info engellemez, yalnız error sayılır)
    analyze = _komut_calistir(["flutter", "analyze", "--no-pub"], proje_yolu, SURE_ANALYZE)
    loglar.append(analyze["log"])

    if not analyze["calisti"]:
        loglar.append("HATA: 'flutter analyze' çalıştırılamadı.")
        return rapor(OLCULEMEDI, False)

    analyze_hata = analyze_hatalarini_say(analyze["cikti"])

    # analyze sıfırdan farklı çıkış kodu verdiği hâlde tek bir 'error •' satırı
    # yoksa, çıktı beklediğimiz biçimde değil demektir (SDK hatası, çökme...).
    # 0 hata diye raporlamak yanlış olur.
    if analyze["kod"] != 0 and analyze_hata == 0:
        if "No issues found" not in analyze["cikti"] and "issues found" not in analyze["cikti"]:
            loglar.append(
                f"HATA: 'flutter analyze' {analyze['kod']} koduyla bitti ama çıktı "
                "ayrıştırılamadı. Hata sayısı ölçülemedi."
            )
            return rapor(OLCULEMEDI, False)

    loglar.append(f"# analyze hata sayısı: {analyze_hata}\n")

    # 4) flutter test
    test = _komut_calistir(["flutter", "test", "--no-pub"], proje_yolu, SURE_TEST)
    loglar.append(test["log"])
    test_gecti = test["calisti"] and test["kod"] == 0
    loglar.append(f"# test sonucu: {'YEŞİL' if test_gecti else 'KIRMIZI'}\n")

    nihai = rapor(analyze_hata, test_gecti)
    loglar.append(
        f"# KAPI: {'YEŞİL' if nihai['gecti'] else 'KIRMIZI'} "
        f"(analyze_hata={analyze_hata}, test_gecti={test_gecti})"
    )
    nihai["log"] = "\n".join(loglar)
    return nihai


def kapi_ozeti(kapi: Dict) -> str:
    """Kapı sonucunu tek satırda özetler (konsol/rapor için)."""
    if kapi.get("gecti"):
        return "kapı YEŞİL (analyze 0 hata, testler geçti)"
    hata = kapi.get("analyze_hata", OLCULEMEDI)
    hata_metni = "ölçülemedi" if hata == OLCULEMEDI else f"{hata} hata"
    test_metni = "testler geçti" if kapi.get("test_gecti") else "testler geçmedi"
    return f"kapı KIRMIZI (analyze: {hata_metni}, {test_metni})"
