# -*- mode: python ; coding: utf-8 -*-

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

http_submodule_targets = ('requests', 'urllib3', 'charset_normalizer', 'idna')
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

http_data_targets = ('requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna')
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
