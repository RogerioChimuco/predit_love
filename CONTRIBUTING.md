# 🤝 Guia de Contribuição

Obrigado pelo interesse em contribuir para o **Predit Love**! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Funcionalidades](#sugerir-funcionalidades)
- [Pull Requests](#pull-requests)
- [Convenções de Código](#convenções-de-código)
- [Configuração de Desenvolvimento](#configuração-de-desenvolvimento)

---

## 📜 Código de Conduta

Este projeto adere a um código de conduta. Ao participar, espera-se que mantenhas este código:

- **Seja respeitoso** com todos os contribuidores
- **Seja construtivo** nas críticas e feedback
- **Seja inclusivo** — todos são bem-vindos
- **Foca no que é melhor** para a comunidade

---

## 🚀 Como Contribuir

### 1. Fork o Repositório

```bash
# Via GitHub CLI
gh repo fork RogerioChimuco/predit_love --clone

# Ou manualmente
git clone https://github.com/SEU_USERNAME/predit_love.git
cd predit_love
git remote add upstream https://github.com/RogerioChimuco/predit_love.git
```

### 2. Configura o Ambiente

```bash
# Criar ambiente virtual
uv venv
source .venv/bin/activate

# Instalar dependências
uv pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com tua GEMINI_API_KEY
```

### 3. Cria uma Branch

```bash
# Atualizar master
git checkout master
git pull upstream master

# Criar branch para a feature/fix
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
```

### 4. Faz as Alterações

- Escreve código limpo e legível
- Adiciona/atualiza testes se necessário
- Atualiza documentação se necessário

### 5. Commit e Push

```bash
# Adicionar alterações
git add .

# Commit com mensagem convencional
git commit -m "feat: adiciona nova funcionalidade X"

# Push para o teu fork
git push origin feature/nome-da-feature
```

### 6. Abre um Pull Request

- Vai ao GitHub e clica em "New Pull Request"
- Descreve claramente as alterações
- Referencia issues relacionadas

---

## 🐛 Reportar Bugs

Antes de reportar um bug:

1. **Verifica** se já não foi reportado nas [Issues](https://github.com/RogerioChimuco/predit_love/issues)
2. **Testa** com a versão mais recente

### Template de Bug Report

```markdown
## Descrição do Bug
Uma descrição clara e concisa do bug.

## Passos para Reproduzir
1. Vai a '...'
2. Clica em '...'
3. Vê o erro

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que acontece de facto.

## Screenshots
Se aplicável, adiciona screenshots.

## Ambiente
- OS: [ex: Ubuntu 22.04]
- Python: [ex: 3.11.5]
- Versão: [ex: 2.0.0]
```

---

## 💡 Sugerir Funcionalidades

### Template de Feature Request

```markdown
## Problema
Descrição do problema que esta feature resolve.

## Solução Proposta
Descrição clara da solução desejada.

## Alternativas Consideradas
Outras soluções que consideraste.

## Contexto Adicional
Qualquer outro contexto relevante.
```

---

## 🔀 Pull Requests

### Checklist antes de submeter

- [ ] Código segue as convenções do projeto
- [ ] Testes passam localmente
- [ ] Documentação atualizada (se necessário)
- [ ] Commit messages seguem Conventional Commits
- [ ] Branch está atualizada com master

### Processo de Review

1. Um maintainer vai rever o PR
2. Pode haver pedidos de alterações
3. Depois de aprovado, será merged

---

## 📝 Convenções de Código

### Python

- **Style Guide**: PEP 8
- **Type Hints**: Usar sempre que possível
- **Docstrings**: Google style
- **Max line length**: 100 caracteres

```python
def calcular_compatibilidade(nome1: str, nome2: str) -> int:
    """
    Calcula a compatibilidade entre dois nomes.

    Args:
        nome1: Primeiro nome.
        nome2: Segundo nome.

    Returns:
        Score de compatibilidade (0-100).
    """
    pass
```

### Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo | Descrição |
|------|-----------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (não afeta código) |
| `refactor` | Refatoração |
| `test` | Testes |
| `chore` | Manutenção |
| `perf` | Performance |

**Exemplos:**

```bash
feat: adiciona endpoint de health check
fix: corrige validação de score negativo
docs: atualiza README com exemplos de API
refactor: extrai lógica de prompt para módulo separado
```

### Branches

| Prefixo | Uso |
|---------|-----|
| `feature/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `docs/` | Documentação |
| `refactor/` | Refatoração |
| `hotfix/` | Correção urgente |

---

## 🛠️ Configuração de Desenvolvimento

### Ferramentas Recomendadas

- **Editor**: VS Code com extensões Python
- **Linter**: ruff
- **Formatter**: black
- **Type Checker**: pyright

### Scripts Úteis

```bash
# Rodar servidor de desenvolvimento
python main.py

# Verificar tipos
pyright main.py

# Formatar código
black .

# Lint
ruff check .
```

### Testes

```bash
# Rodar testes (quando implementados)
pytest

# Com coverage
pytest --cov=.
```

---

## 📞 Dúvidas?

Se tens dúvidas sobre contribuição:

1. Abre uma [Discussion](https://github.com/RogerioChimuco/predit_love/discussions)
2. Entra em contacto via GitHub

---

<p align="center">
  Obrigado por contribuir! 💕
</p>
