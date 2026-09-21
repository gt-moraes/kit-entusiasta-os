from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "instalar.py"
EXAMPLE = ROOT / "examples/respostas.exemplo.json"


def tree_hash(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class InstallerTest(unittest.TestCase):
    def run_installer(self, destination: Path, answers: Path = EXAMPLE) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                "--destino",
                str(destination),
                "--respostas",
                str(answers),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_creates_private_minimal_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "workspace"
            result = self.run_installer(destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((destination / "AGENTS.md").exists())
            self.assertTrue((destination / "_contexto/pessoa.md").exists())
            self.assertTrue((destination / "_sistema/workflows/iniciar.md").exists())
            self.assertTrue((destination / "projetos/README.md").exists())
            self.assertTrue((destination / "biblioteca/README.md").exists())
            self.assertFalse((destination / "conteudo").exists())
            self.assertFalse((destination / "marca").exists())
            agents = (destination / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Ações externas permanecem bloqueadas", agents)

    def test_second_run_preserves_every_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "workspace"
            first = self.run_installer(destination)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = tree_hash(destination)
            second = self.run_installer(destination)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(before, tree_hash(destination))
            self.assertIn("Arquivos novos: 0", second.stdout)

    def test_unknown_answers_become_questions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            answers_path = base / "answers.json"
            answers_path.write_text(json.dumps({"areas": []}), encoding="utf-8")
            destination = base / "workspace"
            result = self.run_installer(destination, answers_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            questions = (destination / "_contexto/perguntas-em-aberto.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Qual é o nome do dono deste workspace?", questions)
            person = (destination / "_contexto/pessoa.md").read_text(encoding="utf-8")
            self.assertNotIn("- Nome:", person)

    def test_generated_workflows_reference_installed_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "workspace"
            result = self.run_installer(destination)
            self.assertEqual(result.returncode, 0, result.stderr)

            iniciar = (destination / "_sistema/workflows/iniciar.md").read_text(
                encoding="utf-8"
            )
            novo_projeto = (
                destination / "_sistema/workflows/novo-projeto.md"
            ).read_text(encoding="utf-8")

            self.assertIn("`_contexto/`", iniciar)
            self.assertNotIn("`core/contexto/`", iniciar)
            self.assertIn(
                "`_sistema/templates/projetos/COMECE-AQUI.md`", novo_projeto
            )
            self.assertNotIn("`templates/projetos/COMECE-AQUI.md`", novo_projeto)

    def test_refuses_unrelated_non_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "workspace"
            destination.mkdir()
            (destination / "arquivo-do-usuario.txt").write_text("preservar", encoding="utf-8")
            result = self.run_installer(destination)
            self.assertEqual(result.returncode, 2)
            self.assertIn("não está vazio", result.stderr)
            self.assertEqual(
                (destination / "arquivo-do-usuario.txt").read_text(encoding="utf-8"),
                "preservar",
            )


if __name__ == "__main__":
    unittest.main()
