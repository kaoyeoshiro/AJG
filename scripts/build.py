# scripts/build.py
# -*- coding: utf-8 -*-
"""
Script unificado para compilar o executável AJG
Combina funcionalidades de build_exe.py e build_with_key.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Adiciona diretório pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def install_pyinstaller():
    """Instala PyInstaller se não estiver disponível"""
    try:
        import PyInstaller
        print("OK - PyInstaller ja esta instalado")
        return True
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("OK - PyInstaller instalado com sucesso")
        return True

def get_api_key():
    """Obtém a chave API de diferentes fontes"""
    # 1. Importa config (que já carrega .env automaticamente)
    import config

    key = config.OPENROUTER_API_KEY
    if key and key != "SUA_CHAVE_AQUI":
        print(f"OK - Chave configurada: {key[:20]}...")
        return key

    # Se não encontrou, pedir ao usuário
    print("ATENCAO - Chave API nao encontrada!")
    print("Voce pode:")
    print("1. Criar arquivo .env com: OPENROUTER_API_KEY=sua-chave")
    print("2. Definir variavel de ambiente: set OPENROUTER_API_KEY=sua-chave")
    print("3. Criar config_local.py com: OPENROUTER_API_KEY = 'sua-chave'")
    print("4. Inserir aqui diretamente (temporario)")

    key = input("\nDigite sua chave OpenRouter (sk-or-v1-...) ou ENTER para continuar sem chave: ").strip()

    if key and key.startswith("sk-or-v1-"):
        return key

    print("Continuando sem chave API configurada...")
    return None

def prepare_config(api_key=None):
    """Prepara o config.py para o build"""
    if not api_key:
        return True

    # Backup do config original
    config_file = Path("config.py")
    backup_file = Path("config_original.py")

    if config_file.exists():
        shutil.copy2(config_file, backup_file)

        # Lê o config atual
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Substitui a placeholder pela chave real
        updated_content = content.replace(
            'OPENROUTER_API_KEY = "SUA_CHAVE_AQUI"',
            f'OPENROUTER_API_KEY = "{api_key}"'
        )

        # Salva temporariamente
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print("OK - Config temporario criado com chave API")
        return True

    return False

def restore_config():
    """Restaura o config original após o build"""
    backup_file = Path("config_original.py")
    config_file = Path("config.py")

    if backup_file.exists():
        shutil.move(backup_file, config_file)
        print("OK - Config original restaurado")

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
        'scripts.updater',
        'scripts.key_manager',
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
    name='AJG',
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

    with open('AJG.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("OK - Arquivo AJG.spec criado")

def build_executable():
    """Compila o executável usando PyInstaller"""
    print("Iniciando compilacao do executavel...")

    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "AJG.spec"
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("OK - Compilacao concluida com sucesso!")
        print(f"Executavel criado em: dist/AJG.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERRO na compilacao:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Função principal do script de build"""
    print("Script de Build Unificado - AJG (Assistencia Judiciaria Gratuita)")
    print("=" * 50)

    # Verifica se estamos no diretório correto
    if not Path("main_exe.py").exists():
        print("ERRO: main_exe.py nao encontrado no diretorio atual")
        print("Execute este script no diretorio raiz do projeto")
        return False

    # Verifica se config.py existe
    if not Path("config.py").exists():
        print("ERRO: config.py nao encontrado")
        return False

    # Argumentos de linha de comando
    use_key = "--with-key" in sys.argv

    api_key = None
    if use_key:
        print("\nConfiguracao de chave API habilitada")
        api_key = get_api_key()

    try:
        # Prepara configuração se necessário
        if api_key:
            prepare_config(api_key)

        # Verifica configuração
        with open("config.py", "r", encoding="utf-8") as f:
            config_content = f.read()

        if "SEU_TJ_WSDL_URL_AQUI" in config_content:
            print("ATENCAO: Configure as variaveis TJ em config.py antes de compilar!")
            print("Substitua os valores 'SEU_TJ_*_AQUI' pelas configuracoes reais")
            return False

        if "SUA_CHAVE_AQUI" in config_content and not api_key:
            print("Nota: OPENROUTER_API_KEY usando placeholder - configurar antes do uso")

        print("OK - Configuracoes verificadas")

        # Instala PyInstaller
        install_pyinstaller()

        # Cria arquivo .spec
        create_spec_file()

        # Compila executável
        success = build_executable()

        if success:
            print()
            print("Build concluido com sucesso!")
            print("Arquivos gerados:")
            print("   - dist/AJG.exe (executavel principal)")
            print("   - build/ (arquivos temporarios - pode deletar)")
            print()
            print("Para testar:")
            print("   1. Copie o executavel para outro computador")
            print("   2. Execute: dist/AJG.exe")
            print("   3. Teste todas as funcionalidades")

        return success

    except Exception as e:
        print(f"ERRO inesperado: {e}")
        return False
    finally:
        # Sempre restaura o config original
        if api_key:
            restore_config()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)