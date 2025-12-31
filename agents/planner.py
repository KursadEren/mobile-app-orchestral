from pydantic import BaseModel
from typing import List

class PlannerAgent:
    def __init__(self, llm):
        self.llm = llm
    
    def create_plan(self, user_request: str) -> str:
        prompt = f"""Sen bir mobil uygulama mimarisın. 
Kullanici istegi: {user_request}

JSON formatinda uygulama plani olustur:
- app_name
- platform (flutter)
- screens listesi
- features listesi
- data_models listesi

Sadece JSON dondur."""

        response = self.llm.invoke(prompt)
        return response.content
