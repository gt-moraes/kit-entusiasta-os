#!/usr/bin/env python3
"""Instalador local do Kit Entusiasta OS.

O instalador cria um workspace novo sem enviar dados para serviços externos e sem
sobrescrever arquivos pessoais. A biblioteca padrão do Python é suficiente.
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


KIT_ROOT = Path(__file__).resolve().parent
KIT_VERSION = "0.1.0"
STATE_PATH = Path("_sistema/instalacao.json")


@dataclass(frozen=True)
class Question:
    key: str
    prompt: str
    open_question: str


QUESTIONS = (
    Question("name", "Qual é o seu nome?", "Qual é o nome do dono deste workspace?"),
    Question(
        "preferred_name",
        "Como você prefere ser tratado pelo agente?",
        "Como o dono prefere ser tratado pelo agente?",
    ),
    Question(
        "building",
        "O que você está tentando construir ou melhorar agora?",
        "O que a pessoa está tentando construir ou melhorar agora?",
    ),
    Question(
        "work_types",
        "Que tipo de trabalho este workspace precisa organizar?",
        "Que tipo de trabalho este workspace precisa organizar?",
    ),
    Question(
        "audience",
        "Quem usa, recebe ou é impactado por esse trabalho?",
        "Quem usa, recebe ou é impactado por esse trabalho?",
    ),
    Question(
        "tools",
        "Quais ferramentas e ambientes você já usa?",
        "Quais ferramentas e ambientes já fazem parte do trabalho?",
    ),
    Question(
        "autonomous_decisions",
        "Que decisões o agente pode tomar sozinho?",
        "Quais decisões o agente pode tomar sozinho?",
    ),
    Question(
        "confirm_decisions",
        "Que ações ou decisões sempre precisam da sua confirmação?",
        "Quais ações ou decisões sempre precisam de confirmação?",
    ),
    Question(
        "quality",
        "Como você reconhece uma boa entrega?",
        "Como uma boa entrega é reconhecida?",
    ),
    Question(
        "references_restrictions",
        "Quais referências, restrições ou preferências precisam ser lembradas?",
        "Quais referências, restrições ou preferências precisam ser lembradas?",
    ),
)

AREA_ALIASES = {
    "projeto": "projetos",
    "projetos": "projetos",
    "biblioteca": "biblioteca",
    "referencia": "biblioteca",
    "referencias": "biblioteca",
    "conteudo": "conteudo",
    "conteudos": "conteudo",
    "marca": "marca",
    "design": "marca",
}
AREA_ORDER = ("projetos", "biblioteca", "conteudo", "marca")


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def clean(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def normalize_areas(raw: Any) -> list[str]:
    if raw is None or raw == "":
        return ["projetos", "biblioteca"]
    values = raw if isinstance(raw, list) else str(raw).split(",")
    normalized: set[str] = set()
    invalid: list[str] = []
    for value in values:
        key = strip_accents(clean(value).lower())
        if not key:
            continue
        area = AREA_ALIASES.get(key)
        if area is None:
            invalid.append(str(value))
        else:
            normalized.add(area)
    if invalid:
        allowed = ", ".join(AREA_ORDER)
        raise ValueError(f"Áreas desconhecidas: {', '.join(invalid)}. Use: {allowed}.")
    return [area for area in AREA_ORDER if area in normalized]


def ask_questions() -> dict[str, Any]:
    print("\nKit Entusiasta OS — onboarding local\n")
    answers: dict[str, Any] = {}
    for question in QUESTIONS:
        answers[question.key] = input(f"{question.prompt}\n> ").strip()
        print()
    areas = input(
        "Quais áreas fazem sentido agora?\n"
        "Opções: projetos, biblioteca, conteúdo, marca.\n"
        "Pressione Enter para usar projetos e biblioteca.\n> "
    )
    answers["areas"] = normalize_areas(areas)
    return answers


def load_answers(path: Path | None) -> dict[str, Any]:
    if path is None:
        return ask_questions()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Arquivo de respostas não encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("O arquivo de respostas precisa conter um objeto JSON.")
    answers = {question.key: clean(data.get(question.key)) for question in QUESTIONS}
    answers["areas"] = normalize_areas(data.get("areas"))
    return answers


def answered_line(label: str, value: Any) -> str | None:
    text = clean(value)
    return f"- {label}: {text}" if text else None


def section(title: str, lines: list[str | None]) -> str:
    present = [line for line in lines if line]
    body = "\n".join(present) if present else "Nenhuma informação confirmada ainda."
    return f"# {title}\n\n{body}\n"


def open_questions(answers: dict[str, Any]) -> list[str]:
    return [q.open_question for q in QUESTIONS if not clean(answers.get(q.key))]


def render_files(answers: dict[str, Any]) -> dict[Path, str]:
    areas = answers["areas"]
    questions = open_questions(answers)
    today = datetime.now().astimezone().date().isoformat()
    name = clean(answers.get("preferred_name")) or clean(answers.get("name")) or "dono"
    files: dict[Path, str] = {
        Path("AGENTS.md"): f"""# Sistema operacional pessoal de {name}

