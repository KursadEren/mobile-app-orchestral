"""
Ortak metin temizleyici.

LLM'ler "SADECE KODU DÖNDÜR" denmesine rağmen çıktıyı sık sık
"Elbette, işte kodunuz:" gibi bir düzyazıyla ve markdown çitiyle sarar.
Bu düzyazı dosyaya yazıldığında dosya artık Dart değildir; derleyici
ilk satırda patlar. Buradaki fonksiyonlar bütün agentlar için tek bir
temizleme davranışı sağlar.
"""

import re

# ```dart ... ``` bloklarını yakalar.
# Kapanış çiti yoksa (max_tokens ile kesilmiş çıktı) metnin sonuna kadar alır.
_CIT_DESENI = re.compile(
    r"```[ \t]*(?P<dil>[A-Za-z0-9_.+#-]*)[ \t]*(?:\r?\n|$)(?P<govde>.*?)(?:```|\Z)",
    re.DOTALL,
)

# Çit hiç yoksa baştaki/sondaki tek tük ``` izlerini silmek için.
_BAS_CIT = re.compile(r"^```[ \t]*[A-Za-z0-9_.+#-]*[ \t]*\r?\n?")
_SON_CIT = re.compile(r"\r?\n?[ \t]*```[ \t]*$")


def _citleri_bul(metin: str):
    """Metindeki bütün markdown çitlerini (dil, gövde) olarak döndürür."""
    return [
        (m.group("dil").lower(), m.group("govde"))
        for m in _CIT_DESENI.finditer(metin)
    ]


def _kaba_temizle(metin: str) -> str:
    """Çit yoksa: baştaki/sondaki ``` izlerini ve boşlukları siler."""
    s = metin.strip()
    s = _BAS_CIT.sub("", s)
    s = _SON_CIT.sub("", s)
    return s.strip()


def _cit_icini_al(metin: str, diller: tuple) -> str:
    """
    Metinde istenen dillerden biriyle etiketli çit varsa yalnız çitin içini
    döndürür; çitin öncesindeki ve sonrasındaki düzyazı atılır.

    Etiketli çit yoksa etiketsiz (```) çit denenir. Hiç çit yoksa metin
    kaba temizlikten geçip olduğu gibi döner.
    """
    if not metin:
        return ""

    citler = _citleri_bul(metin)

    # Önce istenen dil, sonra etiketsiz çit.
    for aranan in (diller, ("",)):
        secilen = [govde for dil, govde in citler if dil in aranan]
        if secilen:
            return "\n\n".join(p.strip() for p in secilen if p.strip()).strip()

    return _kaba_temizle(metin)


def kod_temizle(metin: str) -> str:
    """
    LLM çıktısından Dart kodunu çıkarır.

    - ```dart ... ``` çiti varsa yalnız çitin içi döner.
    - Çit yoksa metin baştaki/sondaki ``` izlerinden arındırılıp döner.
    - Aynı dille birden fazla çit varsa hepsi sırayla birleştirilir.
    """
    return _cit_icini_al(metin, ("dart", "flutter"))


def json_temizle(metin: str) -> str:
    """LLM çıktısından JSON gövdesini çıkarır (```json çiti dahil)."""
    return _cit_icini_al(metin, ("json",))
