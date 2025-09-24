# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys

block_cipher = None

print("=== DEBUG: Iniciando configuração do PyInstaller ===")

def _urllib3_filter(name):
    return 'contrib.emscripten' not in name


hiddenimports = [
    # GUI modules
    'tkinter',
    'tkinter.ttk',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
    'tkinter.filedialog',

    # Base HTTP modules - CRÍTICO
    'requests',
    'requests.adapters',
    'requests.api',
    'requests.auth',
    'requests.certs',
    'requests.compat',
    'requests.cookies',
    'requests.exceptions',
    'requests.hooks',
    'requests.models',
    'requests.sessions',
    'requests.status_codes',
    'requests.structures',
    'requests.utils',
    'urllib3',
    'urllib3._collections',
    'urllib3.connection',
    'urllib3.connectionpool',
    'urllib3.exceptions',
    'urllib3.poolmanager',
    'urllib3.response',
    'urllib3.util',
    'urllib3.util.retry',
    'urllib3.util.ssl_',
    'urllib3.util.timeout',
    'certifi',
    'charset_normalizer',
    'charset_normalizer.api',
    'charset_normalizer.models',
    'idna',
    'idna.core',

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
    'ssl',
    '_ssl',
    'socket',

    # Custom modules
    'scripts.updater',
    'scripts.key_manager',
]

print(f"DEBUG: hiddenimports iniciais: {len(hiddenimports)} módulos")

# Coleta automática de submódulos
http_submodule_targets = ('requests', 'urllib3', 'charset_normalizer', 'idna')
for module_name in http_submodule_targets:
    try:
        if module_name == 'urllib3':
            collected = collect_submodules(module_name, filter=_urllib3_filter)
        else:
            collected = collect_submodules(module_name)
        hiddenimports += collected
        print(f"DEBUG: Coletados {len(collected)} submódulos de {module_name}")
    except ImportError as e:
        print(f"DEBUG: Erro coletando submódulos de {module_name}: {e}")


datas = [
    ('scripts', 'scripts'),
]

# Coleta automática de arquivos de dados
http_data_targets = ('requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna')
for module_name in http_data_targets:
    try:
        collected = collect_data_files(module_name)
        datas += collected
        print(f"DEBUG: Coletados {len(collected)} arquivos de dados de {module_name}")
    except ImportError as e:
        print(f"DEBUG: Erro coletando dados de {module_name}: {e}")

print(f"DEBUG: Total hiddenimports: {len(hiddenimports)}")
print(f"DEBUG: Total datas: {len(datas)}")
print("=== DEBUG: Configuração concluída ===")
sys.stdout.flush()


a = Analysis(
    ['main_exe.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
