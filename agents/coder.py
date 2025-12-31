class CoderAgent:
    """Flutter kodu üreten AI agent"""

    def __init__(self, llm):
        self.llm = llm

    def generate_code(self, plan_json: str) -> str:
        """Verilen plana göre Flutter main.dart kodu üretir"""
        prompt = f"""Sen bir uzman Flutter geliştiricisisin.

Aşağıdaki uygulama planına göre TAM ÇALIŞIR bir Flutter uygulaması yaz.

Plan:
{plan_json}

Gereksinimler:
- Material Design kullan
- Temiz ve okunabilir kod yaz
- Türkçe yorumlar ekle
- StatelessWidget veya StatefulWidget kullan
- Main fonksiyonu dahil et
- Tüm import'ları ekle

SADECE DART KODUNU DÖNDÜR, başka açıklama yazma."""

        response = self.llm.invoke(prompt)
        return response.content

    def generate_screen(self, screen_name: str, screen_details: dict) -> str:
        """Belirli bir ekran için kod üretir"""
        prompt = f"""Flutter için '{screen_name}' ekranını oluştur.

Detaylar: {screen_details}

Gereksinimler:
- Ayrı bir widget dosyası olarak yaz
- Import'ları ekle
- StatelessWidget veya StatefulWidget
- Türkçe yorumlar

SADECE DART KODUNU DÖNDÜR."""

        response = self.llm.invoke(prompt)
        return response.content
