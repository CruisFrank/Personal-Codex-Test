# -*- mode: python ; coding: utf-8 -*-

import pathlib

block_cipher = None

root_dir = pathlib.Path(__file__).resolve().parents[2]
app_dir = root_dir / "app"

analysis = Analysis(
    ['app/main.py'],
    pathex=[str(root_dir)],
    binaries=[],
    datas=[
        (str(app_dir / 'components.py'), 'app'),
        (str(app_dir / '__init__.py'), 'app'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name='CircuitDesigner-1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CircuitDesigner-1.0'
)
