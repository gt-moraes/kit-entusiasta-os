# Roteiro: teste do fluxo interativo com uma pessoa de fora

Fecha o último item aberto de `checks/PRIVACIDADE.md`.

## Quem convidar

Uma pessoa só, com duas características:

- Consegue abrir um terminal e rodar um comando colado. Não precisa programar.
- Não sabe o que é este projeto. Se já ouviu você explicar, o teste perde a graça.

Se a pessoa programa todo dia, ela contorna os problemas sem perceber e você não
aprende nada. O alvo é quem trava de verdade.

## Antes

Mande **só isto**, sem nenhuma explicação a mais:

> Dá uma olhada nesse repositório e tenta instalar? Queria ver se dá pra usar sem eu explicar nada.
> https://github.com/gt-moraes/kit-entusiasta-os

Combine de fazer junto, por chamada com tela compartilhada. O valor está em ver
onde ela para, não no resultado final.

## Durante

**A regra que importa: fique calado.** Toda vez que você explicar algo, você
apagou a evidência. Se ela travar, deixe travar. Anote e siga.

Só quebre o silêncio se ela desistir de vez. Aí pergunte: "o que você esperava
que acontecesse?" e anote a resposta antes de ajudar.

Marque o relógio em três momentos:

| Momento | Tempo |
| --- | --- |
| Abriu o repositório e entendeu o que é | |
| Rodou o instalador pela primeira vez | |
| Terminou o onboarding | |

Anote também:

- Onde ela hesitou antes de clicar ou digitar.
- Qual pergunta do onboarding ela leu duas vezes.
- Qual pergunta ela respondeu com algo vago tipo "sei lá" ou "qualquer coisa".
- Qualquer momento em que ela pediu confirmação: "é aqui?", "é isso mesmo?".
- Se ela achou o `COMECE-AQUI.md` sozinha no fim.

## As cinco perguntas do fim

Faça nesta ordem, e anote a resposta em palavras dela, sem resumir:

1. Sem olhar a tela: o que esse negócio faz?
2. Teve alguma hora que você não soube o que responder? Qual?
3. Teve alguma hora que você achou que ia quebrar algo?
4. O que você faria agora, se eu não estivesse aqui?
5. Você usaria isso de novo? Por quê?

A pergunta 1 mede se o README funciona. A 3 mede confiança. A 4 é a mais
importante: se a resposta for "sei lá, fechava", o `COMECE-AQUI.md` falhou.

## Como ler o resultado

- **Travou no README** → o problema é a explicação, não o código.
- **Travou no comando** → o quickstart precisa de mais contexto (onde rodar, o que é `--destino`).
- **Respondeu vago numa pergunta do onboarding** → a pergunta está mal formulada. Anote qual.
- **Terminou e não soube o que fazer** → o `COMECE-AQUI.md` precisa de um primeiro passo concreto.

Uma pessoa já entrega muita coisa. Duas ou três, se der, mostram o que é padrão
e o que era só daquela pessoa.

## Depois

Anote o resultado, corrija o que apareceu, e só então marque em
`checks/PRIVACIDADE.md`:

```
- [x] O fluxo interativo foi testado por uma pessoa fora do projeto.
```
