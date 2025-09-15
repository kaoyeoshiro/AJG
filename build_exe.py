# build_exe.py
# -*- coding: utf-8 -*-
"""
Script para configurar e compilar o executável .exe usando PyInstaller
"""

import os
import subprocess
import sys
from pathlib import Path

def install_pyinstaller():
    """Instala PyInstaller se não estiver disponível"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado com sucesso")

def create_spec_file():
    """Cria arquivo .spec personalizado para PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_exe.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'requests',
        'xml.etree.ElementTree',
        'lxml',
        'json',
        'base64',
        'threading',
        'logging',
        'datetime',
        'typing',
        'updater',
        'tempfile',
        'shutil',
        'subprocess',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'pillow'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RelatorioTJMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Desabilita janela do console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione caminho do ícone se tiver: icon='icon.ico'
)
'''

    with open('RelatorioTJMS.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("✅ Arquivo RelatorioTJMS.spec criado")

def build_executable():
    """Compila o executável usando PyInstaller"""
    print("🔨 Iniciando compilação do executável...")

    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "RelatorioTJMS.spec"
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Compilação concluída com sucesso!")
        print(f"📁 Executável criado em: dist/RelatorioTJMS.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na compilação:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🚀 Script de Build - Relatório TJ-MS")
    print("=" * 50)

    # Verifica se estamos no diretório correto
    if not Path("main_exe.py").exists():
        print("❌ Erro: main_exe.py não encontrado no diretório atual")
        print("Execute este script no diretório do projeto")
        return False

    # Verifica se config.py foi configurado
    if not Path("config.py").exists():
        print("❌ Erro: config.py não encontrado")
        return False

    # Lê config.py para verificar configuração
    with open("config.py", "r", encoding="utf-8") as f:
        config_content = f.read()

    # Verifica se há placeholders críticos (mas permite SUA_CHAVE_AQUI para build automático)
    if "SEU_TJ_WSDL_URL_AQUI" in config_content:
        print("⚠️  ATENÇÃO: Configure as variáveis TJ em config.py antes de compilar!")
        print("   Substitua os valores 'SEU_TJ_*_AQUI' pelas configurações reais")
        return False

    # Para GitHub Actions ou desenvolvimento, permite placeholder da API key
    if "SUA_CHAVE_AQUI" in config_content:
        print("ℹ️  Nota: OPENROUTER_API_KEY usando placeholder - configurar antes do uso")

    print("✅ Configurações verificadas")

    # Instala PyInstaller
    install_pyinstaller()

    # Cria arquivo .spec
    create_spec_file()

    # Compila executável
    success = build_executable()

    if success:
        print()
        print("🎉 Build concluído com sucesso!")
        print("📁 Arquivos gerados:")
        print("   - dist/RelatorioTJMS.exe (executável principal)")
        print("   - build/ (arquivos temporários - pode deletar)")
        print()
        print("🧪 Para testar:")
        print("   1. Copie o executável para outro computador")
        print("   2. Execute: dist/RelatorioTJMS.exe")
        print("   3. Teste todas as funcionalidades")

    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)