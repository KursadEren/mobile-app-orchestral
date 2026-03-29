#!/usr/bin/env python3
"""
Orkestral Mobil Uygulama Üretici - Gelişmiş AI Agent Sistemi

İki mod destekler:
1. TEK UYGULAMA: Kullanıcı isteğine göre tek uygulama üretir
2. BATCH MOD: 10 farklı uygulama üretip GitHub'a yükler
"""

import os
import sys
import json
import argparse
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from agents import (
    PlannerAgent, CoderAgent, TesterAgent, ReviewerAgent,
    OrchestratorAgent, BatchOrchestrator, QuickBatchOrchestrator
)
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

# .env dosyasını yükle
load_dotenv()

# Renkli terminal çıktısı için
console = Console()


def print_main_banner():
    """Ana banner'ı gösterir"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🤖 ORKESTRAL MOBİL UYGULAMA ÜRETİCİ                     ║
    ║                                                              ║
    ║     AI Agent Sistemi - Flutter Generator                    ║
    ║                                                              ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║     [1] TEK UYGULAMA  - Tek uygulama üret                   ║
    ║     [2] BATCH MOD     - 10 uygulama üret + GitHub           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def check_api_key() -> str:
    """Anthropic API key kontrolü"""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "buraya_api_keyini_yaz":
        console.print(Panel(
            "[bold red]❌ ANTHROPIC API KEY BULUNAMADI![/]\n\n"
            "[yellow]Lütfen şu adımları takip edin:[/]\n\n"
            "1️⃣  [cyan].env.example[/] dosyasını [cyan].env[/] olarak kopyalayın:\n"
            "   [dim]cp .env.example .env[/]\n\n"
            "2️⃣  [cyan].env[/] dosyasını açın ve API key'inizi ekleyin:\n"
            "   [dim]ANTHROPIC_API_KEY=sk-ant-api03-...[/]\n\n"
            "3️⃣  API key almak için:\n"
            "   [dim]https://console.anthropic.com[/]",
            border_style="red",
            title="Kurulum Gerekli"
        ))
        sys.exit(1)

    return api_key


def check_github_credentials() -> tuple:
    """GitHub credentials kontrolü (batch mod için)"""
    github_token = os.getenv("GITHUB_TOKEN")
    github_username = os.getenv("GITHUB_USERNAME")

    if not github_token or not github_username:
        console.print(Panel(
            "[bold red]❌ GITHUB KİMLİK BİLGİLERİ BULUNAMADI![/]\n\n"
            "[yellow]Batch mod için GitHub ayarları gerekli:[/]\n\n"
            "1️⃣  [cyan].env[/] dosyasına şunları ekleyin:\n"
            "   [dim]GITHUB_TOKEN=ghp_xxxxxxxxxxxx[/]\n"
            "   [dim]GITHUB_USERNAME=kullanici_adiniz[/]\n\n"
            "2️⃣  GitHub Token almak için:\n"
            "   [dim]https://github.com/settings/tokens[/]\n"
            "   [dim]→ Generate new token (classic)[/]\n"
            "   [dim]→ 'repo' yetkisini seçin[/]",
            border_style="red",
            title="GitHub Ayarları Gerekli"
        ))
        return None, None

    return github_token, github_username


def init_llm(api_key: str):
    """LLM'i başlatır"""
    console.print("[dim]🔧 AI modeli başlatılıyor...[/]")
    try:
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=api_key,
            temperature=0.7,
            max_tokens=4096
        )
        return llm
    except Exception as e:
        console.print(f"[red]❌ LLM başlatma hatası: {e}[/]")
        sys.exit(1)


def run_single_mode(llm):
    """Tek uygulama modu"""
    console.print("\n[bold cyan]📱 TEK UYGULAMA MODU[/]\n")

    # Agent'ları başlat
    console.print("[dim]🤖 AI agentlar hazırlanıyor...[/]")
    planner = PlannerAgent(llm)
    coder = CoderAgent(llm)
    tester = TesterAgent(llm)
    reviewer = ReviewerAgent(llm)
    orchestrator = OrchestratorAgent(llm, planner, coder, tester, reviewer)

    console.print("[green]✅ Sistem hazır![/]\n")

    # Kullanıcı isteği
    console.print("[bold green]Ne tür bir mobil uygulama istiyorsun?[/]\n")
    console.print("[dim]💡 Örnekler: Todo listesi, Hesap makinesi, Not defteri[/]\n")
    user_request = input("➜ ")

    if not user_request.strip():
        console.print("[red]Lütfen bir açıklama girin![/]")
        return

    console.print("\n[bold cyan]🚀 İşlem başlatılıyor...[/]\n")

    # Orchestrator çalıştır
    result = orchestrator.run(user_request)

    if result["status"] == "cancelled":
        console.print(f"\n[yellow]⚠️ İşlem iptal edildi: {result['reason']}[/]")
        return

    # Sonuçları kaydet
    save_single_output(result)


def run_batch_mode(llm, github_token: str, github_username: str):
    """Batch modu - 10 uygulama üret"""
    console.print("\n[bold cyan]🚀 BATCH MOD - 10 UYGULAMA[/]\n")

    # Batch orchestrator başlat
    batch = BatchOrchestrator(llm, github_token, github_username)

    # Çalıştır
    results = batch.run()

    # Sonuçları kaydet
    save_batch_summary(results)


