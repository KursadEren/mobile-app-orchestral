#!/usr/bin/env python3
"""
Mobil Uygulama Üretici - AI Agent Sistemi
Kullanıcı isteğine göre otomatik Flutter uygulaması üretir
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from agents import PlannerAgent, CoderAgent, TesterAgent
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# .env dosyasını yükle
load_dotenv()

# Renkli terminal çıktısı için
console = Console()


def main():
    # API key kontrolü
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "buraya_api_keyini_yaz":
        console.print("[bold red]❌ HATA: API key bulunamadı![/]")
        console.print("\n[yellow]Lütfen .env dosyasını oluştur ve ANTHROPIC_API_KEY ekle:[/]")
        console.print("[cyan]1. .env.example dosyasını kopyala → .env[/]")
        console.print("[cyan]2. ANTHROPIC_API_KEY=sk-ant-... şeklinde key'ini ekle[/]")
        console.print("[cyan]3. Tekrar çalıştır: python main.py[/]")
        return

    # Header
    console.print(Panel.fit(
        "[bold blue]🤖 MOBIL UYGULAMA ÜRETİCİ[/]\n"
        "[dim]AI Agent Sistemi - Flutter Uygulama Üretici[/]",
        border_style="blue"
    ))

    # Kullanıcı girişi
    console.print("\n[bold green]Ne tür bir mobil uygulama istiyorsun?[/]")
    console.print("[dim]Örnek: 'Bir todo listesi uygulaması', 'Hava durumu uygulaması'[/]\n")
    user_request = input("➜ ")

    if not user_request.strip():
        console.print("[red]Lütfen bir uygulama açıklaması gir![/]")
        return

    # LLM başlat
    try:
        llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=api_key,
            temperature=0.7
        )
    except Exception as e:
        console.print(f"[red]❌ LLM başlatılamadı: {e}[/]")
        return

    # Agentları oluştur
    planner = PlannerAgent(llm)
    coder = CoderAgent(llm)
    tester = TesterAgent(llm)

    # İşlem başlasın
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        # 1. PLANLAMA
        task1 = progress.add_task("[cyan]📋 Uygulama planlanıyor...", total=None)
        try:
            plan = planner.create_plan(user_request)
            progress.update(task1, completed=True)
            console.print("[green]✅ Plan hazır![/]")
        except Exception as e:
            console.print(f"[red]❌ Planlama hatası: {e}[/]")
            return

        # 2. KOD YAZMA
        task2 = progress.add_task("[cyan]💻 Flutter kodu yazılıyor...", total=None)
        try:
            code = coder.generate_code(plan)
            progress.update(task2, completed=True)
            console.print("[green]✅ Kod yazıldı![/]")
        except Exception as e:
            console.print(f"[red]❌ Kod yazma hatası: {e}[/]")
            return

        # 3. TEST YAZMA
        task3 = progress.add_task("[cyan]🧪 Testler yazılıyor...", total=None)
        try:
            tests = tester.generate_tests(code)
            progress.update(task3, completed=True)
            console.print("[green]✅ Testler yazıldı![/]")
        except Exception as e:
            console.print(f"[red]❌ Test yazma hatası: {e}[/]")
            return

    # Output klasörü oluştur
    os.makedirs("output", exist_ok=True)

    # Dosyaları kaydet
    with open("output/plan.json", "w", encoding="utf-8") as f:
        f.write(plan)

    with open("output/main.dart", "w", encoding="utf-8") as f:
        f.write(code)

    with open("output/main_test.dart", "w", encoding="utf-8") as f:
        f.write(tests)

    # Sonuç raporu
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        "[bold green]🎉 UYGULAMA OLUŞTURULDU![/]\n\n"
        "[cyan]📁 Dosyalar:[/]\n"
        "  • output/plan.json      → Uygulama planı\n"
        "  • output/main.dart      → Flutter kodu\n"
        "  • output/main_test.dart → Test kodları\n\n"
        "[yellow]📝 Sonraki Adımlar:[/]\n"
        "  1. Flutter projesine kodu kopyala\n"
        "  2. flutter run ile çalıştır\n"
        "  3. flutter test ile testleri çalıştır",
        border_style="green",
        title="Başarılı!"
    ))


if __name__ == "__main__":
    main()
