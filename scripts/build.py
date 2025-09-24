# scripts/build.py
# -*- coding: utf-8 -*-
"""
Script unificado para compilar o executável AJG.
Atualizado para coletar explicitamente a stack HTTP (requests, urllib3, certifi, etc.)
mitigando erros de ModuleNotFoundError em ambientes limpos.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Adiciona diretório pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Pacotes que precisam ter TODO o conteúdo coletado
HTTP_SUBMODULE_TARGETS = ("requests", "urllib3", "charset_normalizer", "idna")
HTTP_DATAS_TARGETS = ("requests", "urllib3", "certifi", "charset_normalizer", "idna")


def install_pyinstaller():
    """Instala PyInstaller se não estiver disponível"""
    try:
        import PyInstaller  # pylint: disable=import-outside-toplevel
        print("OK - PyInstaller já está instalado")
        return True
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("OK - PyInstaller instalado com sucesso")
        return True


def get_api_key():
    """Obtém a chave API de diferentes fontes"""
    import config  # pylint: disable=import-outside-toplevel

    key = config.OPENROUTER_API_KEY
    if key and key != "SUA_CHAVE_AQUI":
        print(f"OK - Chave configurada: {key[:20]}...")
        return key

    print("ATENÇÃO - Chave API não encontrada!")
    print("Você pode:")
    print("1. Criar arquivo .env com: OPENROUTER_API_KEY=sua-chave")
    print("2. Definir variável de ambiente: set OPENROUTER_API_KEY=sua-chave")
    print("3. Criar config_local.py com: OPENROUTER_API_KEY = 'sua-chave'")
    print("4. Inserir aqui diretamente (temporário)")

    key = input("\nDigite sua chave OpenRouter (sk-or-v1-...) ou ENTER para continuar sem chave: ").strip()

    if key and key.startswith("sk-or-v1-"):
        return key

    print("Continuando sem chave API configurada...")
    return None


def prepare_config(api_key=None):
    """Prepara o config.py para o build"""
    if not api_key:
        return True

    config_file = Path("config.py")
    backup_file = Path("config_original.py")

    if config_file.exists():
        shutil.copy2(config_file, backup_file)

        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content = content.replace(
            'OPENROUTER_API_KEY = "SUA_CHAVE_AQUI"',
            f'OPENROUTER_API_KEY = "{api_key}"'
        )

        with open(config_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print("OK - Config temporário criado com chave API")
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
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None


def _urllib3_filter(name):
    return 'contrib.emscripten' not in name


hiddenimports = [
    # GUI modules
    'tkinter',
    'tkinter.ttk',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
    'tkinter.filedialog',

    # Base HTTP modules
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',

    # XML processing
    'xml.etree.ElementTree',
    'lxml',
    'lxml.etree',
    'lxml.objectify',

    # Standard library
    'json',
    'base64',
    'threading',
    'logging',
    'datetime',
    'typing',
    'tempfile',
    'shutil',
    'subprocess',
    'pathlib',
    'os',
    'sys',
    're',
    'html',

    # Custom modules
    'scripts.updater',
    'scripts.key_manager',
]

http_submodule_targets = {HTTP_SUBMODULE_TARGETS!r}
for module_name in http_submodule_targets:
    try:
        if module_name == 'urllib3':
            hiddenimports += collect_submodules(module_name, filter=_urllib3_filter)
        else:
            hiddenimports += collect_submodules(module_name)
    except ImportError:
        pass


datas = [
    ('scripts', 'scripts'),
]

http_data_targets = {HTTP_DATAS_TARGETS!r}
for module_name in http_data_targets:
    try:
        datas += collect_data_files(module_name)
    except ImportError:
        pass


a = Analysis(
    ['main_exe.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''

    with open('AJG.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("OK - Arquivo AJG.spec criado")


def build_executable():
    """Compila o executável usando PyInstaller"""
    print("Iniciando compilação do executável...")

    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "AJG.spec"
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("OK - Compilação concluída com sucesso!")
        print("Executável criado em: dist/AJG.exe")
        return True
    except subprocess.CalledProcessError as e:
        print("ERRO na compilação:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def main():
    """Função principal do script de build"""
    print("Script de Build Unificado - AJG (Assistência Judiciária Gratuita)")
    print("=" * 50)

    if not Path("main_exe.py").exists():
        print("ERRO: main_exe.py não encontrado no diretório atual")
        print("Execute este script no diretório raiz do projeto")
        return False

    if not Path("config.py").exists():
        print("ERRO: config.py não encontrado")
        return False

    use_key = "--with-key" in sys.argv

    api_key = None
    if use_key:
        print("\nConfiguração de chave API habilitada")
        api_key = get_api_key()

    try:
        if api_key:
            prepare_config(api_key)

        with open("config.py", "r", encoding="utf-8") as f:
            config_content = f.read()

        if "SEU_TJ_WSDL_URL_AQUI" in config_content:
            print("ATENÇÃO: Configure as variáveis TJ em config.py antes de compilar!")
            print("Substitua os valores 'SEU_TJ_*_AQUI' pelas configurações reais")
            return False

        if "SUA_CHAVE_AQUI" in config_content and not api_key:
            print("Nota: OPENROUTER_API_KEY usando placeholder - configurar antes do uso")

        print("OK - Configurações verificadas")

        install_pyinstaller()
        create_spec_file()
        success = build_executable()

        if success:
            print()
            print("Build concluído com sucesso!")
            print("Arquivos gerados:")
            print("   - dist/AJG.exe (executável principal)")
            print("   - build/ (arquivos temporários - pode deletar)")
            print()
            print("Para testar:")
            print("   1. Copie o executável para outro computador")
            print("   2. Execute: dist/AJG.exe")
            print("   3. Teste todas as funcionalidades")

        return success

    except Exception as e:  # pylint: disable=broad-except
        print(f"ERRO inesperado: {e}")
        return False
    finally:
        if api_key:
            restore_config()


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
