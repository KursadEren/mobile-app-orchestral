"""
Batch Orchestrator - 10 uygulamayı sırayla üreten ana koordinatör
Her uygulama için:
1. Plan seçimi (onay ile)
2. Kod üretimi
3. Test üretimi
4. GitHub'a yükleme
"""

import os
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm

from .idea_generator import IdeaGeneratorAgent
from .planner import PlannerAgent
from .coder import CoderAgent
from .tester import TesterAgent
from .reviewer import ReviewerAgent
from .github_agent import GitHubAgent

console = Console()


class BatchOrchestrator:
    """10 uygulamayı sırayla üreten ana orkestratör"""

    def __init__(self, llm, github_token: str, github_username: str):
        """
        Args:
            llm: Language model instance
            github_token: GitHub Personal Access Token
            github_username: GitHub kullanıcı adı
        """
        self.llm = llm
        self.github_token = github_token
        self.github_username = github_username

        # Agentları başlat
        self.idea_generator = IdeaGeneratorAgent(llm)
        self.planner = PlannerAgent(llm)
        self.coder = CoderAgent(llm)
        self.tester = TesterAgent(llm)
        self.reviewer = ReviewerAgent(llm)
        self.github = GitHubAgent(github_token, github_username)

        # Sonuçları takip et
        self.results = []
        self.output_dir = "output/batch"

    def run(self) -> List[Dict]:
        """Ana batch işlemi başlatır"""
        console.print(Panel.fit(
            "[bold cyan]🚀 BATCH MOD - 10 UYGULAMA ÜRETİCİ[/]\n\n"
            "[dim]Bu mod 10 farklı mobil uygulama üretecek ve\n"
            "her birini ayrı GitHub repo'suna yükleyecek.[/]",
            border_style="cyan"
        ))

        # ADIM 1: Fikirler üret
        console.print("\n[bold yellow]📋 ADIM 1: FİKİR ÜRETİMİ[/]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]10 uygulama fikri üretiliyor...", total=None)
            ideas = self.idea_generator.generate_ideas(10)
            progress.update(task, completed=True)

        # Fikirleri göster
        self._display_ideas(ideas)

        # Onay al
        if not Confirm.ask("\n[cyan]Bu fikirlerle devam edilsin mi?[/]", default=True):
            console.print("[yellow]İşlem iptal edildi.[/]")
            return []

        # ADIM 2: Her uygulama için döngü
        console.print("\n[bold yellow]📋 ADIM 2: UYGULAMA ÜRETİMİ[/]\n")

        for i, idea in enumerate(ideas, 1):
            console.print(f"\n{'='*60}")
            console.print(f"[bold cyan]UYGULAMA {i}/10: {idea['name']}[/]")
            console.print(f"{'='*60}\n")

            result = self._process_single_app(idea, i)
            self.results.append(result)

            if result["status"] == "success":
                console.print(f"[bold green]✅ {idea['name']} başarıyla oluşturuldu![/]")
                console.print(f"[dim]📁 Repo: {result.get('repo_url', 'N/A')}[/]")
            else:
                console.print(f"[bold red]❌ {idea['name']} oluşturulamadı: {result.get('error', 'Bilinmeyen hata')}[/]")

            # İlk uygulama başarılıysa devam et
            if i == 1:
                if result["status"] != "success":
                    console.print("\n[red]⚠️  İlk uygulama başarısız oldu. İşlem durduruluyor.[/]")
                    break
                else:
                    console.print("\n[green]✅ İlk uygulama başarılı! Diğer 9 uygulamaya devam ediliyor...[/]")

            # Kısa bekleme (rate limiting için)
            if i < len(ideas):
                time.sleep(2)

        # Final rapor
        self._print_final_report()

        return self.results

    def _display_ideas(self, ideas: List[Dict]):
        """Fikirleri tablo olarak gösterir"""
        table = Table(title="🚀 10 Mobil Uygulama Fikri", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Uygulama", style="green", width=25)
        table.add_column("Kategori", style="yellow", width=15)
        table.add_column("Açıklama", style="white", width=40)
        table.add_column("Zorluk", style="blue", width=8)

        for idea in ideas:
            table.add_row(
                str(idea["id"]),
                idea["name"],
                idea["category"],
                idea["description"][:40] + "..." if len(idea["description"]) > 40 else idea["description"],
                idea["complexity"]
            )

        console.print(table)

    def _process_single_app(self, idea: Dict, app_number: int) -> Dict:
        """Tek bir uygulamayı işler"""
        app_slug = idea["slug"]
        app_path = f"{self.output_dir}/{app_slug}"

        try:
            # 1. Plan seç (basit plan otomatik seçilir, kullanıcı onaylar)
            console.print("[dim]📋 Plan oluşturuluyor...[/]")
            plans = self.planner.create_multiple_plans(
                f"{idea['name']}: {idea['description']}. Özellikler: {', '.join(idea['features'])}",
                count=1
            )

            if not plans:
                return {"status": "error", "error": "Plan oluşturulamadı", "idea": idea}

            selected_plan = plans[0]
            selected_plan["app_name"] = idea["name"]
            selected_plan["slug"] = app_slug

            console.print(f"[green]✅ Plan hazır: {selected_plan.get('level', 'Orta')} seviye[/]")

            # 2. Kod üret
            console.print("[dim]💻 Flutter kodu yazılıyor...[/]")
            code = self.coder.generate_code(json.dumps(selected_plan, ensure_ascii=False))

            if not code:
                return {"status": "error", "error": "Kod üretilemedi", "idea": idea}

            console.print("[green]✅ Kod yazıldı![/]")

            # 3. Test üret
            console.print("[dim]🧪 Testler yazılıyor...[/]")
            tests = self.tester.generate_tests(code, idea["name"])
            console.print("[green]✅ Testler yazıldı![/]")

            # 4. Proje klasörü oluştur
            console.print("[dim]📁 Proje yapısı oluşturuluyor...[/]")
            Path(app_path).mkdir(parents=True, exist_ok=True)
            Path(f"{app_path}/lib").mkdir(exist_ok=True)
            Path(f"{app_path}/test").mkdir(exist_ok=True)

            # Dosyaları kaydet
            with open(f"{app_path}/lib/main.dart", "w", encoding="utf-8") as f:
                f.write(code)

            with open(f"{app_path}/test/main_test.dart", "w", encoding="utf-8") as f:
                f.write(tests)

            # Flutter proje yapısı
            self.github.create_flutter_project(app_path, app_slug)

            # README oluştur
            self.github.create_readme(app_path, idea)

            # Plan ve review kaydet
            with open(f"{app_path}/plan.json", "w", encoding="utf-8") as f:
                json.dump(selected_plan, f, ensure_ascii=False, indent=2)

            console.print("[green]✅ Proje yapısı hazır![/]")

            # 5. GitHub'a yükle
            console.print("[dim]📤 GitHub'a yükleniyor...[/]")

            # Repo oluştur
            repo_result = self.github.create_repo(
                repo_name=app_slug,
                description=f"{idea['name']} - {idea['description']}",
                private=True
            )

            if not repo_result.get("success"):
                return {
                    "status": "error",
                    "error": f"Repo oluşturulamadı: {repo_result.get('error', '')}",
                    "idea": idea,
                    "local_path": app_path
                }

            # Kodu push et
            push_result = self.github.push_to_repo(
                local_path=app_path,
                repo_name=app_slug,
                commit_message=f"feat: {idea['name']} - AI tarafından üretildi"
            )

            if push_result.get("success"):
                return {
                    "status": "success",
                    "idea": idea,
                    "plan": selected_plan,
                    "repo_url": repo_result["url"],
                    "local_path": app_path
                }
            else:
                return {
                    "status": "error",
                    "error": f"Push başarısız: {push_result.get('error', '')}",
                    "idea": idea,
                    "local_path": app_path
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "idea": idea
            }

    def _print_final_report(self):
        """Final raporu yazdırır"""
        console.print("\n" + "=" * 70)
        console.print("[bold cyan]📊 BATCH İŞLEM RAPORU[/]")
        console.print("=" * 70 + "\n")

        # Sonuç tablosu
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Uygulama", style="white", width=25)
        table.add_column("Durum", style="white", width=10)
        table.add_column("GitHub Repo", style="blue", width=40)

        success_count = 0
        for i, result in enumerate(self.results, 1):
            idea = result.get("idea", {})
            status = "✅ Başarılı" if result["status"] == "success" else "❌ Hata"
            status_style = "green" if result["status"] == "success" else "red"
            repo_url = result.get("repo_url", result.get("error", "N/A"))[:40]

            if result["status"] == "success":
                success_count += 1

            table.add_row(
                str(i),
                idea.get("name", "N/A"),
                f"[{status_style}]{status}[/]",
                repo_url
            )

        console.print(table)

        # Özet
        console.print(f"\n[bold]Özet:[/]")
        console.print(f"  ✅ Başarılı: {success_count}/{len(self.results)}")
        console.print(f"  ❌ Başarısız: {len(self.results) - success_count}/{len(self.results)}")

        if success_count > 0:
            console.print(f"\n[green]🎉 {success_count} uygulama GitHub'a yüklendi![/]")
            console.print(f"[dim]GitHub profil: https://github.com/{self.github_username}?tab=repositories[/]")

        # Lokal dosyalar
        console.print(f"\n[dim]📁 Lokal dosyalar: {self.output_dir}/[/]")


class QuickBatchOrchestrator(BatchOrchestrator):
    """Hızlı batch modu - kullanıcı onayı olmadan çalışır"""

    def run(self, auto_approve: bool = True) -> List[Dict]:
        """Otomatik onaylı batch işlemi"""
        console.print(Panel.fit(
            "[bold cyan]⚡ HIZLI BATCH MOD[/]\n\n"
            "[dim]Onay istemeden 10 uygulama üretir.[/]",
            border_style="cyan"
        ))

        # Fikirler üret
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Fikirler üretiliyor...", total=None)
            ideas = self.idea_generator.generate_ideas(10)
            progress.update(task, completed=True)

        # Fikirleri göster
        self._display_ideas(ideas)

        # İlerleme çubuğu ile işle
        console.print("\n[bold yellow]📋 UYGULAMALAR ÜRETİLİYOR...[/]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]İşleniyor...", total=len(ideas))

            for i, idea in enumerate(ideas, 1):
                progress.update(task, description=f"[cyan]{idea['name']}...")
                result = self._process_single_app(idea, i)
                self.results.append(result)
                progress.advance(task)
                time.sleep(1)

        # Final rapor
        self._print_final_report()

        return self.results
