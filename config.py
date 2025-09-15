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
# IMPORTANTE: Substitua pela sua API key real
OPENROUTER_API_KEY = "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"
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