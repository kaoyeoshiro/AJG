#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir executável com PyInstaller.
Inclui coleta explícita da stack HTTP (requests, urllib3, certifi, etc.)
para evitar erros de ModuleNotFoundError em ambientes limpos.
"""

import subprocess
import sys
import os
import shutil

# Pacotes cujo conteúdo completo deve ser coletado
HTTP_STACK_MODULES = [
    "requests",
    "urllib3",
    "certifi",
    "charset_normalizer",
    "idna",
]

# Imports que o PyInstaller nem sempre detecta sozinho
HIDDEN_IMPORTS = [
    # GUI
    "tkinter",
    "tkinter.ttk",
    "tkinter.scrolledtext",
    "tkinter.messagebox",
    "tkinter.filedialog",

    # HTTP stack base
    "requests",
    "urllib3",
    "certifi",
    "charset_normalizer",
    "idna",

    # XML processing
    "xml.etree.ElementTree",
    "lxml",
    "lxml.etree",

    # Scripts customizados
    "scripts.updater",
    "scripts.key_manager",
]


def clean_build_dirs():
    """Remove diretórios de builds anteriores para evitar resíduos"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removendo diretório: {dir_name}")
            shutil.rmtree(dir_name)


def build_exe():
    """Constrói o executável usando PyInstaller com configurações otimizadas"""

    print("Iniciando construção do executável...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--noconsole',
        '--name=AJG',
        '--clean',
        '--noconfirm',
    ]

    # Imports explícitos
    for module in HIDDEN_IMPORTS:
        cmd.append(f'--hidden-import={module}')

    # Coleta completa da stack HTTP (código + dados, ex: cacert.pem)
    for module in HTTP_STACK_MODULES:
        cmd.append(f'--collect-all={module}')

    # Dados adicionais
    cmd.extend([
        '--add-data=scripts;scripts',
        'main_exe.py',
    ])

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

    if not os.path.exists('main_exe.py'):
        print("❌ Arquivo main_exe.py não encontrado!")
        print("Execute este script no diretório raiz do projeto.")
        sys.exit(1)

    clean_build_dirs()

    success = build_exe()

    if success:
        print("\n✅ Build concluído com sucesso!")
        print("Execute: dist/AJG.exe")
    else:
        print("\n❌ Build falhou. Verifique os erros acima.")
        sys.exit(1)


if __name__ == "__main__":
    main()
