"""
Orchestrator Agent - Ana koordinatör
Tüm agentları yönetir, kullanıcı etkileşimini sağlar
"""

from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class OrchestratorAgent:
    """Ana orkestratör - tüm süreci yönetir"""

    def __init__(self, llm, planner, coder, tester, reviewer):
        self.llm = llm
        self.planner = planner
        self.coder = coder
        self.tester = tester
        self.reviewer = reviewer

        # Süreç durumu
        self.user_request = None
        self.selected_plan = None
        self.generated_code = None
        self.test_code = None
        self.review_result = None

    def run(self, user_request: str) -> Dict:
        """Ana orkestrasyon döngüsü"""
        self.user_request = user_request

        console.print(Panel.fit(
            f"[bold cyan]🎯 İstek:[/] {user_request}",
            border_style="cyan"
        ))

        # Adım 1: Plan Seçimi
        if not self._planning_phase():
            return {"status": "cancelled", "reason": "Plan seçilmedi"}

        # Adım 2: Kod Üretimi (iterasyonlu)
        if not self._coding_phase():
            return {"status": "cancelled", "reason": "Kod üretimi iptal edildi"}

        # Adım 3: Test Üretimi
        if not self._testing_phase():
            return {"status": "cancelled", "reason": "Test üretimi iptal edildi"}

        # Adım 4: Final Review
        if not self._review_phase():
            return {"status": "cancelled", "reason": "Review'da onaylanmadı"}

        return {
            "status": "success",
            "plan": self.selected_plan,
            "code": self.generated_code,
            "tests": self.test_code,
            "review": self.review_result
        }

    def _planning_phase(self) -> bool:
        """Planlama aşaması - 3 seçenek sunar"""
        console.print("\n[bold yellow]📋 ADIM 1: PLANLAMA[/]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]3 farklı plan oluşturuluyor...", total=None)

            try:
                plans = self.planner.create_multiple_plans(self.user_request, count=3)
                progress.update(task, completed=True)
            except Exception as e:
                console.print(f"[red]❌ Plan oluşturma hatası: {e}[/]")
                return False

        # Planları göster
        console.print("\n[bold green]✅ 3 Plan Hazır![/]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Seviye", style="green", width=15)
        table.add_column("Özellikler", style="yellow")
        table.add_column("Ekranlar", style="blue")

        for i, plan in enumerate(plans, 1):
            features = "\n".join(f"• {f}" for f in plan.get("features", [])[:4])
            screens = "\n".join(f"• {s}" for s in plan.get("screen_names", [])[:4])
            table.add_row(
                str(i),
                plan.get("level", "Orta"),
                features,
                screens
            )

        console.print(table)

        # Kullanıcı seçimi
        while True:
            choice = Prompt.ask(
                "\n[bold cyan]Hangi planı seçiyorsun?[/]",
                choices=["1", "2", "3", "detay", "iptal"],
                default="2"
            )

            if choice == "iptal":
                return False

            if choice == "detay":
                # Detaylı plan göster
                detail_choice = Prompt.ask("Hangi planın detayını görmek istersin?", choices=["1", "2", "3"])
                plan_detail = plans[int(detail_choice) - 1]
                console.print(Panel(
                    f"[bold]{plan_detail.get('app_name', 'Uygulama')}[/]\n\n"
                    f"[cyan]Açıklama:[/]\n{plan_detail.get('description', 'N/A')}\n\n"
                    f"[cyan]Ekranlar:[/]\n" + "\n".join(f"• {s}" for s in plan_detail.get('screen_names', [])) + "\n\n"
                    f"[cyan]Özellikler:[/]\n" + "\n".join(f"• {f}" for f in plan_detail.get('features', [])),
                    title=f"Plan {detail_choice} Detayı",
                    border_style="blue"
                ))
                continue

            # Plan seçildi
            self.selected_plan = plans[int(choice) - 1]
            console.print(f"\n[bold green]✅ Plan {choice} seçildi![/]\n")
            return True

    def _coding_phase(self) -> bool:
        """Kod üretim aşaması - iterasyonlu"""
        console.print("[bold yellow]📋 ADIM 2: KOD YAZIMI[/]\n")

        iteration = 1
        max_iterations = 3

        while iteration <= max_iterations:
            console.print(f"[dim]İterasyon {iteration}/{max_iterations}[/]\n")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Flutter kodu yazılıyor...", total=None)

                try:
                    self.generated_code = self.coder.generate_code(
                        str(self.selected_plan),
                        iteration=iteration
                    )
                    progress.update(task, completed=True)
                except Exception as e:
                    console.print(f"[red]❌ Kod yazma hatası: {e}[/]")
                    return False

            console.print("[bold green]✅ Kod yazıldı![/]\n")

            # Kod önizleme
            lines = self.generated_code.split('\n')
            preview = '\n'.join(lines[:20])
            console.print(Panel(
                f"[dim]{preview}\n...\n(Toplam {len(lines)} satır)[/]",
                title="Kod Önizleme",
                border_style="blue"
            ))

            # Kullanıcı seçimi
            console.print("\n[bold cyan]Ne yapmak istersin?[/]")
            choice = Prompt.ask(
                "Seçim yapın",
                choices=["onayla", "değiştir", "yeniden", "iptal"],
                default="onayla"
            )

            if choice == "onayla":
                console.print("[bold green]✅ Kod onaylandı![/]\n")
                return True

            elif choice == "iptal":
                return False

            elif choice == "yeniden":
                console.print("[yellow]🔄 Kod yeniden yazılıyor...[/]\n")
                iteration += 1
                continue

            elif choice == "değiştir":
                feedback = Prompt.ask("[cyan]Ne değişmesini istersin?[/]")
                console.print(f"[yellow]🔄 '{feedback}' uygulanıyor...[/]\n")

                # Feedback ile yeniden üret
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Kod güncelleniyor...", total=None)
                    try:
                        self.generated_code = self.coder.refine_code(
                            self.generated_code,
                            feedback
                        )
                        progress.update(task, completed=True)
                    except Exception as e:
                        console.print(f"[red]❌ Güncelleme hatası: {e}[/]")
                        return False

                console.print("[bold green]✅ Kod güncellendi![/]\n")
                iteration += 1

        console.print("[yellow]⚠️  Maksimum iterasyon sayısına ulaşıldı[/]")
        return Confirm.ask("Mevcut kodu kabul ediyor musun?", default=True)

    def _testing_phase(self) -> bool:
        """Test üretim aşaması"""
        console.print("[bold yellow]📋 ADIM 3: TEST YAZIMI[/]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Test kodları yazılıyor...", total=None)

            try:
                self.test_code = self.tester.generate_tests(
                    self.generated_code,
                    self.selected_plan.get("app_name", "App")
                )
                progress.update(task, completed=True)
            except Exception as e:
                console.print(f"[red]❌ Test yazma hatası: {e}[/]")
                return False

        console.print("[bold green]✅ Testler yazıldı![/]\n")

        # Test önizleme
        lines = self.test_code.split('\n')
        preview = '\n'.join(lines[:15])
        console.print(Panel(
            f"[dim]{preview}\n...\n(Toplam {len(lines)} satır)[/]",
            title="Test Önizleme",
            border_style="blue"
        ))

        return Confirm.ask("\n[cyan]Testleri onayla?[/]", default=True)

    def _review_phase(self) -> bool:
        """Final review aşaması"""
        console.print("\n[bold yellow]📋 ADIM 4: FİNAL REVIEW[/]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]AI review yapılıyor...", total=None)

            try:
                self.review_result = self.reviewer.review_code(
                    self.generated_code,
                    self.selected_plan
                )
                progress.update(task, completed=True)
            except Exception as e:
                console.print(f"[red]❌ Review hatası: {e}[/]")
                return False

        # Review sonucunu göster
        console.print("\n[bold green]✅ Review Tamamlandı![/]\n")
        console.print(Panel(
            self.review_result.get("summary", "Review yapıldı"),
            title="🔍 AI Review Sonucu",
            border_style="green" if self.review_result.get("approved", False) else "yellow"
        ))

        if not self.review_result.get("approved", True):
            return Confirm.ask("[yellow]Uyarılar var. Yine de devam et?[/]", default=True)

        return True
