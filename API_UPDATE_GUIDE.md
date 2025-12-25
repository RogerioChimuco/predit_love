# 🔧 Guia de Atualização da API FastAPI

## Resumo das Alterações

O Flutter agora envia um payload **enriquecido** com todos os detalhes de cada algoritmo de compatibilidade. Precisas atualizar a API para receber estes dados e usar no prompt do Gemini.

---

## 📦 Novo Payload que o Flutter Envia

```json
{
  "overall_score": 65,
  "same_gender": false,
  "name1": "Rogério Chimuco",
  "name2": "Domilcia Zumba",
  
  "letters": {
    "score": 30,
    "result_type": "Amor",
    "total_remaining": 10,
    "remainder": 2,
    "name1_remaining": "gichmuc",
    "name2_remaining": "dlczb"
  },
  
  "flames": {
    "score": 100,
    "result_type": "Casamento",
    "flames_letter": "M",
    "count": 12,
    "name1_remaining": "gichmuc",
    "name2_remaining": "dlczb"
  },
  
  "true_love": {
    "score": 20,
    "interests_similarity": 0.85,
    "personality_similarity": 0.72,
    "location_similarity": 0.50,
    "age_similarity": 0.90,
    "weights": {"interests": 0.6, "personality": 0.2, "location": 0.1, "age": 0.1}
  },
  
  "horoscope": {
    "score": 75,
    "sign1": "Áries",
    "sign2": "Leão",
    "element1": "Fogo",
    "element2": "Fogo",
    "quality1": "Cardinal",
    "quality2": "Fixo",
    "same_element": true,
    "aspect_analysis": "Trígono (120°) - Excelente harmonia"
  },
  
  "pythagorean": {
    "score": 85,
    "destiny1": 5,
    "destiny2": 7,
    "meaning1": "Liberdade e aventura",
    "meaning2": "Espiritualidade e análise",
    "relationship_number": 3,
    "relationship_meaning": "Comunicação e criatividade"
  }
}
```

---

## ✏️ Alterações no `main.py`

### 1. Substituir os Models Pydantic

Remove o `CompatibilityResult` antigo e adiciona estes novos models:

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# ========== NOVOS MODELS ==========

class LettersAlgorithm(BaseModel):
    score: int
    result_type: Optional[str] = None  # Amor, Paixão, Amizade, Ódio
    total_remaining: Optional[int] = None
    remainder: Optional[int] = None
    name1_remaining: Optional[str] = None
    name2_remaining: Optional[str] = None


class FlamesAlgorithm(BaseModel):
    score: int
    result_type: Optional[str] = None  # Amizade, Amor, Afeição, Casamento, Inimizade, Irmãos
    flames_letter: Optional[str] = None  # F, L, A, M, E, S
    count: Optional[int] = None
    name1_remaining: Optional[str] = None
    name2_remaining: Optional[str] = None


class TrueLoveAlgorithm(BaseModel):
    score: int
    interests_similarity: Optional[float] = None  # 0.0 - 1.0
    personality_similarity: Optional[float] = None
    location_similarity: Optional[float] = None
    age_similarity: Optional[float] = None
    weights: Optional[Dict[str, float]] = None


class HoroscopeAlgorithm(BaseModel):
    score: int
    sign1: Optional[str] = None  # Áries, Touro, Gémeos...
    sign2: Optional[str] = None
    element1: Optional[str] = None  # Fogo, Terra, Ar, Água
    element2: Optional[str] = None
    quality1: Optional[str] = None  # Cardinal, Fixo, Mutável
    quality2: Optional[str] = None
    same_element: Optional[bool] = None
    aspect_analysis: Optional[str] = None


class PythagoreanAlgorithm(BaseModel):
    score: int
    destiny1: Optional[int] = None  # 1-9
    destiny2: Optional[int] = None
    meaning1: Optional[str] = None
    meaning2: Optional[str] = None
    relationship_number: Optional[int] = None
    relationship_meaning: Optional[str] = None


class CompatibilityRequest(BaseModel):
    """Request completo com todos os dados de compatibilidade"""
    overall_score: int
    same_gender: bool
    name1: str
    name2: str
    letters: LettersAlgorithm
    flames: FlamesAlgorithm
    true_love: TrueLoveAlgorithm
    horoscope: HoroscopeAlgorithm
    pythagorean: PythagoreanAlgorithm
