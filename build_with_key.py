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
    # 1. Importa config (que já carrega .env automaticamente)
    sys.path.insert(0, ".")
    import config

    key = config.OPENROUTER_API_KEY
    if key and key != "SUA_CHAVE_AQUI":
        print(f"✅ Chave configurada: {key[:20]}...")
        return key

    # Se não encontrou, pedir ao usuário
    print("⚠️ Chave API não encontrada!")
    print("Você pode:")
    print("1. Criar arquivo .env com: OPENROUTER_API_KEY=sua-chave")
    print("2. Definir variável de ambiente: set OPENROUTER_API_KEY=sua-chave")
    print("3. Criar config_local.py com: OPENROUTER_API_KEY = 'sua-chave'")
    print("4. Inserir aqui diretamente (temporário)")

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