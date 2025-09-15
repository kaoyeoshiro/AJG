# config.py
# -*- coding: utf-8 -*-
"""
Configurações embutidas para o executável
Substitui a dependência do arquivo .env
"""

# ==================================================
# CONFIGURAÇÕES DO TJ-MS
# ==================================================
# IMPORTANTE: Substitua pelos valores reais antes de compilar
TJ_WSDL_URL = "https://esaj.tjms.jus.br/mniws/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl"
TJ_WS_USER = "PGEMS"
TJ_WS_PASS = "SAJ03PGEMS"

# ==================================================
# CONFIGURAÇÕES DO OPENROUTER
# ==================================================
import os

# Tenta carregar de diferentes fontes (ordem de prioridade):
# 1. Variável de ambiente
# 2. Arquivo config_local.py (ignorado pelo git)
# 3. Definição direta (para executável final)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Se não encontrou via ambiente, tenta config_local.py
if not OPENROUTER_API_KEY:
    try:
        from config_local import OPENROUTER_API_KEY as LOCAL_KEY
        OPENROUTER_API_KEY = LOCAL_KEY
    except ImportError:
        pass

# Para executável compilado: substitua "SUA_CHAVE_AQUI" pela chave real antes de compilar
if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "SUA_CHAVE_AQUI":
    OPENROUTER_API_KEY = "SUA_CHAVE_AQUI"  # SUBSTITUA AQUI PARA O EXECUTÁVEL

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.5-flash"

# ==================================================
# OUTRAS CONFIGURAÇÕES
# ==================================================
STRICT_CNJ_CHECK = False

# Classes de Cumprimento
CLASSES_CUMPRIMENTO = {
    "155","156","12231","15430","12078","15215","15160",
    "12246","10980","157","15161","10981","229"
}

# Namespaces XML
NS = {
    "soap": "http://schemas.xmlsoap.org/soap/envelope/",
    "ns2":  "http://www.cnj.jus.br/intercomunicacao-2.2.2",
}