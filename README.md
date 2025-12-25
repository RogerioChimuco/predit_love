# 💕 Predit Love API

> API de compatibilidade amorosa com inteligência artificial — transforma dados em poesia romântica.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Sobre o Projeto

**Predit Love** é uma API que recebe dados de múltiplos algoritmos de compatibilidade (FLAMES, Letras, Numerologia Pitagórica, Astrologia e TrueLove) e gera frases poéticas, místicas e intensamente românticas usando **Google Gemini AI**.

A API foi desenvolvida para o app **Mi and You** — uma aplicação mobile de compatibilidade amorosa.

### ✨ Características

- 🔮 **5 Algoritmos de Compatibilidade**: FLAMES, Letras, Horóscopo, Numerologia e TrueLove
- 🤖 **IA Generativa**: Google Gemini 2.5 Flash para frases poéticas
- 🇦🇴 **Toque Angolano**: Linguagem natural com gírias angolanas leves
- ⚡ **Serverless**: Deploy na Vercel com cold start rápido
- 🔒 **Sem Exposição de Dados**: Nunca revela scores, percentagens ou métodos

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                      Flutter App                            │
│                    (Mi and You)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ POST /generate-phrase
                      │ JSON Payload (5 algoritmos)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Vercel Edge Network                       │
│                    (Serverless)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Pydantic Models (validação de tipos)               │   │
│  │  - CompatibilityRequest                             │   │
│  │  - LettersAlgorithm, FlamesAlgorithm                │   │
│  │  - HoroscopeAlgorithm, PythagoreanAlgorithm         │   │
│  │  - TrueLoveAlgorithm                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Prompt Engineering                                 │   │
│  │  - Prioriza Amor/Casamento                         │   │
│  │  - Transforma dados em contexto poético            │   │
│  │  - Regras de interpretação astrológica             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Google Gemini AI                           │
│               (gemini-2.5-flash-lite)                       │
│                                                             │
│  Input: Contexto estruturado dos 5 algoritmos               │
│  Output: 1-2 frases poéticas românticas                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
predit_love/
├── api/
│   └── index.py          # Entry point para Vercel (serverless)
├── main.py               # Lógica principal da API FastAPI
├── requirements.txt      # Dependências Python
├── vercel.json           # Configuração de deploy Vercel
├── pyproject.toml        # Configuração do projeto Python
├── .gitignore            # Ficheiros ignorados pelo Git
├── .env.example          # Exemplo de variáveis de ambiente
├── API_UPDATE_GUIDE.md   # Guia de atualização da API
├── LICENSE               # Licença MIT
├── CONTRIBUTING.md       # Guia de contribuição
└── README.md             # Este ficheiro
```

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recomendado) ou pip
- Chave de API do [Google AI Studio](https://aistudio.google.com/apikey)

### Instalação Local

```bash
# Clonar o repositório
git clone https://github.com/RogerioChimuco/predit_love.git
cd predit_love

# Criar ambiente virtual e instalar dependências
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar GEMINI_API_KEY

# Rodar servidor local
python main.py
```

A API estará disponível em `http://localhost:8000`

### Testar a API

```bash
curl -X POST http://localhost:8000/generate-phrase \
  -H "Content-Type: application/json" \
  -d '{
    "overall_score": 75,
    "same_gender": false,
    "name1": "Rogério",
    "name2": "Maria",
    "letters": {"score": 80, "result_type": "Amor"},
    "flames": {"score": 85, "result_type": "Casamento", "flames_letter": "M"},
    "true_love": {"score": 70, "interests_similarity": 0.8, "personality_similarity": 0.7},
    "horoscope": {"score": 65, "sign1": "Leão", "sign2": "Áries", "element1": "Fogo", "element2": "Fogo", "same_element": true},
    "pythagorean": {"score": 72, "destiny1": 7, "destiny2": 2, "relationship_number": 9, "relationship_meaning": "Amor Universal"}
  }'
```

---

## 📡 API Reference

