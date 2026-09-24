# Checklist antes de distribuir

## Conteúdo

- [x] Não há nomes, e-mails, telefones ou caminhos pessoais.
- [x] Não há tokens, chaves, cookies ou credenciais.
- [x] Não há posts, projetos, marcas ou arquivos reais do autor.
- [x] Não há hooks com caminhos absolutos da máquina do autor.
- [x] Exemplos são sintéticos e claramente identificados.
- [x] Dependências de terceiros foram revisadas.

## Instalação

- [x] O onboarding automatizado funciona em uma pasta limpa.
- [x] Uma segunda execução não sobrescreve dados do usuário.
- [ ] O fluxo interativo foi testado por uma pessoa fora do projeto.

## Como reverificar

Rodar na raiz do repositório. Saída vazia é o resultado esperado.

Este arquivo cita os próprios padrões que procura, então ele fica de fora das
varreduras com `':!checks/PRIVACIDADE.md'`. Sem isso, o checklist se acusa sozinho.

```bash
# nomes, e-mails e telefones
git grep -rInE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\+?55 ?\(?[0-9]{2}\)?" -- . ':!checks/PRIVACIDADE.md'

# tokens, chaves e credenciais
git grep -rInE "sk-[A-Za-z0-9]{8,}|ghp_|github_pat_|xox[baprs]-|AIza[0-9A-Za-z_-]{10,}|BEGIN (RSA|OPENSSH|PRIVATE)" -- . ':!checks/PRIVACIDADE.md'

# caminhos absolutos da máquina
git grep -rInE "/Users/|/home/[a-z]|C:\\\\Users" -- . ':!checks/PRIVACIDADE.md'

# hooks e scripts executáveis rastreados
git ls-files | grep -iE "hook|\.sh$|\.ps1$|settings.json"

# dependências externas (esperado: apenas biblioteca padrão do Python)
git grep -rInE "^import |^from |require\(|pip install" -- '*.py'
```

## Último passe

Verificado em 24/09/2026 no commit inicial (`10eae85`), com os comandos acima.
Nenhuma ocorrência em nenhuma das cinco varreduras, nenhum hook ou script shell
rastreado, e `instalar.py` e `tests/test_instalador.py` importando apenas a
biblioteca padrão do Python.

O único item aberto é o teste do fluxo interativo com uma pessoa fora do projeto.
Ele não pode ser fechado por varredura: depende de observar alguém instalando do
zero e anotar onde trava.