## Como operar

- Leia `_contexto/` antes de iniciar trabalho relevante.
- Trate informações ausentes como perguntas, nunca como fatos.
- Preserve edições manuais e mostre o diff antes de alterar contexto existente.
- Pergunte antes de decisões importantes ou mudanças estruturais.
- Não publique, envie mensagens, faça deploy, compre, apague ou conecte contas sem autorização explícita.
- Ações externas permanecem bloqueadas por padrão.

## Propriedade

Este workspace pertence ao usuário. Arquivos de `_contexto/`, `marca/`, `conteudo/`,
`biblioteca/` e `projetos/` são pessoais. O material administrado pelo kit fica em
`_sistema/` e nunca deve sobrescrever conteúdo pessoal silenciosamente.

## Primeiro passo em cada sessão

1. Leia `_contexto/estado.md`.
2. Leia apenas o contexto necessário para a tarefa.
3. Confirme a prioridade e as restrições antes de executar mudanças maiores.
""",
        Path("COMECE-AQUI.md"): """# Comece aqui

Seu workspace foi criado pelo Kit Entusiasta OS.

## Agora

1. Revise os arquivos em `_contexto/` e corrija o que não representar você.
2. Responda às perguntas em `_contexto/perguntas-em-aberto.md`.
3. Escolha um trabalho real e pequeno para testar o sistema.

## Três próximos passos

1. Complete o contexto ainda desconhecido.
2. Crie o primeiro projeto usando `_sistema/templates/projetos/COMECE-AQUI.md`.
3. Ao fim da primeira sessão, use `_sistema/workflows/fechar-sessao.md`.

Nenhuma integração, publicação, mensagem ou deploy foi habilitado durante a instalação.
""",
        Path("_contexto/pessoa.md"): section(
            "Pessoa",
            [
                answered_line("Nome", answers.get("name")),
                answered_line("Como prefere ser tratado", answers.get("preferred_name")),
                answered_line("O que está construindo", answers.get("building")),
            ],
        ),
        Path("_contexto/negocio-ou-projeto.md"): section(
            "Negócio ou projeto",
            [
                answered_line("Trabalho que precisa ser organizado", answers.get("work_types")),
                answered_line("Público ou pessoas envolvidas", answers.get("audience")),
                answered_line("Ferramentas usadas", answers.get("tools")),
                answered_line(
                    "Referências, restrições e preferências",
                    answers.get("references_restrictions"),
                ),
            ],
        ),
        Path("_contexto/principios.md"): section(
            "Princípios de trabalho",
            [
                answered_line("Como uma boa entrega é reconhecida", answers.get("quality")),
                answered_line(
                    "Decisões que o agente pode tomar sozinho",
                    answers.get("autonomous_decisions"),
                ),
                answered_line(
                    "Ações ou decisões que exigem confirmação",
                    answers.get("confirm_decisions"),
                ),
                "- Ações externas: Bloqueadas por padrão.",
            ],
        ),
        Path("_contexto/estado.md"): f"""# Estado atual

