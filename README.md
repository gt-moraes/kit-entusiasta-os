# Kit Entusiasta OS

Um ponto de partida para construir um workspace pessoal de trabalho com IA.

O kit ajuda a organizar contexto, preferências, processos, referências e projetos
em arquivos simples, portáveis e auditáveis. Ele não entrega a identidade, o negócio
ou o conteúdo de outra pessoa: cada instalação começa vazia e é preenchida pelo dono.

## Estado

Protótipo executável. A estrutura ainda está sendo validada com pessoas reais antes de
qualquer publicação ou promessa de compatibilidade ampla.

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
