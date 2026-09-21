# Contrato de instalação

O Kit Entusiasta OS é o repositório-base. A instalação cria ou orienta a criação de
um workspace separado, que pertence ao usuário.

## Regras

1. O repositório-base não recebe dados pessoais do usuário.
2. O workspace gerado deve ser privado por padrão.
3. Contexto, marca, conteúdo, biblioteca e projetos pertencem ao usuário.
4. Atualizações do kit não sobrescrevem arquivos pessoais sem revisão explícita.
5. Ações externas ficam bloqueadas no núcleo.
6. Módulos opcionais precisam declarar o que acessam e o que podem alterar.
7. O histórico do repositório-base não pode conter material privado usado como exemplo.
8. O instalador recusa uma pasta não vazia que não reconheça como workspace do kit.
9. Uma nova execução preserva arquivos existentes e informa o que não alterou.

## Separação de propriedade

```text
Kit Entusiasta OS                 Workspace da pessoa
------------------                ----------------------
core/                             _contexto/
templates/                        marca/
checks/                           biblioteca/
docs/                             conteúdo/
AGENTS.md                         projetos/
```

O kit fornece estrutura e procedimentos. A pessoa fornece identidade, decisões,
referências e trabalho real.

## Estrutura gerada

O material estável do kit fica em `_sistema/`. O contexto e as áreas de trabalho ficam
fora dele e pertencem à pessoa. Essa separação permite evoluir o kit sem confundir
arquivos administrados com memória pessoal.