def save_single_output(result: dict):
    """Tek uygulama sonuçlarını kaydeder"""
    os.makedirs("output", exist_ok=True)

    with open("output/plan.json", "w", encoding="utf-8") as f:
        json.dump(result.get("plan", {}), f, ensure_ascii=False, indent=2)

    with open("output/main.dart", "w", encoding="utf-8") as f:
        f.write(result.get("code", ""))

    with open("output/main_test.dart", "w", encoding="utf-8") as f:
        f.write(result.get("tests", ""))

    with open("output/review.json", "w", encoding="utf-8") as f:
        json.dump(result.get("review", {}), f, ensure_ascii=False, indent=2)

    console.print(Panel.fit(
        "[bold green]🎉 UYGULAMA OLUŞTURULDU![/]\n\n"
        "[cyan]📁 Dosyalar:[/]\n"
        "  • output/plan.json\n"
        "  • output/main.dart\n"
        "  • output/main_test.dart\n"
        "  • output/review.json",
        border_style="green"
    ))


def save_batch_summary(results: list):
    """Batch sonuç özetini kaydeder"""
    os.makedirs("output/batch", exist_ok=True)

    summary = {
        "total": len(results),
        "success": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] != "success"),
        "apps": []
    }

    for result in results:
        app_summary = {
            "name": result.get("idea", {}).get("name", "N/A"),
            "status": result["status"],
            "repo_url": result.get("repo_url", None),
            "error": result.get("error", None)
        }
        summary["apps"].append(app_summary)

    with open("output/batch/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    console.print(f"\n[dim]📁 Özet kaydedildi: output/batch/summary.json[/]")


def run_auto_batch_mode(llm, github_token: str, github_username: str):
    """Otomatik batch modu - onay istemeden çalışır (CI/CD için)"""
    console.print("\n[bold cyan]🚀 OTOMATİK BATCH MOD - 10 UYGULAMA[/]\n")

    # QuickBatchOrchestrator kullan (onay istemez)
    batch = QuickBatchOrchestrator(llm, github_token, github_username)

    # Çalıştır
    results = batch.run(auto_approve=True)

    # Sonuçları kaydet
    save_batch_summary(results)

    return results


def main():
    """Ana program"""
    # Argument parser
    parser = argparse.ArgumentParser(description='Orkestral Mobil Uygulama Üretici')
    parser.add_argument('--auto-batch', action='store_true',
                        help='Otomatik batch modu (CI/CD için, onay istemez)')
    parser.add_argument('--mode', type=str, choices=['1', '2'],
                        help='Mod seçimi: 1=Tek uygulama, 2=Batch')
    args = parser.parse_args()

    try:
        # Banner
        print_main_banner()

        # API key kontrolü
        api_key = check_api_key()

        # LLM başlat
        llm = init_llm(api_key)

        # Otomatik batch modu (GitHub Actions için)
        if args.auto_batch or args.mode == '2':
            github_token, github_username = check_github_credentials()

            if not github_token or not github_username:
                console.print("[red]❌ GitHub ayarları eksik![/]")
                sys.exit(1)

            if args.auto_batch:
                # Tamamen otomatik, onay yok
                run_auto_batch_mode(llm, github_token, github_username)
            else:
                # Normal batch modu (onay ister)
                console.print(Panel(
                    "[bold yellow]⚠️ BATCH MOD UYARISI[/]\n\n"
                    "Bu mod şunları yapacak:\n\n"
                    "1️⃣  AI ile 10 farklı uygulama fikri üretecek\n"
                    "2️⃣  Her biri için Flutter kodu yazacak\n"
                    "3️⃣  Her biri için testler üretecek\n"
                    "4️⃣  Her birini AYRI GitHub repo'suna yükleyecek\n"
                    f"   [dim]({github_username}/ altında private repo'lar)[/]\n\n"
                    "[cyan]Tahmini süre: 15-30 dakika[/]\n"
                    "[cyan]Tahmini maliyet: ~$0.50-1.00[/]",
                    border_style="yellow"
                ))

                if Confirm.ask("\n[bold]Devam etmek istiyor musun?[/]", default=True):
                    run_batch_mode(llm, github_token, github_username)
                else:
                    console.print("[yellow]İşlem iptal edildi.[/]")
            return

        # Mod seçimi (interaktif)
        if args.mode:
            mode = args.mode
        else:
            mode = Prompt.ask(
                "\n[bold cyan]Hangi modu kullanmak istiyorsun?[/]",
                choices=["1", "2"],
                default="1"
            )

        if mode == "1":
            # Tek uygulama modu
            run_single_mode(llm)

        elif mode == "2":
            # Batch modu
            github_token, github_username = check_github_credentials()

            if not github_token or not github_username:
                console.print("\n[yellow]GitHub ayarları eksik. Tek uygulama moduna geçiliyor...[/]")
                run_single_mode(llm)
            else:
                # Onay al
                console.print(Panel(
                    "[bold yellow]⚠️ BATCH MOD UYARISI[/]\n\n"
                    "Bu mod şunları yapacak:\n\n"
                    "1️⃣  AI ile 10 farklı uygulama fikri üretecek\n"
                    "2️⃣  Her biri için Flutter kodu yazacak\n"
                    "3️⃣  Her biri için testler üretecek\n"
                    "4️⃣  Her birini AYRI GitHub repo'suna yükleyecek\n"
                    f"   [dim]({github_username}/ altında private repo'lar)[/]\n\n"
                    "[cyan]Tahmini süre: 15-30 dakika[/]\n"
                    "[cyan]Tahmini maliyet: ~$0.50-1.00[/]",
                    border_style="yellow"
                ))

                if Confirm.ask("\n[bold]Devam etmek istiyor musun?[/]", default=True):
                    run_batch_mode(llm, github_token, github_username)
                else:
                    console.print("[yellow]İşlem iptal edildi.[/]")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️ İşlem kullanıcı tarafından iptal edildi.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Beklenmeyen hata: {e}[/]")
        console.print("[dim]Lütfen GitHub'da issue açın.[/]")
        sys.exit(1)


if __name__ == "__main__":
    main()
