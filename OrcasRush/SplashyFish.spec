# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SplashyFish.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/bgm.mp3', 'assets'), ('assets/orca.png', 'assets'), ('assets/pipe01.png', 'assets'), ('assets/pipe02.png', 'assets'), ('assets/pipe03.png', 'assets'), ('assets/pipe04.png', 'assets'), ('assets/pipe05.png', 'assets'), ('assets/pipe06.png', 'assets'), ('assets/swim.wav', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SplashyFish',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='SplashyFish.app',
    icon=None,
    bundle_identifier=None,
)