- Prioridade atual: Validar o primeiro uso real do workspace.
- Projetos em andamento: Nenhum projeto registrado ainda.
- Próxima decisão importante: Escolher o primeiro trabalho pequeno para testar o sistema.
- Pendências: Responder às perguntas em `perguntas-em-aberto.md`.
- Última atualização: {today}
""",
        Path("_contexto/perguntas-em-aberto.md"): "# Perguntas em aberto\n\n"
        + ("\n".join(f"- {question}" for question in questions) if questions else "Nenhuma.")
        + "\n",
        Path("_sistema/manifest.json"): json.dumps(
            {
                "kit": "kit-entusiasta-os",
                "version": KIT_VERSION,
                "managedPaths": ["_sistema/"],
                "userOwnedPaths": [
                    "AGENTS.md",
                    "COMECE-AQUI.md",
                    "_contexto/",
                    "marca/",
                    "conteudo/",
                    "biblioteca/",
                    "projetos/",
                ],
                "externalActionsDefault": "blocked",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        STATE_PATH: json.dumps(
            {
                "kit": "kit-entusiasta-os",
                "version": KIT_VERSION,
                "installedAt": today,
                "selectedAreas": areas,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        Path(".gitignore"): """.env
.env.*
!.env.example
*.pem
*.key
credentials.*
secrets.*
.DS_Store
""",
    }

    for source in sorted((KIT_ROOT / "core/workflows").glob("*.md")):
        files[Path("_sistema/workflows") / source.name] = source.read_text(encoding="utf-8")
    files[Path("_sistema/templates/projetos/COMECE-AQUI.md")] = (
        KIT_ROOT / "templates/projetos/COMECE-AQUI.md"
    ).read_text(encoding="utf-8")

    if "projetos" in areas:
        files[Path("projetos/README.md")] = """# Projetos

Cada projeto deve começar pequeno, com objetivo, restrições e critério de pronto.
Use o modelo em `_sistema/templates/projetos/COMECE-AQUI.md`.
"""
    if "biblioteca" in areas:
        files[Path("biblioteca/README.md")] = """# Biblioteca

Guarde referências e dados junto do motivo pelo qual eles são úteis. Link sem contexto
vira acúmulo e não memória operacional.
"""
    if "conteudo" in areas:
        files[Path("conteudo/ideias.md")] = (
            KIT_ROOT / "templates/conteudo/ideias.md"
        ).read_text(encoding="utf-8")
    if "marca" in areas:
        files[Path("marca/README.md")] = """# Marca

Registre aqui identidade, voz, referências e decisões visuais confirmadas. Não copie a
identidade de outra pessoa como padrão do seu workspace.
"""
    return files


def ensure_target(target: Path) -> None:
    if target.resolve() == KIT_ROOT or KIT_ROOT in target.resolve().parents:
        raise ValueError("O workspace precisa ficar fora do repositório-base do kit.")
    if target.exists():
        entries = list(target.iterdir())
        if entries and not (target / STATE_PATH).exists():
            raise ValueError(
                "O destino não está vazio e não foi criado pelo Kit Entusiasta OS. "
                "Escolha uma pasta vazia."
            )


def install(target: Path, answers: dict[str, Any], dry_run: bool) -> tuple[list[Path], list[Path]]:
    ensure_target(target)
    created: list[Path] = []
    preserved: list[Path] = []
    for relative, content in render_files(answers).items():
        destination = target / relative
        if destination.exists():
            preserved.append(relative)
            continue
        created.append(relative)
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8", newline="\n") as file:
            file.write(content)
    return created, preserved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cria um workspace pessoal a partir do Kit Entusiasta OS."
    )
    parser.add_argument("--destino", required=True, type=Path, help="Pasta do novo workspace.")
    parser.add_argument(
        "--respostas",
        type=Path,
        help="JSON opcional para instalação não interativa.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria criado sem escrever arquivos.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        answers = load_answers(args.respostas)
        created, preserved = install(args.destino.expanduser(), answers, args.dry_run)
    except ValueError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2

    mode = "Simulação concluída" if args.dry_run else "Instalação concluída"
    print(f"\n{mode}: {args.destino.expanduser().resolve()}")
    print(f"Arquivos novos: {len(created)}")
    print(f"Arquivos preservados: {len(preserved)}")
    if created:
        print("\nCriados:")
        for path in created:
            print(f"- {path}")
    if preserved:
        print("\nPreservados sem alteração:")
        for path in preserved:
            print(f"- {path}")
    print("\nPróximo passo: abra COMECE-AQUI.md no workspace gerado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
