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

# Função para carregar arquivo .env
def load_env_file(env_file=".env"):
    """Carrega variáveis do arquivo .env se existir"""
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and not os.getenv(key):  # Só define se não existe
                            os.environ[key] = value
        except Exception as e:
            print(f"Aviso: Erro ao carregar .env: {e}")

# Carrega .env primeiro
load_env_file()

# Tenta carregar de diferentes fontes (ordem de prioridade):
# 1. Variável de ambiente (incluindo .env)
# 2. Arquivo config_local.py (ignorado pelo git)
# 3. Chave salva pelo key_manager
# 4. Definição direta (para executável final)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Se não encontrou via ambiente, tenta config_local.py
if not OPENROUTER_API_KEY:
    try:
        from config_local import OPENROUTER_API_KEY as LOCAL_KEY
        OPENROUTER_API_KEY = LOCAL_KEY
    except ImportError:
        pass

# Se ainda não tem chave, tenta carregar do key_manager
if not OPENROUTER_API_KEY:
    try:
        from key_manager import KeyManager
        km = KeyManager()
        saved_key = km.load_key()
        if saved_key:
            OPENROUTER_API_KEY = saved_key
    except ImportError:
        pass

# Para executável compilado: substitua "SUA_CHAVE_AQUI" pela chave real antes de compilar
if not OPENROUTER_API_KEY or OPENROUTER_API_KEY in ["SUA_CHAVE_AQUI", "GITHUB_BUILD_PLACEHOLDER"]:
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