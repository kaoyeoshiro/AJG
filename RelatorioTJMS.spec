# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_exe.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('config.py', '.'),
    ],
    hiddenimports=[
        'requests',
        'tkinter',
        'xml.etree.ElementTree',
        'json',
        'base64',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PIL',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
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
    strip=True,  # Remove debug symbols
    upx=False,   # Não usar UPX (suspeito)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',  # Se tiver arquivo de versão
    icon='icon.ico'  # Se tiver ícone
)