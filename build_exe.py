#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir executável com PyInstaller
Resolve problemas de dependências do requests e outros módulos
"""

import subprocess
import sys
import os
import shutil

def clean_build_dirs():
    """Remove diretórios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removendo diretório: {dir_name}")
            shutil.rmtree(dir_name)

def build_exe():
    """Constrói o executável usando PyInstaller com configurações otimizadas"""

    print("Iniciando construção do executável...")

    # Comando PyInstaller otimizado
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Arquivo único
        '--noconsole',                  # Sem janela de console
        '--name=AJG',                   # Nome do executável
        '--clean',                      # Limpa cache
        '--noconfirm',                  # Não pede confirmação

        # Módulos principais
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',

        # Requests e dependências
        '--hidden-import=requests',
        '--hidden-import=requests.adapters',
        '--hidden-import=requests.auth',
        '--hidden-import=requests.cookies',
        '--hidden-import=requests.models',
        '--hidden-import=requests.sessions',
        '--hidden-import=urllib3',
        '--hidden-import=certifi',
        '--hidden-import=charset_normalizer',
        '--hidden-import=idna',

        # XML processing
        '--hidden-import=xml.etree.ElementTree',
        '--hidden-import=lxml',
        '--hidden-import=lxml.etree',

        # Scripts customizados
        '--hidden-import=scripts.updater',
        '--hidden-import=scripts.key_manager',

        # Outros módulos essenciais
        '--hidden-import=json',
        '--hidden-import=base64',
        '--hidden-import=threading',
        '--hidden-import=logging',
        '--hidden-import=datetime',
        '--hidden-import=typing',
        '--hidden-import=tempfile',
        '--hidden-import=shutil',
        '--hidden-import=subprocess',
        '--hidden-import=pathlib',
        '--hidden-import=ssl',
        '--hidden-import=socket',

        # Incluir diretório scripts
        '--add-data=scripts;scripts',

        # Arquivo principal
        'main_exe.py'
    ]

    try:
        print("Executando comando PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=600)
        print("✅ Executável criado com sucesso!")
        print("Localização:", os.path.join("dist", "AJG.exe"))
        return True

    except subprocess.CalledProcessError as e:
        print("❌ Erro ao criar executável:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout: Processo demorou mais de 10 minutos")
        return False

def main():
    """Função principal"""
    print("=== BUILD EXECUTÁVEL RELATÓRIO TJ-MS ===")

    # Verificar se estamos no diretório correto
    if not os.path.exists('main_exe.py'):
        print("❌ Arquivo main_exe.py não encontrado!")
        print("Execute este script no diretório raiz do projeto.")
        sys.exit(1)

    # Limpar diretórios antigos
    clean_build_dirs()

    # Construir executável
    success = build_exe()

    if success:
        print("\n✅ Build concluído com sucesso!")
        print("Execute: dist/AJG.exe")
    else:
        print("\n❌ Build falhou. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()