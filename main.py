from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Optional, Dict
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

app = FastAPI(
    title="Mi and You API",
    description="API para gerar frases de compatibilidade usando Google Gemini",
    version="2.0.0"
)


# ========== MODELS DE ALGORITMOS ==========

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


class PhraseResponse(BaseModel):
    phrase: str

# Configuração da API Key do Google Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Mi and You API is running!"}


@app.post("/generate-phrase", response_model=PhraseResponse)
async def generate_phrase(data: CompatibilityRequest):
    if not GEMINI_API_KEY:
        return PhraseResponse(phrase="O universo conspira a vosso favor!")

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Construir contexto enriquecido para o Gemini
        prompt = f"""
# PROMPT (CONTEXT — NÃO CITAR/EXPLICAR OS DADOS)
# Tens acesso a várias leituras internas sobre a ligação entre duas pessoas.
# Não deves mencionar nem explicar percentagens, scores, nomes de métodos ou cálculos.
# Sintetiza tudo numa ou duas frases que soem como uma revelação poética.

## Nomes do casal:
- {data.name1} e {data.name2}
- Mesmo género: {"sim" if data.same_gender else "não"}

## Intensidade geral (uso interno — NÃO revelar):
- Força da conexão: {"muito alta" if data.overall_score >= 80 else "alta" if data.overall_score >= 65 else "moderada" if data.overall_score >= 45 else "suave"}

## FLAMES (resultado textual — PRIORIZAR se Amor/Casamento):
- Resultado: {data.flames.result_type or "?"}
- Letra FLAMES: {data.flames.flames_letter or "?"}
- Score interno: {data.flames.score}

## Letras (resultado textual — PRIORIZAR se Amor/Paixão):
- Resultado: {data.letters.result_type or "?"}
- Score interno: {data.letters.score}

## Astrologia:
- Signos: {data.horoscope.sign1 or "?"} ({data.horoscope.element1 or "?"}, {data.horoscope.quality1 or "?"}) + {data.horoscope.sign2 or "?"} ({data.horoscope.element2 or "?"}, {data.horoscope.quality2 or "?"})
- Mesmo elemento: {"sim — harmonia natural, mesma energia" if data.horoscope.same_element else "não — energias complementares, dança de opostos"}
- Análise de aspecto: {data.horoscope.aspect_analysis or "neutro"}
- Score interno: {data.horoscope.score}

## Numerologia pitagórica:
- Número do destino de {data.name1}: {data.pythagorean.destiny1 or "?"} ({data.pythagorean.meaning1 or "?"})
- Número do destino de {data.name2}: {data.pythagorean.destiny2 or "?"} ({data.pythagorean.meaning2 or "?"})
- Número do relacionamento: {data.pythagorean.relationship_number or "?"} — {data.pythagorean.relationship_meaning or "?"}
- Score interno: {data.pythagorean.score}

## TrueLove (afinidades — usar como textura emocional):
- Interesses em comum: {"muito altos" if (data.true_love.interests_similarity or 0) >= 0.7 else "moderados" if (data.true_love.interests_similarity or 0) >= 0.4 else "diferentes mas complementares"}
- Personalidades: {"muito compatíveis" if (data.true_love.personality_similarity or 0) >= 0.7 else "complementares" if (data.true_love.personality_similarity or 0) >= 0.4 else "contrastantes — desafio de crescimento"}
- Proximidade/localização: {"próximos" if (data.true_love.location_similarity or 0) >= 0.7 else "distância moderada" if (data.true_love.location_similarity or 0) >= 0.4 else "distantes — amor que atravessa"}
- Idades: {"muito compatíveis" if (data.true_love.age_similarity or 0) >= 0.7 else "compatíveis" if (data.true_love.age_similarity or 0) >= 0.4 else "gerações diferentes — sabedoria compartilhada"}
- Score interno: {data.true_love.score}

## Regras de interpretação (NÃO explicar ao utilizador):
1. Se FLAMES = "Amor" ou "Casamento" ou Letras = "Amor" → núcleo da frase deve ser compromisso, aliança, promessa eterna
2. Se FLAMES = "Paixão" ou Letras = "Paixão" → núcleo deve ser chama, desejo, intensidade ardente
3. Se mesmo elemento (especialmente Fogo) → usar imagens de chama, calor, combustão
4. Se elementos opostos (Fogo+Água, Terra+Ar) → usar imagens de equilíbrio, dança, complemento
5. Se número do relacionamento é 6, 2 ou 9 → forte destino, escrito nas estrelas
6. Se afinidades TrueLove altas → almas gémeas, mesma vibração, sintonia
7. Se houver sinais mistos → transformar em riqueza narrativa ("fogo que aprende", "dança de opostos")
8. Se houver fraquezas → suavizar como desafio belo ("crescimento", "ajuste", "aprendizagem mútua")

## Instruções de estilo:
- Gera 1–2 frases curtas, místicas, confiantes e intensamente românticas.
- Tom: sábio, poético, quente; como quem entrega uma verdade íntima.
- Linguagem: natural, com gírias angolanas leves se fizerem sentido.
- Restrições: NÃO citar scores, percentagens, nem nomes de técnicas ou algoritmos. NÃO explicar o processo. Evitar clichés banais.
- Opcional: até 1 emoji discreto.
- Saída: apenas a(s) frase(s) final(is).

## Exemplos de tom (NÃO copiar literalmente):
- Casamento/compromisso forte: "Entre {data.name1} e {data.name2} há uma aliança que fala de lar e eternidade — caminham com o pacto escrito nas estrelas." ✨
- Amor/paixão intensa: "A chama entre {data.name1} e {data.name2} não é só desejo; é promessa que arde bonita e funda o amanhã."
- Sinais mistos/desafio: "Vocês são fogo que aprende; a intensidade é ponte e o desafio é convite para crescerem juntos."
- Elementos opostos mas fortes: "Água e fogo dançam em {data.name1} e {data.name2} — o vapor que sobe é o amor que transforma."
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

        phrase = (response.text or "").strip()
        if not phrase:
            phrase = f"A conexão entre {data.name1} e {data.name2} é especial! ✨"
        return PhraseResponse(phrase=phrase)

    except Exception as e:
        print(f"Erro interno: {str(e)}")
        return PhraseResponse(phrase=f"A energia entre {data.name1} e {data.name2} é única e misteriosa!")

# Para rodar localmente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
