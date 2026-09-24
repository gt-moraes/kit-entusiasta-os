# Kit Entusiasta OS

Um ponto de partida para construir um workspace pessoal de trabalho com IA.

![status](https://img.shields.io/badge/status-prot%C3%B3tipo-orange)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-brightgreen)
![licença](https://img.shields.io/badge/licen%C3%A7a-MIT-lightgrey)

O kit ajuda a organizar contexto, preferências, processos, referências e projetos
em arquivos simples, portáveis e auditáveis. Ele não entrega a identidade, o negócio
ou o conteúdo de outra pessoa: cada instalação começa vazia e é preenchida pelo dono.

## Em 30 segundos

```bash
git clone https://github.com/gt-moraes/kit-entusiasta-os.git
cd kit-entusiasta-os
python3 instalar.py --destino ../meu-workspace
```

O instalador faz o onboarding pergunta por pergunta e monta o workspace na pasta que
você indicar. Sem `pip install`, sem Node, sem conta em lugar nenhum: só a biblioteca
padrão do Python.

## O que ele não faz

Deixar isso claro economiza o seu tempo:

- Não publica, não envia mensagem, não faz deploy e não conecta contas. Ações externas
  ficam fora do núcleo e exigem módulos opt-in.
- Não traz conteúdo, marca ou projeto de ninguém. Os exemplos são fictícios.
- Não sobrescreve o que você escreveu. Uma segunda execução preserva os seus arquivos.
- Não é um framework de landing page nem de marketing. O caso de uso é seu.

## Estado

Protótipo executável. A estrutura ainda está sendo validada com pessoas reais antes de
qualquer publicação ou promessa de compatibilidade ampla.

O checklist de privacidade em [`checks/PRIVACIDADE.md`](checks/PRIVACIDADE.md) traz o
que já foi verificado e o que continua aberto, com os comandos para reverificar.

Leia [`docs/visao-do-produto.md`](docs/visao-do-produto.md) para entender o escopo e
[`docs/contrato-de-instalacao.md`](docs/contrato-de-instalacao.md) para entender a
separação entre o kit e o workspace de cada pessoa.

## Princípios

- O workspace pertence ao usuário.
- Contexto explícito é melhor que contexto presumido.
- O agente pergunta antes de criar decisões importantes.
- Arquivos pessoais não são sobrescritos por atualizações do kit.
- Ações externas ficam fora do núcleo e exigem módulos opt-in.

## Começar

O instalador usa apenas a biblioteca padrão do Python e cria o workspace em outra pasta:

```bash
python3 instalar.py --destino ../meu-entusiasta-os
```

Ele faz as perguntas do onboarding uma por vez. Para testar sem interação:

```bash
python3 instalar.py \
  --destino /tmp/meu-entusiasta-os \
  --respostas examples/respostas.exemplo.json
```

O instalador recusa pastas não vazias que não tenham sido criadas pelo kit e preserva
todos os arquivos existentes numa segunda execução.

Para rodar a validação local:

```bash
python3 -m unittest discover -s tests -v
```

## Estrutura

| Pasta | O que é |
| --- | --- |
| `core/contexto/` | Os arquivos de contexto que o agente lê em toda sessão |
| `core/workflows/` | Os processos: iniciar, atualizar, novo projeto, fechar sessão |
| `templates/` | Modelos de arquivo para o usuário preencher |
| `docs/` | Visão do produto e contrato de instalação |
| `checks/` | Checklist de privacidade antes de distribuir |
| `examples/` | Exemplo fictício de respostas do onboarding |
| `tests/` | Validação do instalador |

## Licença

MIT.
