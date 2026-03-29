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
                "name": "Ruh Hali Günlüğü",
                "slug": "ruh-hali-gunlugu",
                "category": "Sağlık & Wellness",
                "description": "Günlük ruh halini emoji ile kaydet, haftalık mood grafiği gör",
                "features": ["Emoji ile mood seçimi", "Haftalık grafik", "Not ekleme", "Hatırlatıcı"],
                "target_audience": "Mental sağlığını takip etmek isteyenler",
                "complexity": "medium"
            },
            {
                "id": 2,
                "name": "Kitap Okuma Takipçisi",
                "slug": "kitap-okuma-takipcisi",
                "category": "Eğitim",
                "description": "Okuduğun kitapları, sayfa sayısını ve notlarını kaydet",
                "features": ["Kitap ekleme", "Sayfa takibi", "Okuma hedefi", "Kitap notları"],
                "target_audience": "Kitap severler",
                "complexity": "medium"
            },
            {
                "id": 3,
                "name": "Uyku Kalitesi Takipçisi",
                "slug": "uyku-kalitesi-takipcisi",
                "category": "Sağlık",
                "description": "Uyku saatlerini ve kalitesini kaydet, uyku düzenini analiz et",
                "features": ["Uyku başlangıç/bitiş", "Kalite puanı", "Haftalık analiz", "İpuçları"],
                "target_audience": "Uyku düzenini iyileştirmek isteyenler",
                "complexity": "medium"
            },
            {
                "id": 4,
                "name": "Fotoğraf Hatıra Defteri",
                "slug": "fotograf-hatira-defteri",
                "category": "Yaşam Tarzı",
                "description": "Günlük 1 fotoğraf çek, kısa not ekle, yıllık kolaj oluştur",
                "features": ["Günlük fotoğraf", "Konum etiketi", "Not ekleme", "Yıllık görünüm"],
                "target_audience": "Anılarını saklamak isteyenler",
                "complexity": "medium"
            },
            {
                "id": 5,
                "name": "Borç Takipçisi",
                "slug": "borc-takipcisi",
                "category": "Finans",
                "description": "Arkadaşlarla olan borç/alacak ilişkilerini takip et",
                "features": ["Borç/alacak girişi", "Kişi bazlı takip", "Hatırlatıcı", "Ödeme kaydı"],
                "target_audience": "Arkadaşlarıyla para alışverişi yapanlar",
                "complexity": "low"
            },
            {
                "id": 6,
                "name": "Alışkanlık Zinciri",
                "slug": "aliskanlik-zinciri",
                "category": "Verimlilik",
                "description": "Günlük alışkanlıklarını streak ile takip et, zinciri kırma",
                "features": ["Alışkanlık ekleme", "Günlük check", "Streak sayacı", "İstatistikler"],
                "target_audience": "Yeni alışkanlıklar edinmek isteyenler",
                "complexity": "medium"
            },
            {
                "id": 7,
                "name": "Tarif Defteri",
                "slug": "tarif-defteri",
                "category": "Yaşam Tarzı",
                "description": "Favori yemek tariflerini kaydet, malzeme listesi çıkar",
                "features": ["Tarif ekleme", "Fotoğraf", "Malzeme listesi", "Kategori"],
                "target_audience": "Yemek yapanlar",
                "complexity": "medium"
            },
            {
                "id": 8,
                "name": "Bitki Bakım Asistanı",
                "slug": "bitki-bakim-asistani",
                "category": "Yaşam Tarzı",
                "description": "Evdeki bitkilerin sulama ve bakım zamanını hatırlat",
                "features": ["Bitki ekleme", "Sulama takvimi", "Hatırlatıcılar", "Bakım notları"],
                "target_audience": "Bitki sahipleri",
                "complexity": "low"
            },
            {
                "id": 9,
                "name": "Motivasyon Kutusu",
                "slug": "motivasyon-kutusu",
                "category": "Wellness",
                "description": "Günlük motivasyon sözleri, favorilere ekle, paylaş",
                "features": ["Günün sözü", "Favoriler", "Bildirimler", "Paylaşım"],
                "target_audience": "Motivasyona ihtiyaç duyanlar",
                "complexity": "low"
            },
            {
                "id": 10,
                "name": "Film ve Dizi Listesi",
                "slug": "film-dizi-listesi",
                "category": "Eğlence",
                "description": "İzlemek istediğin ve izlediğin film/dizileri listele ve puanla",
                "features": ["Liste ekleme", "İzledim işareti", "Puanlama", "Kategoriler"],
                "target_audience": "Film ve dizi severler",
                "complexity": "low"
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
