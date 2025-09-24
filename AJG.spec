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
        # GUI modules
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',

        # Requests and HTTP libraries - comprehensive list
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
        'requests.packages',
        'requests.packages.urllib3',
        'requests.packages.urllib3.exceptions',
        'requests.packages.urllib3.fields',
        'requests.packages.urllib3.filepost',
        'requests.packages.urllib3.poolmanager',
        'requests.packages.urllib3.util',
        'requests.packages.urllib3.util.retry',
        'requests.packages.urllib3.util.ssl_',
        'requests.sessions',
        'requests.status_codes',
        'requests.structures',
        'requests.utils',

        # urllib3 comprehensive
        'urllib3',
        'urllib3._collections',
        'urllib3.connection',
        'urllib3.connectionpool',
        'urllib3.exceptions',
        'urllib3.fields',
        'urllib3.filepost',
        'urllib3.poolmanager',
        'urllib3.response',
        'urllib3.util',
        'urllib3.util.connection',
        'urllib3.util.retry',
        'urllib3.util.ssl_',
        'urllib3.util.timeout',
        'urllib3.util.url',

        # SSL and certificates
        'certifi',
        'ssl',
        'socket',
        '_ssl',

        # Encoding
        'charset_normalizer',
        'charset_normalizer.api',
        'charset_normalizer.cd',
        'charset_normalizer.models',
        'charset_normalizer.utils',
        'idna',
        'idna.core',
        'idna.idnadata',
        'idna.intranges',
        'idna.package_data',
        'idna.uts46data',

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
