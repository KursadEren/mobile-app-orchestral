"""
agents/temizle.py testleri.

Harici bağımlılık yok; çalıştırmak için:
    python3 -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.temizle import kod_temizle, json_temizle  # noqa: E402


class KodTemizleTesti(unittest.TestCase):

    def test_basinda_duzyazi_olan_citli_girdi(self):
        """Çitin önündeki düzyazı atılır, yalnız kod kalır."""
        girdi = (
            "Elbette, burada Flutter uygulamanız için kapsamlı testler yazdım:\n\n"
            "```dart\n"
            "import 'package:flutter_test/flutter_test.dart';\n\n"
            "void main() {}\n"
            "```\n"
        )
        beklenen = (
            "import 'package:flutter_test/flutter_test.dart';\n\n"
            "void main() {}"
        )
        self.assertEqual(kod_temizle(girdi), beklenen)

    def test_citsiz_girdi_oldugu_gibi_kalir(self):
        """Çit yoksa kod değişmeden döner."""
        girdi = "import 'package:flutter/material.dart';\n\nvoid main() => runApp(const MyApp());"
        self.assertEqual(kod_temizle(girdi), girdi)

    def test_sonunda_aciklama_olan_girdi(self):
        """Çitten sonraki açıklama atılır, yalnız kod kısmı kalır."""
        girdi = (
            "```dart\n"
            "void main() {\n"
            "  runApp(const MyApp());\n"
            "}\n"
            "```\n\n"
            "Bu kod Material Design 3 kullanır ve setState ile çalışır.\n"
            "Başka bir şey isterseniz söyleyin."
        )
        beklenen = "void main() {\n  runApp(const MyApp());\n}"
        self.assertEqual(kod_temizle(girdi), beklenen)

    def test_hem_basinda_hem_sonunda_duzyazi(self):
        girdi = (
            "Tabii ki! İşte kod:\n"
            "```dart\n"
            "void main() {}\n"
            "```\n"
            "Kolay gelsin."
        )
        self.assertEqual(kod_temizle(girdi), "void main() {}")

    def test_etiketsiz_cit(self):
        """```dart yerine düz ``` kullanılmışsa da çitin içi alınır."""
        girdi = "İşte kod:\n```\nvoid main() {}\n```"
        self.assertEqual(kod_temizle(girdi), "void main() {}")

    def test_kapanmamis_cit_kesilmis_cikti(self):
        """max_tokens ile ortadan kesilen çıktıda kapanış çiti yoktur."""
        girdi = "İşte kod:\n```dart\nvoid main() {\n  final x = 1"
        self.assertEqual(kod_temizle(girdi), "void main() {\n  final x = 1")

    def test_birden_fazla_dart_citi_birlestirilir(self):
        girdi = (
            "Önce model:\n```dart\nclass A {}\n```\n"
            "Sonra ekran:\n```dart\nclass B {}\n```\n"
        )
        self.assertEqual(kod_temizle(girdi), "class A {}\n\nclass B {}")

    def test_bos_girdi(self):
        self.assertEqual(kod_temizle(""), "")
        self.assertEqual(kod_temizle(None or ""), "")

    def test_bastaki_tek_cit_izi(self):
        """Eski _clean_code davranışı: baştaki ```dart etiketi silinir."""
        self.assertEqual(kod_temizle("```dart\nvoid main() {}"), "void main() {}")

    def test_bos_satirlar_kirpilir(self):
        girdi = "\n\n```dart\n\nvoid main() {}\n\n```\n\n"
        self.assertEqual(kod_temizle(girdi), "void main() {}")


class JsonTemizleTesti(unittest.TestCase):

    def test_json_citi(self):
        girdi = 'İşte sonuç:\n```json\n{"approved": true}\n```\nUmarım olur.'
        self.assertEqual(json_temizle(girdi), '{"approved": true}')

    def test_citsiz_json(self):
        self.assertEqual(json_temizle('{"approved": true}'), '{"approved": true}')

    def test_etiketsiz_cit_json(self):
        self.assertEqual(json_temizle('```\n{"a": 1}\n```'), '{"a": 1}')


if __name__ == "__main__":
    unittest.main()
