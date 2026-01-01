#!/usr/bin/env python3
"""
Mobil Uygulama Üretici - Gelişmiş AI Agent Sistemi
Kullanıcı isteğine göre otomatik Flutter uygulaması üretir
- Çoklu plan seçenekleri
- İterasyon desteği
- Kod review
- İnteraktif kullanıcı deneyimi
"""

import os
import json
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from agents import PlannerAgent, CoderAgent, TesterAgent, ReviewerAgent, OrchestratorAgent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# .env dosyasını yükle
load_dotenv()

# Renkli terminal çıktısı için
console = Console()


def print_banner():
    """Başlangıç banner'ını gösterir"""
    banner = """
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║     🤖 ORKESTRAL MOBİL UYGULAMA ÜRETİCİ         ║
    ║                                                  ║
    ║     AI Agent Sistemi - Flutter Generator        ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("\n[dim]Birden fazla plan seçeneği • İterasyon desteği • AI Kod Review[/]\n")


def check_api_key() -> str:
    """API key kontrolü yapar"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "buraya_api_keyini_yaz":
        console.print(Panel(
            "[bold red]❌ API KEY BULUNAMADI![/]\n\n"
            "[yellow]Lütfen şu adımları takip edin:[/]\n\n"
            "1️⃣  [cyan].env.example[/] dosyasını [cyan].env[/] olarak kopyalayın:\n"
            "   [dim]cp .env.example .env[/]\n\n"
            "2️⃣  [cyan].env[/] dosyasını açın ve API key'inizi ekleyin:\n"
            "   [dim]ANTHROPIC_API_KEY=sk-ant-api03-...[/]\n\n"
            "3️⃣  API key almak için:\n"
            "   [dim]https://console.anthropic.com[/]\n\n"
            "4️⃣  Programı tekrar çalıştırın:\n"
            "   [dim]python main.py[/]",
            border_style="red",
            title="Kurulum Gerekli"
        ))
        exit(1)

    return api_key


def get_user_request() -> str:
    """Kullanıcıdan uygulama isteği alır"""
    console.print("[bold green]Ne tür bir mobil uygulama istiyorsun?[/]\n")

    console.print("[dim]💡 Örnekler:[/]")
    examples = [
        "• Bir todo listesi uygulaması",
        "• Hesap makinesi",
        "• Not defteri uygulaması",
        "• Hava durumu uygulaması",
        "• Quiz oyunu"
    ]
    for ex in examples:
        console.print(f"  [cyan]{ex}[/]")

    console.print()
    user_request = input("➜ ")

    if not user_request.strip():
        console.print("[red]Lütfen bir uygulama açıklaması girin![/]")
        exit(1)

    return user_request.strip()


def save_outputs(result: dict):
    """Sonuçları dosyalara kaydeder"""
    os.makedirs("output", exist_ok=True)

    # Plan kaydet
    with open("output/plan.json", "w", encoding="utf-8") as f:
        json.dump(result["plan"], f, ensure_ascii=False, indent=2)

    # Kod kaydet
    with open("output/main.dart", "w", encoding="utf-8") as f:
        f.write(result["code"])

    # Test kaydet
    with open("output/main_test.dart", "w", encoding="utf-8") as f:
        f.write(result["tests"])

    # Review kaydet
    with open("output/review.json", "w", encoding="utf-8") as f:
        json.dump(result["review"], f, ensure_ascii=False, indent=2)


def print_success_message():
    """Başarı mesajını gösterir"""
    console.print("\n" + "="*70)
    console.print(Panel.fit(
        "[bold green]🎉 UYGULAMA BAŞARIYLA OLUŞTURULDU![/]\n\n"
        "[cyan]📁 Oluşturulan Dosyalar:[/]\n"
        "  • [yellow]output/plan.json[/]      → Seçilen plan detayları\n"
        "  • [yellow]output/main.dart[/]      → Flutter uygulama kodu\n"
        "  • [yellow]output/main_test.dart[/] → Test kodları\n"
        "  • [yellow]output/review.json[/]    → AI kod review raporu\n\n"
        "[cyan]📝 Sonraki Adımlar:[/]\n"
        "  1. Flutter projesine kodu kopyalayın\n"
        "  2. [dim]flutter run[/] ile uygulamayı çalıştırın\n"
        "  3. [dim]flutter test[/] ile testleri çalıştırın\n\n"
        "[dim]Detaylı kullanım için: NASIL_KULLANILIR.md[/]",
        border_style="green",
        title="✅ Başarılı!"
    ))
    console.print("="*70 + "\n")


def main():
    """Ana program"""
    try:
        # Banner
        print_banner()

        # API key kontrolü
        api_key = check_api_key()

        # LLM başlat
        console.print("[dim]🔧 AI modeli başlatılıyor...[/]")
        try:
            llm = ChatAnthropic(
                model="claude-sonnet-4-20250514",
                api_key=api_key,
                temperature=0.7,
                max_tokens=4096
            )
        except Exception as e:
            console.print(f"[red]❌ LLM başlatma hatası: {e}[/]")
            console.print("[yellow]API key'inizi kontrol edin.[/]")
            exit(1)

        # Agent'ları başlat
        console.print("[dim]🤖 AI agentlar hazırlanıyor...[/]")
        planner = PlannerAgent(llm)
        coder = CoderAgent(llm)
        tester = TesterAgent(llm)
        reviewer = ReviewerAgent(llm)
        orchestrator = OrchestratorAgent(llm, planner, coder, tester, reviewer)

        console.print("[green]✅ Sistem hazır![/]\n")

        # Kullanıcı isteğini al
        user_request = get_user_request()

        console.print("\n[bold cyan]🚀 İşlem başlatılıyor...[/]\n")

        # Orchestrator'ı çalıştır
        result = orchestrator.run(user_request)

        # Sonuç kontrolü
        if result["status"] == "cancelled":
            console.print(f"\n[yellow]⚠️  İşlem iptal edildi: {result['reason']}[/]")
            exit(0)

        # Dosyaları kaydet
        console.print("\n[dim]💾 Dosyalar kaydediliyor...[/]")
        save_outputs(result)

        # Başarı mesajı
        print_success_message()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  İşlem kullanıcı tarafından iptal edildi.[/]")
        exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Beklenmeyen hata: {e}[/]")
        console.print("[dim]Lütfen GitHub'da issue açın: https://github.com/KursadEren/mobile-app-orchestral/issues[/]")
        exit(1)


if __name__ == "__main__":
    main()