```

### 2. Atualizar o Endpoint

```python
@app.post("/generate-phrase", response_model=PhraseResponse)
async def generate_phrase(data: CompatibilityRequest):
    if not GEMINI_API_KEY:
        return PhraseResponse(phrase="O universo conspira a vosso favor!")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Construir contexto enriquecido para o Gemini
        prompt = f"""
# Contexto (INFORMAÇÃO PARA O MODELO — NÃO CITAR NEM EXPLICAR)
# Os dados abaixo guiam o tom e a "certeza" da frase.
# NÃO mencionar percentagens, scores, nomes de técnicas nem detalhes do processamento.

## Dados de Compatibilidade (uso interno):
- Score geral: {data.overall_score}% ({"alta" if data.overall_score >= 70 else "média" if data.overall_score >= 40 else "baixa"})
- Mesmo género: {"sim" if data.same_gender else "não"}

## Astrologia:
- Signos: {data.horoscope.sign1 or "?"} + {data.horoscope.sign2 or "?"}
- Elementos: {data.horoscope.element1 or "?"} + {data.horoscope.element2 or "?"}
- Mesmo elemento: {"sim, harmonia natural" if data.horoscope.same_element else "não, complementares"}
- Aspecto: {data.horoscope.aspect_analysis or "neutro"}

## Numerologia:
- Números do destino: {data.pythagorean.destiny1 or "?"} e {data.pythagorean.destiny2 or "?"}
- Significados: {data.pythagorean.meaning1 or "?"}, {data.pythagorean.meaning2 or "?"}
- Número do relacionamento: {data.pythagorean.relationship_number or "?"} ({data.pythagorean.relationship_meaning or "?"})

## FLAMES:
- Resultado: {data.flames.result_type or "?"} (letra {data.flames.flames_letter or "?"})

## Letras:
- Resultado: {data.letters.result_type or "?"}

## TRUE LOVE (similaridades):
- Interesses em comum: {int((data.true_love.interests_similarity or 0) * 100)}%
- Personalidades: {int((data.true_love.personality_similarity or 0) * 100)}%
- Proximidade: {int((data.true_love.location_similarity or 0) * 100)}%
- Idades compatíveis: {int((data.true_love.age_similarity or 0) * 100)}%

# Instruções de geração
Atue como um astrólogo sábio, divertido e moderno de Angola.
Gere 1–2 frases curtas e inspiradoras sobre a compatibilidade entre {data.name1} e {data.name2}.

- Tonalidade: místico mas contemporâneo; confiante, caloroso, como quem "acertou".
- Linguagem: use gírias angolanas leves quando apropriado; natural e coloquial.
- Estilo: revele o resultado como se fosse mágica — direto, poético, sem explicações técnicas.
- Restrições: NÃO citar scores, percentagens, nem mencionar métodos (horóscopo, numerologia, FLAMES, algoritmos, etc.). NÃO explicar o processo.
- Extras: opcional 1 emoji adequado; evitar clichês batidos; máximo 2 frases.

Exemplos de elementos que PODES usar subtilmente (sem explicar):
- Se mesmo elemento de fogo: mencionar "chama", "fogo", "paixão ardente"
- Se FLAMES = Casamento: tom de compromisso duradouro
- Se numerologia alta: "destino", "escrito nas estrelas"
- Se interesses altos: "almas gémeas", "mesma vibração"
"""

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=0.7,
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents,
            config=generate_content_config,
        )
        
        phrase = response.text.strip()
        return PhraseResponse(phrase=phrase)
                
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        return PhraseResponse(phrase=f"A energia entre {data.name1} e {data.name2} é única e misteriosa!")
```

---

## 🎯 Benefícios do Novo Payload

| Antes | Depois |
|-------|--------|
| Só scores numéricos | Signos reais (Áries, Leão...) |
| `flames_result: "Casamento"` | + letra FLAMES (M) e contagem |
| `horoscope_score: 75` | + elementos (Fogo+Fogo), aspecto (Trígono) |
| `pythagorean_score: 85` | + números do destino (5, 7), significados |
| Nenhuma similaridade | Interesses 85%, Personalidade 72%... |

---

## 📝 Exemplo de Prompt Enriquecido para o Gemini

Com os novos dados, o Gemini pode gerar frases muito mais contextualizadas:

**Antes:**
> "Rogerio e Domilcia têm 65% de compatibilidade!"

**Depois:**
> "Áries e Leão, dois signos de Fogo! 🔥 A chama entre Rogerio e Domilcia promete aquecer corações. O destino número 3 sussurra criatividade e comunicação — bora conversar até o sol nascer, meus jovens!"

---

## ✅ Checklist de Implementação

- [ ] Adicionar os novos models Pydantic
- [ ] Atualizar o endpoint `/generate-phrase`
- [ ] Construir prompt enriquecido com os novos dados
- [ ] Testar com o Flutter atualizado
- [ ] Verificar se o Gemini gera frases mais ricas

---

## 🚀 Teste Rápido

Depois de atualizar, podes testar com curl:

```bash
curl -X POST http://localhost:8000/generate-phrase \
  -H "Content-Type: application/json" \
  -d '{
    "overall_score": 65,
    "same_gender": false,
    "name1": "Rogério",
    "name2": "Domilcia",
    "letters": {"score": 30, "result_type": "Amor"},
    "flames": {"score": 100, "result_type": "Casamento", "flames_letter": "M"},
    "true_love": {"score": 20, "interests_similarity": 0.85},
    "horoscope": {"score": 75, "sign1": "Áries", "sign2": "Leão", "element1": "Fogo", "element2": "Fogo", "same_element": true},
    "pythagorean": {"score": 85, "destiny1": 5, "destiny2": 7, "relationship_number": 3, "relationship_meaning": "Comunicação"}
  }'
```

---

## 📁 Ficheiros Alterados

| Ficheiro | Alteração |
|----------|-----------|
| `backend/main.py` | Novos models + prompt enriquecido |
| `lib/data/services/api_service.dart` | ✅ Já atualizado (envia payload completo) |

---

*Gerado em 25/12/2025 - Mi and You Project*
