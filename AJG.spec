# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_exe.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Incluir certificados SSL do requests/certifi
        ('scripts', 'scripts'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'requests',
        'requests.adapters',
        'requests.auth',
        'requests.cookies',
        'requests.models',
        'requests.sessions',
        'requests.packages',
        'requests.packages.urllib3',
        'requests.packages.urllib3.util',
        'requests.packages.urllib3.util.retry',
        'urllib3',
        'urllib3.util',
        'urllib3.util.retry',
        'certifi',
        'charset_normalizer',
        'idna',
        'xml.etree.ElementTree',
        'lxml',
        'lxml.etree',
        'lxml.objectify',
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
        'ssl',
        'socket',
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
