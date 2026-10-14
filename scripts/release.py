"""Script d'automatisation de release pour Learnio.

Vérifie l'état du dépôt, la conformité du code, exécute les tests,
construit les packages de distribution et crée le tag git associé.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def run_command(cmd: list[str], cwd: Path = ROOT_DIR) -> None:
    """Exécute une commande shell et lève une exception en cas d'erreur."""
    print(f"--> Exécution : {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if result.returncode != 0:
        print(f"[ERREUR] Échec de la commande : {' '.join(cmd)}", file=sys.stderr)
        sys.exit(result.returncode)


def get_current_version() -> str:
    """Extrait la version actuelle depuis src/__version__.py."""
    version_file = ROOT_DIR / "src" / "__version__.py"
    content = version_file.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        print(
            f"[ERREUR] Impossible de trouver __version__ dans {version_file}",
            file=sys.stderr,
        )
        sys.exit(1)
    return match.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Automatisation des releases Learnio")
    parser.add_argument(
        "--version",
        "-v",
        help="Version à releaser (par défaut celle de src/__version__.py)",
        default=None,
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Ignorer l'exécution des tests (déconseillé)",
    )
    parser.add_argument(
        "--create-tag",
        action="store_true",
        help="Créer automatiquement le tag git et le pousser",
    )
    args = parser.parse_args()

    version = args.version or get_current_version()
    print(f"=== Préparation de la release v{version} ===")

    # 1. Vérification de la syntaxe et compilation bytecode
    print("\n[1/5] Compilation du bytecode Python...")
    run_command(["uv", "run", "python", "-m", "compileall", "src", "tests"])

    # 2. Vérification Ruff (linter et formatage)
    print("\n[2/5] Vérification du style et du formatage (Ruff)...")
    run_command(["uv", "run", "ruff", "check", "src", "tests"])
    run_command(["uv", "run", "ruff", "format", "--check", "src", "tests"])

    # 3. Exécution de la suite de tests
    if not args.skip_tests:
        print("\n[3/5] Exécution de la suite de tests (pytest)...")
        run_command(["uv", "run", "pytest", "-v", "--tb=short"])
    else:
        print("\n[3/5] Tests ignorés (--skip-tests).")

    # 4. Construction des archives de distribution
    print("\n[4/5] Construction du package de distribution (uv build)...")
    run_command(["uv", "build"])

    # 5. Tag git optionnel
    tag_name = f"v{version}"
    if args.create_tag:
        print(f"\n[5/5] Création et envoi du tag git {tag_name}...")
        run_command(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"])
        run_command(["git", "push", "upstream", tag_name])
        print(f"\nRelease {tag_name} publiée avec succès !")
    else:
        print("\n[5/5] Pour créer et pousser le tag git manuellement :")
        print(f'  git tag -a {tag_name} -m "Release {tag_name}"')
        print(f"  git push upstream {tag_name}")

    print("\nValidation de la release terminée avec succès !")


if __name__ == "__main__":
    main()
