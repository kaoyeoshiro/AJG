import sys
from pathlib import Path

# Adiciona diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config

key = config.OPENROUTER_API_KEY
if key and key != "SUA_CHAVE_AQUI":
    print(f"OK - Chave configurada: {key[:20]}...")
else:
    print("ATENCAO - Chave precisa ser configurada")
    print("Para compilar o executavel, use: python scripts/build.py --with-key")