### `POST /generate-phrase`

Gera uma frase poética de compatibilidade.

#### Request Body

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `overall_score` | int | ✅ | Score geral de compatibilidade (0-100) |
| `same_gender` | bool | ✅ | Se o casal é do mesmo género |
| `name1` | string | ✅ | Nome da primeira pessoa |
| `name2` | string | ✅ | Nome da segunda pessoa |
| `letters` | object | ✅ | Resultado do algoritmo de Letras |
| `flames` | object | ✅ | Resultado do algoritmo FLAMES |
| `true_love` | object | ✅ | Resultado do algoritmo TrueLove |
| `horoscope` | object | ✅ | Resultado do algoritmo de Horóscopo |
| `pythagorean` | object | ✅ | Resultado do algoritmo Pitagórico |

<details>
<summary>📋 Schema completo dos algoritmos</summary>

```typescript
interface LettersAlgorithm {
  score: number;
  result_type?: "Amor" | "Paixão" | "Amizade" | "Ódio";
  total_remaining?: number;
  remainder?: number;
}

interface FlamesAlgorithm {
  score: number;
  result_type?: "Amizade" | "Amor" | "Afeição" | "Casamento" | "Inimizade" | "Irmãos";
  flames_letter?: "F" | "L" | "A" | "M" | "E" | "S";
  count?: number;
}

interface TrueLoveAlgorithm {
  score: number;
  interests_similarity?: number;  // 0.0 - 1.0
  personality_similarity?: number;
  location_similarity?: number;
  age_similarity?: number;
}

interface HoroscopeAlgorithm {
  score: number;
  sign1?: string;
  sign2?: string;
  element1?: "Fogo" | "Terra" | "Ar" | "Água";
  element2?: "Fogo" | "Terra" | "Ar" | "Água";
  quality1?: "Cardinal" | "Fixo" | "Mutável";
  quality2?: "Cardinal" | "Fixo" | "Mutável";
  same_element?: boolean;
  aspect_analysis?: string;
}

interface PythagoreanAlgorithm {
  score: number;
  destiny1?: number;  // 1-9
  destiny2?: number;
  meaning1?: string;
  meaning2?: string;
  relationship_number?: number;
  relationship_meaning?: string;
}
```

</details>

#### Response

```json
{
  "phrase": "Entre Rogério e Maria há uma aliança que fala de lar e eternidade — caminham com o pacto escrito nas estrelas. ✨"
}
```

---

## 🌐 Deploy na Vercel

### Via Dashboard

1. Fork ou clone este repositório
2. Vai a [vercel.com](https://vercel.com) e faz login com GitHub
3. Clica **"Add New Project"**
4. Seleciona o repositório **predit_love**
5. Nas **Environment Variables**, adiciona:
   - `GEMINI_API_KEY` = tua chave da API do Google Gemini
6. Clica **Deploy**

### Via CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd predit_love
vercel --prod
```

---

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|----------|-------------|-----------|
| `GEMINI_API_KEY` | ✅ | Chave de API do Google AI Studio |

### Obter Chave do Gemini

1. Vai a [Google AI Studio](https://aistudio.google.com/apikey)
2. Clica **"Create API Key"**
3. Copia a chave gerada
4. Adiciona ao `.env` ou às variáveis de ambiente da Vercel

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, lê o [CONTRIBUTING.md](CONTRIBUTING.md) antes de submeter PRs.

### Como Contribuir

1. Fork o projeto
2. Cria uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit as mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abre um Pull Request

### Convenções de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` manutenção

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** — vê o ficheiro [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Rogério Chimuco**

- GitHub: [@RogerioChimuco](https://github.com/RogerioChimuco)

---

## 🙏 Agradecimentos

- [Google Gemini](https://ai.google.dev/) pela API de IA generativa
- [FastAPI](https://fastapi.tiangolo.com/) pelo framework web
- [Vercel](https://vercel.com/) pelo hosting serverless

---

<p align="center">
  Feito com 💕 em Angola
</p>
