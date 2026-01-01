"""
Planner Agent - Uygulama planlama uzmanı
3 farklı seviyede plan oluşturur: Basit, Orta, Gelişmiş
"""

from pydantic import BaseModel
from typing import List, Dict
import json


class PlannerAgent:
    """Uygulama mimarisi planlayan agent"""

    def __init__(self, llm):
        self.llm = llm

    def create_plan(self, user_request: str) -> str:
        """Tek bir plan oluşturur (geriye uyumluluk için)"""
        plans = self.create_multiple_plans(user_request, count=1)
        return json.dumps(plans[0], ensure_ascii=False, indent=2)

    def create_multiple_plans(self, user_request: str, count: int = 3) -> List[Dict]:
        """
        Kullanıcı isteğine göre birden fazla plan seçeneği oluşturur

        Args:
            user_request: Kullanıcının uygulama isteği
            count: Oluşturulacak plan sayısı (varsayılan 3)

        Returns:
            Plan listesi (her biri dict)
        """
        prompt = f"""Sen bir uzman mobil uygulama mimarısın.

Kullanıcı İsteği: "{user_request}"

Bu isteğe göre 3 FARKLI seviyede uygulama planı oluştur:

1. **BASİT PLAN**: Minimum özelliklerle, yeni başlayanlar için
2. **ORTA PLAN**: Dengeli özellikler, çoğu kullanıcı için ideal
3. **GELİŞMİŞ PLAN**: Maksimum özellikler, profesyonel seviye

Her plan için şu JSON formatını kullan:

{{
  "plans": [
    {{
      "level": "Basit / Orta / Gelişmiş",
      "app_name": "Uygulama Adı",
      "platform": "flutter",
      "description": "Kısa açıklama (1-2 cümle)",
      "screens": [
        {{
          "name": "HomeScreen",
          "description": "Ana ekran açıklaması",
          "components": ["Widget1", "Widget2"]
        }}
      ],
      "screen_names": ["HomeScreen", "DetailScreen"],
      "features": [
        "Özellik 1",
        "Özellik 2",
        "Özellik 3"
      ],
      "data_models": [
        {{
          "name": "User",
          "fields": ["id", "name", "email"]
        }}
      ],
      "complexity": "low / medium / high"
    }}
  ]
}}

SADECE JSON döndür, başka açıklama yazma!"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()

            # JSON'ı temizle
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()

            # Parse et
            data = json.loads(content)

            # Planları al
            if "plans" in data:
                plans = data["plans"]
            elif isinstance(data, list):
                plans = data
            else:
                # Tek plan dönmüşse, 3'e çoğalt
                plans = [data] * 3

            # En fazla count kadar plan döndür
            return plans[:count]

        except json.JSONDecodeError as e:
            # JSON parse hatası - fallback planlar döndür
            return self._create_fallback_plans(user_request, count)
        except Exception as e:
            # Genel hata - fallback planlar döndür
            return self._create_fallback_plans(user_request, count)

    def _create_fallback_plans(self, user_request: str, count: int = 3) -> List[Dict]:
        """API hatası durumunda örnek planlar döndürür"""
        base_plan = {
            "level": "Orta",
            "app_name": "Mobil Uygulama",
            "platform": "flutter",
            "description": f"'{user_request}' isteğine göre oluşturulmuş uygulama",
            "screens": [
                {
                    "name": "HomeScreen",
                    "description": "Ana ekran",
                    "components": ["AppBar", "ListView", "FloatingActionButton"]
                },
                {
                    "name": "DetailScreen",
                    "description": "Detay ekranı",
                    "components": ["AppBar", "Container", "Button"]
                }
            ],
            "screen_names": ["HomeScreen", "DetailScreen", "SettingsScreen"],
            "features": [
                "Temel CRUD işlemleri",
                "Local storage",
                "Responsive tasarım"
            ],
            "data_models": [
                {
                    "name": "Item",
                    "fields": ["id", "title", "description", "createdAt"]
                }
            ],
            "complexity": "medium"
        }

        plans = []

        # Basit plan
        simple_plan = base_plan.copy()
        simple_plan.update({
            "level": "Basit",
            "screen_names": ["HomeScreen"],
            "features": ["Temel listeleme", "Ekleme/Silme"],
            "complexity": "low"
        })
        plans.append(simple_plan)

        # Orta plan
        plans.append(base_plan)

        # Gelişmiş plan
        advanced_plan = base_plan.copy()
        advanced_plan.update({
            "level": "Gelişmiş",
            "screen_names": ["HomeScreen", "DetailScreen", "SettingsScreen", "ProfileScreen", "SearchScreen"],
            "features": [
                "Gelişmiş CRUD işlemleri",
                "Firebase entegrasyonu",
                "Push notifications",
                "Dark mode",
                "Çoklu dil desteği",
                "Offline mode"
            ],
            "complexity": "high"
        })
        plans.append(advanced_plan)

        return plans[:count]
