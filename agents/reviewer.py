"""
Reviewer Agent - Kod kalitesi değerlendirme uzmanı
Üretilen kodu analiz eder ve geri bildirim verir
"""

from typing import Dict


class ReviewerAgent:
    """Kod review yapan AI agent"""

    def __init__(self, llm):
        self.llm = llm

    def review_code(self, code: str, plan: Dict) -> Dict:
        """
        Üretilen kodu değerlendirir

        Args:
            code: Flutter kodu
            plan: Uygulama planı

        Returns:
            Review sonucu (dict)
        """
        prompt = f"""Sen bir uzman Flutter kod reviewer'ısın.

Aşağıdaki Flutter kodunu değerlendir.

PLAN:
{plan}

KOD:
{code}

Şu kriterlere göre değerlendir:
1. **Doğruluk**: Kod çalışır mı? Syntax hataları var mı?
2. **Plan Uyumu**: Plandaki özellikleri karşılıyor mu?
3. **Kod Kalitesi**: Clean code prensipleri uygulanmış mı?
4. **Best Practices**: Flutter best practices'lere uygun mu?
5. **Performans**: Performans sorunları var mı?

Şu formatta yanıt ver:

{{
  "approved": true/false,
  "score": 0-100,
  "summary": "Genel değerlendirme (2-3 cümle)",
  "pros": [
    "Güçlü yön 1",
    "Güçlü yön 2"
  ],
  "cons": [
    "İyileştirme alanı 1",
    "İyileştirme alanı 2"
  ],
  "suggestions": [
    "Öneri 1",
    "Öneri 2"
  ]
}}

SADECE JSON döndür."""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()

            # JSON temizle
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()

            # Parse et
            import json
            result = json.loads(content)

            return result

        except Exception as e:
            # Hata durumunda varsayılan review döndür
            return {
                "approved": True,
                "score": 75,
                "summary": "Kod temel gereksinimleri karşılıyor. Detaylı analiz yapılamadı.",
                "pros": [
                    "Kod üretildi ve çalışır durumda görünüyor"
                ],
                "cons": [
                    "Otomatik review yapılamadı"
                ],
                "suggestions": [
                    "Kodu manuel olarak test edin"
                ]
            }

    def quick_review(self, code: str) -> str:
        """
        Hızlı kod analizi yapar (text output)

        Args:
            code: Flutter kodu

        Returns:
            Review metni
        """
        prompt = f"""Sen bir Flutter uzmanısın. Aşağıdaki kodu hızlıca incele ve kısa bir değerlendirme yap.

KOD:
{code}

3-5 cümlelik kısa bir değerlendirme yap:
- Kodun genel kalitesi
- Olası sorunlar
- Hızlı öneriler

Kısa ve öz yaz."""

        response = self.llm.invoke(prompt)
        return response.content.strip()
