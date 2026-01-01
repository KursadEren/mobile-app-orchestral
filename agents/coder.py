"""
Coder Agent - Flutter kodu üreten AI agent
İterasyon ve refinement desteği ile
"""


class CoderAgent:
    """Flutter kodu üreten AI agent"""

    def __init__(self, llm):
        self.llm = llm
        self.iteration_history = []

    def generate_code(self, plan_json: str, iteration: int = 1) -> str:
        """
        Verilen plana göre Flutter main.dart kodu üretir

        Args:
            plan_json: JSON formatında uygulama planı
            iteration: Kaçıncı iterasyon (1, 2, 3...)

        Returns:
            Flutter Dart kodu
        """
        # Önceki iterasyonlardan öğrenme
        iteration_context = ""
        if iteration > 1 and self.iteration_history:
            iteration_context = f"""
ÖNCEKİ İTERASYONLAR:
{chr(10).join(f"İterasyon {i+1}: Üretildi" for i in range(len(self.iteration_history)))}

Bu sefer daha farklı bir yaklaşım kullan, daha temiz ve okunabilir kod yaz.
"""

        prompt = f"""Sen bir uzman Flutter geliştiricisisin.

Aşağıdaki uygulama planına göre TAM ÇALIŞIR bir Flutter uygulaması yaz.

Plan:
{plan_json}

{iteration_context}

Gereksinimler:
- Material Design 3 kullan
- Temiz ve okunabilir kod yaz
- Türkçe yorumlar ekle
- StatelessWidget veya StatefulWidget kullan
- Main fonksiyonu dahil et
- Tüm import'ları ekle
- Provider veya GetX gibi state management kullanma, basit setState kullan
- Çalışır kod yaz, örnek veriler ekle

SADECE DART KODUNU DÖNDÜR, başka açıklama yazma.
```dart ile başlama, direkt kodu yaz."""

        response = self.llm.invoke(prompt)
        code = response.content

        # Kodu temizle
        code = self._clean_code(code)

        # Geçmişe ekle
        self.iteration_history.append(code)

        return code

    def refine_code(self, current_code: str, feedback: str) -> str:
        """
        Mevcut kodu kullanıcı geri bildirimine göre iyileştirir

        Args:
            current_code: Şu anki kod
            feedback: Kullanıcıdan gelen geri bildirim

        Returns:
            İyileştirilmiş kod
        """
        prompt = f"""Sen bir uzman Flutter geliştiricisisin.

Aşağıdaki Flutter kodunu kullanıcı geri bildirimine göre iyileştir.

MEVCUT KOD:
{current_code}

KULLANICI GERİ BİLDİRİMİ:
"{feedback}"

Gereksinimler:
- Kullanıcının istediği değişikliği yap
- Kodun geri kalanını koru
- Çalışır durumda tut
- Türkçe yorumlar ekle

SADECE GÜNCELLENMİŞ DART KODUNU DÖNDÜR.
```dart ile başlama, direkt kodu yaz."""

        response = self.llm.invoke(prompt)
        code = response.content

        # Kodu temizle
        code = self._clean_code(code)

        return code

    def generate_screen(self, screen_name: str, screen_details: dict) -> str:
        """Belirli bir ekran için kod üretir"""
        prompt = f"""Flutter için '{screen_name}' ekranını oluştur.

Detaylar: {screen_details}

Gereksinimler:
- Ayrı bir widget dosyası olarak yaz
- Import'ları ekle
- StatelessWidget veya StatefulWidget
- Material Design 3
- Türkçe yorumlar

SADECE DART KODUNU DÖNDÜR.
```dart ile başlama, direkt kodu yaz."""

        response = self.llm.invoke(prompt)
        code = response.content

        return self._clean_code(code)

    def _clean_code(self, code: str) -> str:
        """Kod çıktısını temizler"""
        # Markdown code block'larını kaldır
        if code.startswith("```dart"):
            code = code.replace("```dart", "", 1)

        if code.startswith("```"):
            code = code.replace("```", "", 1)

        if code.endswith("```"):
            code = code.rsplit("```", 1)[0]

        # Başındaki ve sonundaki boşlukları temizle
        code = code.strip()

        return code
