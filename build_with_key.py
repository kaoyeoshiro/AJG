# build_with_key.py
# -*- coding: utf-8 -*-
"""
Script para compilar o executável com chave API configurada
"""

import os
import re
import sys
import shutil
from pathlib import Path

def get_api_key():
    """Obtém a chave API de diferentes fontes"""
    # 1. Variável de ambiente
    key = os.getenv("OPENROUTER_API_KEY", "")
    if key:
        print(f"✅ Chave encontrada via variável de ambiente: {key[:20]}...")
        return key

    # 2. config_local.py
    try:
        sys.path.insert(0, ".")
        from config_local import OPENROUTER_API_KEY
        print(f"✅ Chave encontrada em config_local.py: {OPENROUTER_API_KEY[:20]}...")
        return OPENROUTER_API_KEY
    except ImportError:
        pass

    # 3. Pedir ao usuário
    print("⚠️ Chave API não encontrada!")
    print("Você pode:")
    print("1. Definir variável de ambiente: set OPENROUTER_API_KEY=sua-chave")
    print("2. Criar config_local.py com: OPENROUTER_API_KEY = 'sua-chave'")
    print("3. Inserir aqui diretamente (temporário)")

    key = input("\nDigite sua chave OpenRouter (sk-or-v1-...): ").strip()
    if not key or not key.startswith("sk-or-v1-"):
        print("❌ Chave inválida!")
        sys.exit(1)

    return key

def create_config_with_key(api_key):
    """Cria uma versão temporária do config.py com a chave"""
    # Backup do config original
    shutil.copy2("config.py", "config_original.py")

    # Lê o config atual
    with open("config.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Substitui a placeholder pela chave real
    updated_content = content.replace(
        'OPENROUTER_API_KEY = "SUA_CHAVE_AQUI"',
        f'OPENROUTER_API_KEY = "{api_key}"'
    )

    # Salva temporariamente
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("✅ Config temporário criado com chave API")

def restore_config():
    """Restaura o config original"""
    if os.path.exists("config_original.py"):
        shutil.move("config_original.py", "config.py")
        print("✅ Config original restaurado")

def main():
    print("🚀 Build com Chave API - RelatorioTJMS")
    print("=" * 50)

    try:
        # Obtém a chave API
        api_key = get_api_key()

        # Cria config temporário com chave
        create_config_with_key(api_key)

        # Executa o build normal
        print("\n🔨 Iniciando compilação...")
        import subprocess
        result = subprocess.run([sys.executable, "build_exe.py"], check=True)

        print("✅ Compilação concluída com sucesso!")
        print("📁 Executável com chave API: dist/RelatorioTJMS.exe")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na compilação: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Build cancelado pelo usuário")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    finally:
        # Sempre restaura o config original
        restore_config()

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)