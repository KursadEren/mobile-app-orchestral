"""
Idea Generator Agent - 10 farklı mobil uygulama fikri üretir
Her fikir benzersiz ve uygulanabilir olmalı
"""

from typing import List, Dict
import json


class IdeaGeneratorAgent:
    """10 benzersiz mobil uygulama fikri üreten agent"""

    def __init__(self, llm):
        self.llm = llm

    def generate_ideas(self, count: int = 10, category: str = None) -> List[Dict]:
        """
        Benzersiz mobil uygulama fikirleri üretir

        Args:
            count: Üretilecek fikir sayısı (varsayılan 10)
            category: Opsiyonel kategori filtresi

        Returns:
            Fikir listesi (her biri dict)
        """
        category_filter = f"\nKategori: {category}" if category else ""

        prompt = f"""Sen bir yaratıcı mobil uygulama uzmanısın.

{count} adet BENZERSİZ ve PRATİK mobil uygulama fikri üret.{category_filter}

Her fikir:
1. Gerçekçi ve uygulanabilir olmalı
2. Flutter ile yapılabilir olmalı
3. Birbirinden farklı kategorilerde olmalı
4. Açık ve net tanımlanmış olmalı

Şu kategorilerden çeşitlilik sağla:
- Verimlilik (Todo, Not, Takvim)
- Sağlık & Fitness
- Finans & Bütçe
- Eğitim & Öğrenme
- Sosyal & İletişim
- Eğlence & Oyun
- Yaşam Tarzı
- Yardımcı Araçlar

Her fikir için şu JSON formatını kullan:

{{
  "ideas": [
    {{
      "id": 1,
      "name": "Uygulama Adı",
      "slug": "uygulama-adi",
      "category": "Kategori",
      "description": "Kısa açıklama (1-2 cümle)",
      "features": ["Özellik 1", "Özellik 2", "Özellik 3"],
      "target_audience": "Hedef kitle",
      "complexity": "low/medium/high"
    }}
  ]
}}

SADECE JSON döndür, başka açıklama yazma!"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()

            # JSON temizle
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()

            # Parse et
            data = json.loads(content)

            if "ideas" in data:
                ideas = data["ideas"]
            elif isinstance(data, list):
                ideas = data
            else:
                ideas = [data]

            # Slug'ları düzelt
            for idea in ideas:
                if "slug" not in idea or not idea["slug"]:
                    idea["slug"] = self._create_slug(idea.get("name", f"app-{idea.get('id', 1)}"))

            return ideas[:count]

        except Exception as e:
            # Hata durumunda örnek fikirler döndür
            return self._get_fallback_ideas(count)

    def _create_slug(self, name: str) -> str:
        """İsimden URL-friendly slug oluşturur"""
        slug = name.lower()
        # Türkçe karakterleri değiştir
        replacements = {
            'ş': 's', 'ğ': 'g', 'ü': 'u', 'ö': 'o', 'ı': 'i', 'ç': 'c',
            'Ş': 's', 'Ğ': 'g', 'Ü': 'u', 'Ö': 'o', 'İ': 'i', 'Ç': 'c',
            ' ': '-', '_': '-'
        }
        for old, new in replacements.items():
            slug = slug.replace(old, new)
        # Sadece alfanumerik ve tire bırak
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        # Çift tireleri tek tire yap
        while '--' in slug:
            slug = slug.replace('--', '-')
        return slug.strip('-')

    def _get_fallback_ideas(self, count: int = 10) -> List[Dict]:
        """API hatası durumunda örnek fikirler döndürür"""
        fallback_ideas = [
            {
                "id": 1,
                "name": "Günlük Görev Takipçisi",
                "slug": "gunluk-gorev-takipcisi",
                "category": "Verimlilik",
                "description": "Günlük görevleri takip eden ve hatırlatan basit todo uygulaması",
                "features": ["Görev ekleme/silme", "Hatırlatıcılar", "İstatistikler"],
                "target_audience": "Öğrenciler ve çalışanlar",
                "complexity": "low"
            },
            {
                "id": 2,
                "name": "Harcama Takipçisi",
                "slug": "harcama-takipcisi",
                "category": "Finans",
                "description": "Günlük harcamaları kategorize eden bütçe uygulaması",
                "features": ["Harcama girişi", "Kategoriler", "Aylık rapor"],
                "target_audience": "Bütçe yönetmek isteyenler",
                "complexity": "medium"
            },
            {
                "id": 3,
                "name": "Su Takibi",
                "slug": "su-takibi",
                "category": "Sağlık",
                "description": "Günlük su tüketimini takip eden sağlık uygulaması",
                "features": ["Su ekleme", "Günlük hedef", "Hatırlatıcılar"],
                "target_audience": "Sağlıklı yaşam isteyenler",
                "complexity": "low"
            },
            {
                "id": 4,
                "name": "Kelime Ezberleyici",
                "slug": "kelime-ezberleyici",
                "category": "Eğitim",
                "description": "Yabancı dil kelimelerini flashcard yöntemiyle öğreten uygulama",
                "features": ["Flashcard'lar", "Quiz modu", "İlerleme takibi"],
                "target_audience": "Dil öğrenenler",
                "complexity": "medium"
            },
            {
                "id": 5,
                "name": "Pomodoro Timer",
                "slug": "pomodoro-timer",
                "category": "Verimlilik",
                "description": "Pomodoro tekniği ile çalışma seanslarını yöneten zamanlayıcı",
                "features": ["25/5 dakika döngüsü", "İstatistikler", "Özelleştirme"],
                "target_audience": "Odaklanmak isteyenler",
                "complexity": "low"
            },
            {
                "id": 6,
                "name": "Alışveriş Listesi",
                "slug": "alisveris-listesi",
                "category": "Yaşam Tarzı",
                "description": "Kategorize edilmiş alışveriş listesi uygulaması",
                "features": ["Ürün ekleme", "Kategoriler", "Liste paylaşımı"],
                "target_audience": "Ev kullanıcıları",
                "complexity": "low"
            },
            {
                "id": 7,
                "name": "Günlük Defteri",
                "slug": "gunluk-defteri",
                "category": "Yaşam Tarzı",
                "description": "Kişisel günlük tutma ve duygu takibi uygulaması",
                "features": ["Günlük yazma", "Duygu takibi", "Fotoğraf ekleme"],
                "target_audience": "Kendini ifade etmek isteyenler",
                "complexity": "medium"
            },
            {
                "id": 8,
                "name": "Basit Hesap Makinesi",
                "slug": "basit-hesap-makinesi",
                "category": "Yardımcı Araçlar",
                "description": "Temel ve bilimsel hesaplamalar yapan hesap makinesi",
                "features": ["4 işlem", "Geçmiş", "Bilimsel mod"],
                "target_audience": "Herkes",
                "complexity": "low"
            },
            {
                "id": 9,
                "name": "Quiz Oyunu",
                "slug": "quiz-oyunu",
                "category": "Eğlence",
                "description": "Çeşitli kategorilerde bilgi yarışması oyunu",
                "features": ["Kategoriler", "Puan sistemi", "Liderlik tablosu"],
                "target_audience": "Bilgi meraklıları",
                "complexity": "medium"
            },
            {
                "id": 10,
                "name": "Egzersiz Takipçisi",
                "slug": "egzersiz-takipcisi",
                "category": "Sağlık & Fitness",
                "description": "Günlük egzersizleri ve antrenmanları takip eden uygulama",
                "features": ["Egzersiz kütüphanesi", "Zamanlayıcı", "İlerleme grafikleri"],
                "target_audience": "Spor yapanlar",
                "complexity": "medium"
            }
        ]
        return fallback_ideas[:count]

    def present_ideas(self, ideas: List[Dict]) -> str:
        """Fikirleri güzel formatlanmış tablo olarak döndürür"""
        lines = []
        lines.append("=" * 80)
        lines.append(" " * 20 + "🚀 10 MOBİL UYGULAMA FİKRİ")
        lines.append("=" * 80)

        for idea in ideas:
            lines.append(f"\n[{idea['id']}] {idea['name']}")
            lines.append(f"    📁 Kategori: {idea['category']}")
            lines.append(f"    📝 {idea['description']}")
            lines.append(f"    ✨ Özellikler: {', '.join(idea['features'][:3])}")
            lines.append(f"    🎯 Hedef: {idea['target_audience']}")
            lines.append(f"    ⚙️  Karmaşıklık: {idea['complexity']}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
