# test_update.py
# -*- coding: utf-8 -*-
"""
Script para testar o sistema de auto-atualização
"""

import time
from updater import AutoUpdater

def test_updater():
    print("Testando sistema de auto-atualizacao...")
    print("=" * 50)

    # Simula versão antiga
    updater = AutoUpdater(current_version="v1.0.0")

    print(f"Versao atual simulada: {updater.current_version}")
    print("Verificando por atualizacoes...")

    try:
        update_info = updater.check_for_updates()

        if update_info:
            print(f"✅ Nova versao encontrada: {update_info['version']}")
            print(f"Nome: {update_info['name']}")
            print(f"Assets: {len(update_info['assets'])} arquivo(s)")

            # Mostra assets disponíveis
            for asset in update_info['assets']:
                print(f"  - {asset['name']} ({asset['size']} bytes)")

            return True
        else:
            print("❌ Nenhuma atualizacao encontrada")
            return False

    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def wait_for_release():
    """Aguarda até que uma release seja criada"""
    print("Aguardando release ser criada...")
    max_attempts = 20

    for attempt in range(max_attempts):
        print(f"Tentativa {attempt + 1}/{max_attempts}")

        if test_updater():
            print("🎉 Release encontrada!")
            return True

        if attempt < max_attempts - 1:
            print("Aguardando 30 segundos...")
            time.sleep(30)

    print("❌ Release nao foi criada no tempo esperado")
    return False

if __name__ == "__main__":
    wait_for_release()