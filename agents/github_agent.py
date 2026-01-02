"""
GitHub Agent - GitHub repo oluşturma ve kod yükleme
Private repo oluşturur ve Flutter projesini push eder
"""

import os
import subprocess
import shutil
from typing import Dict, Optional
from pathlib import Path


class GitHubAgent:
    """GitHub işlemlerini yöneten agent"""

    def __init__(self, github_token: str, github_username: str):
        """
        Args:
            github_token: GitHub Personal Access Token
            github_username: GitHub kullanıcı adı
        """
        self.token = github_token
        self.username = github_username
        self.base_url = f"https://{github_token}@github.com/{github_username}"

    def create_repo(self, repo_name: str, description: str = "", private: bool = True) -> Dict:
        """
        Yeni GitHub repo'su oluşturur

        Args:
            repo_name: Repo adı
            description: Repo açıklaması
            private: Private repo mu? (varsayılan True)

        Returns:
            Sonuç dict'i
        """
        try:
            # gh CLI kullanarak repo oluştur
            visibility = "--private" if private else "--public"
            cmd = [
                "gh", "repo", "create",
                f"{self.username}/{repo_name}",
                visibility,
                "--description", description,
                "--confirm"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env={**os.environ, "GH_TOKEN": self.token}
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "repo_name": repo_name,
                    "url": f"https://github.com/{self.username}/{repo_name}",
                    "private": private
                }
            else:
                # Repo zaten var olabilir
                if "already exists" in result.stderr.lower():
                    return {
                        "success": True,
                        "repo_name": repo_name,
                        "url": f"https://github.com/{self.username}/{repo_name}",
                        "private": private,
                        "note": "Repo zaten mevcut"
                    }
                return {
                    "success": False,
                    "error": result.stderr
                }

        except FileNotFoundError:
            # gh CLI yüklü değilse curl ile dene
            return self._create_repo_with_api(repo_name, description, private)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _create_repo_with_api(self, repo_name: str, description: str, private: bool) -> Dict:
        """GitHub API kullanarak repo oluşturur (gh CLI yoksa)"""
        import json

        data = json.dumps({
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": False
        })

        cmd = [
            "curl", "-s", "-X", "POST",
            "-H", f"Authorization: token {self.token}",
            "-H", "Accept: application/vnd.github.v3+json",
            "https://api.github.com/user/repos",
            "-d", data
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        try:
            response = json.loads(result.stdout)
            if "html_url" in response:
                return {
                    "success": True,
                    "repo_name": repo_name,
                    "url": response["html_url"],
                    "private": private
                }
            elif "errors" in response:
                if any("name already exists" in str(e) for e in response["errors"]):
                    return {
                        "success": True,
                        "repo_name": repo_name,
                        "url": f"https://github.com/{self.username}/{repo_name}",
                        "private": private,
                        "note": "Repo zaten mevcut"
                    }
                return {
                    "success": False,
                    "error": str(response["errors"])
                }
            else:
                return {
                    "success": False,
                    "error": response.get("message", "Bilinmeyen hata")
                }
        except:
            return {
                "success": False,
                "error": result.stdout
            }

    def create_flutter_project(self, project_path: str, app_name: str) -> Dict:
        """
        Flutter projesi oluşturur

        Args:
            project_path: Proje dizini
            app_name: Uygulama adı

        Returns:
            Sonuç dict'i
        """
        try:
            # Klasörü oluştur
            Path(project_path).mkdir(parents=True, exist_ok=True)

            # Flutter projesi oluştur
            result = subprocess.run(
                ["flutter", "create", "--project-name", app_name.replace("-", "_"), "."],
                cwd=project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return {"success": True, "path": project_path}
            else:
                # Flutter yoksa basit yapı oluştur
                return self._create_basic_structure(project_path, app_name)

        except FileNotFoundError:
            # Flutter yüklü değilse basit yapı oluştur
            return self._create_basic_structure(project_path, app_name)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_basic_structure(self, project_path: str, app_name: str) -> Dict:
        """Flutter olmadan temel proje yapısı oluşturur"""
        try:
            Path(project_path).mkdir(parents=True, exist_ok=True)
            Path(f"{project_path}/lib").mkdir(exist_ok=True)
            Path(f"{project_path}/test").mkdir(exist_ok=True)

            # pubspec.yaml oluştur
            pubspec = f"""name: {app_name.replace("-", "_")}
description: AI tarafından üretilmiş Flutter uygulaması
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
"""
            with open(f"{project_path}/pubspec.yaml", "w") as f:
                f.write(pubspec)

            return {"success": True, "path": project_path}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def push_to_repo(self, local_path: str, repo_name: str, commit_message: str = "Initial commit") -> Dict:
        """
        Lokal projeyi GitHub'a push eder

        Args:
            local_path: Lokal proje dizini
            repo_name: GitHub repo adı
            commit_message: Commit mesajı

        Returns:
            Sonuç dict'i
        """
        try:
            remote_url = f"https://{self.token}@github.com/{self.username}/{repo_name}.git"

            # Git init
            subprocess.run(["git", "init"], cwd=local_path, capture_output=True)

            # .gitignore ekle
            gitignore_content = """# Flutter
.dart_tool/
.packages
build/
*.iml

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""
            with open(f"{local_path}/.gitignore", "w") as f:
                f.write(gitignore_content)

            # Git config
            subprocess.run(
                ["git", "config", "user.email", "ai@orchestral.dev"],
                cwd=local_path, capture_output=True
            )
            subprocess.run(
                ["git", "config", "user.name", "Orchestral AI"],
                cwd=local_path, capture_output=True
            )

            # Add all files
            subprocess.run(["git", "add", "-A"], cwd=local_path, capture_output=True)

            # Commit
            full_message = f"""{commit_message}

🤖 Generated with Orchestral AI Mobile App Generator
https://github.com/{self.username}/mobile-app-orchestral
"""
            subprocess.run(
                ["git", "commit", "-m", full_message],
                cwd=local_path, capture_output=True
            )

            # Remote ekle
            subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                cwd=local_path, capture_output=True
            )

            # Push
            result = subprocess.run(
                ["git", "push", "-u", "origin", "main", "--force"],
                cwd=local_path, capture_output=True, text=True
            )

            # main branch yoksa master dene
            if result.returncode != 0:
                subprocess.run(
                    ["git", "branch", "-M", "main"],
                    cwd=local_path, capture_output=True
                )
                result = subprocess.run(
                    ["git", "push", "-u", "origin", "main", "--force"],
                    cwd=local_path, capture_output=True, text=True
                )

            if result.returncode == 0:
                return {
                    "success": True,
                    "url": f"https://github.com/{self.username}/{repo_name}",
                    "message": "Kod başarıyla yüklendi"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_readme(self, project_path: str, app_info: Dict) -> None:
        """Proje için README.md oluşturur"""
        readme_content = f"""# {app_info.get('name', 'Flutter App')}

{app_info.get('description', 'AI tarafından üretilmiş mobil uygulama')}

## 📱 Hakkında

**Kategori:** {app_info.get('category', 'Genel')}

**Hedef Kitle:** {app_info.get('target_audience', 'Herkes')}

## ✨ Özellikler

{chr(10).join(f"- {f}" for f in app_info.get('features', ['Temel özellikler']))}

## 🚀 Kurulum

```bash
# Bağımlılıkları yükle
flutter pub get

# Uygulamayı çalıştır
flutter run
```

## 🧪 Testler

```bash
flutter test
```

## 📁 Proje Yapısı

```
lib/
├── main.dart          # Ana giriş noktası
├── screens/           # Ekranlar
├── widgets/           # Özel widget'lar
└── models/            # Veri modelleri
```

## 🤖 Oluşturan

Bu uygulama **Orchestral AI Mobile App Generator** tarafından otomatik olarak oluşturulmuştur.

---

**Generated with ❤️ by AI**
"""
        with open(f"{project_path}/README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

    def cleanup(self, path: str) -> None:
        """Geçici klasörü temizler"""
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except:
            pass
