import sys
import os

# Adiciona o diretório pai ao path para importar main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel serverless entry point
# O Vercel procura por uma variável 'app' no arquivo especificado em vercel.json

# Handler para Vercel (necessário para serverless functions)
handler = app
