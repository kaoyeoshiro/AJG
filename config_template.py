# config_template.py
# -*- coding: utf-8 -*-
"""
Template de configurações para o executável
COPIE este arquivo para config.py e configure as variáveis
"""

# ==================================================
# CONFIGURAÇÕES DO TJ-MS
# ==================================================
TJ_WSDL_URL = "https://esaj.tjms.jus.br/mniws/servico-intercomunicacao-2.2.2/intercomunicacao?wsdl"
TJ_WS_USER = "PGEMS"
TJ_WS_PASS = "SAJ03PGEMS"

# ==================================================
# CONFIGURAÇÕES DO OPENROUTER
# ==================================================
# IMPORTANTE: Configure via variáveis de ambiente
import os
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "SUA_CHAVE_API_AQUI")
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