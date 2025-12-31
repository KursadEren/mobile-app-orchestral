class TesterAgent:
    """Flutter test kodu üreten AI agent"""

    def __init__(self, llm):
        self.llm = llm

    def generate_tests(self, code: str, app_name: str = "TestApp") -> str:
        """Verilen Flutter kodu için test üretir"""
        prompt = f"""Sen bir Flutter test uzmanısın.

Aşağıdaki Flutter kodu için KAPSAMLI testler yaz:

Kod:
{code}

Gereksinimler:
- flutter_test paketini kullan
- Widget testleri yaz
- testWidgets kullan
- pump() ve pumpAndSettle() kullan
- find.byType, find.text kullan
- En az 3-5 test senaryosu
- Türkçe yorumlar

SADECE TEST KODUNU DÖNDÜR (import'larla birlikte)."""

        response = self.llm.invoke(prompt)
        return response.content

    def generate_unit_tests(self, model_code: str, model_name: str) -> str:
        """Model/Class için unit test üretir"""
        prompt = f"""'{model_name}' modeli için unit testler yaz.

Model Kodu:
{model_code}

Gereksinimler:
- test() ve group() kullan
- expect() ile assertion'lar
- Edge case'leri test et
- Türkçe yorumlar

SADECE TEST KODUNU DÖNDÜR."""

        response = self.llm.invoke(prompt)
        return response.content
